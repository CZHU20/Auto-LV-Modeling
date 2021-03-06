import os
import sys
sys.path.append(os.path.join(os.path.dirname(
__file__), "../src"))
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
import collections
from vtk.util.numpy_support import vtk_to_numpy, numpy_to_vtk
import label_io
import utils
"""
Functions to write interpolated surface meshes for perscribed wall motion

"""

def cubic_spline_ipl(time, t_m, dt_m, boundary_queue):
    """
    Cubic Hermite spline interpolation for nodes movement
    see https://en.wikipedia.org/wiki/Cubic_Hermite_spline

    Args:
        time: time index in range(num_itpls)+1
        t_m: initial time point
        dt_m: number of iterpolations
        boundary_queue: list of VTK PolyData
    
    Returns:
        coords: coordinates of the interpolated mesh
    """

    boundary0 = vtk_to_numpy(boundary_queue[0].GetPoints().GetData())
    boundary1 = vtk_to_numpy(boundary_queue[1].GetPoints().GetData())
    boundary2 = vtk_to_numpy(boundary_queue[2].GetPoints().GetData())
    boundary3 = vtk_to_numpy(boundary_queue[3].GetPoints().GetData())

    dim = boundary0.shape[-1]

    t_a = (float(time) - t_m)/dt_m
    h_00 = 2*t_a*t_a*t_a - 3*t_a*t_a + 1
    h_10 = t_a*t_a*t_a - 2*t_a*t_a + t_a
    h_01 = - 2*t_a*t_a*t_a + 3*t_a*t_a
    h_11 = t_a*t_a*t_a - t_a*t_a

    v_m = (boundary2-boundary0)/dt_m/2
    v_m1 = (boundary3-boundary1)/dt_m/2
    coords = h_00*boundary1 + h_01*boundary2 + h_10*v_m*dt_m + h_11*v_m1*dt_m
    return coords

def find_index_in_array(x, y):
    """
    For x being a list containing y, find the index of each element of y in x
    """
    xsorted = np.argsort(x)
    ypos = np.searchsorted(x[xsorted], y)
    indices = xsorted[ypos]
    return indices

def move_mesh(fns, start_point, intpl_num, num_cycle):
    total_num_phase = len(fns)
    total_steps = total_num_phase * (intpl_num+1)*num_cycle
    initialized = False
    poly_template = label_io.loadVTKMesh(fns[start_point])
    ref_coords = vtk_to_numpy(poly_template.GetPoints().GetData())
    store = np.zeros((poly_template.GetNumberOfPoints(), 3, total_steps+1)) 
    count = 0
    for c in range(num_cycle):
        for msh_idx in list(range(start_point, total_num_phase))+ list(range(0, start_point)):
            if not initialized:
                boundary_queue = collections.deque(4*[None], 4)
                boundary_queue.append(label_io.loadVTKMesh(fns[msh_idx]))
                boundary_queue.append(label_io.loadVTKMesh(fns[msh_idx]))
                boundary_queue.append(label_io.loadVTKMesh(fns[(msh_idx+1)%total_num_phase]))
                boundary_queue.append(label_io.loadVTKMesh(fns[(msh_idx+2)%total_num_phase]))
                initialized = True
            else:
                print(msh_idx)
                boundary_queue.append(label_io.loadVTKMesh(fns[(msh_idx+2)%total_num_phase]))

            for i_idx in range(intpl_num+1):
                new_coords = cubic_spline_ipl(i_idx, 0, intpl_num, boundary_queue)
                displacement = new_coords- ref_coords
                store[:, :, count] = displacement
                count+=1

    return store

def write_motion(fns,  start_point, intpl_num, output_dir, num_cycle, duration, debug=False):
    total_num_phase = len(fns)
    total_steps = num_cycle* total_num_phase * (intpl_num+1)
    initialized = False
    
    poly_template = label_io.loadVTKMesh(fns[start_point])
    
    displacements = move_mesh(fns, start_point, intpl_num, num_cycle)
    if debug:
        import vtk
        coords = vtk_to_numpy(poly_template.GetPoints().GetData())
        poly = vtk.vtkPolyData()
        poly.DeepCopy(poly_template)
        for ii in range(displacements.shape[-1]):
            poly.GetPoints().SetData(numpy_to_vtk(displacements[:,:,ii]+coords))
            fn_debug = os.path.join(output_dir, "debug%d.vtk" %ii)
            label_io.writeVTKPolyData(poly, fn_debug)

    node_ids = vtk_to_numpy(poly_template.GetPointData().GetArray('GlobalNodeID'))
    face_ids = vtk_to_numpy(poly_template.GetCellData().GetArray('ModelFaceID'))
    #write time steps and node numbers
    for face in np.unique(face_ids):
        fn = os.path.join(output_dir, '%d_motion.dat' % face)
        face_poly = utils.thresholdPolyData(poly_template, 'ModelFaceID', (face,face))
        f = open(fn, 'w')
        f.write('{} {} {}\n'.format(3, total_steps,face_poly.GetNumberOfPoints()))
        for t in np.linspace(0,num_cycle*duration, total_steps):
            f.write('{}\n'.format(t))
        #f.write('{}\n'.format(face_poly.GetNumberOfPoints()))
        face_ids = vtk_to_numpy(face_poly.GetPointData().GetArray('GlobalNodeID'))
        node_id_index = find_index_in_array(node_ids, face_ids)
        for i in node_id_index:
            disp = displacements[i, :, :]
            f.write('{}\n'.format(node_ids[i]))
            for j in range(total_steps):
                f.write('{} {} {}\n'.format(disp[0,j], disp[1,j],disp[2,j]))

        f.close()




if __name__=='__main__':
    import time
    import argparse
    start = time.time()
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--json_fn', help="Name of the json file")
    parser.add_argument('--phase', default=-1, type=int, help="Id of the phase to generate volume mesh")
    args = parser.parse_args()
    paras = label_io.loadJsonArgs(args.json_fn)
    
    mesh_dir = os.path.join(paras['out_dir'], paras['patient_id'], "surfaces")
    output_dir = os.path.join(paras['out_dir'], paras['patient_id'], paras['patient_id']+'-mesh-complete')

    try:
       os.makrdirs(output_dir)
    except Exception as e: print(e)
    import glob
    fns = sorted(glob.glob(os.path.join(mesh_dir, "*.vtk")))
    write_motion(fns,  args.phase ,paras['num_interpolation'], output_dir, paras['num_cycle'], paras['duration'], debug=False)
    end = time.time()
    print("Time spent: ", end-start)
