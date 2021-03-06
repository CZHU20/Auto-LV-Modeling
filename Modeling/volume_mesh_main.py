import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__),"src"))
import argparse
import numpy as np
import meshing
import models
import label_io
import time

if __name__ == '__main__':
    start = time.time()
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--json_fn', help="Name of the json file")
    parser.add_argument('--phase', default=-1, type=int, help="Id of the phase to generate volume mesh")
    args = parser.parse_args()

    paras = label_io.loadJsonArgs(args.json_fn)
    
    output_dir = os.path.join(paras['out_dir'], paras['patient_id'], "surfaces")

    volume_fn = np.load(os.path.join(output_dir, "volume.npy"))
    if args.phase == -1:
        phase = volume_fn[:,0][int(np.argmax(volume_fn[:,1]))]
    else:
        phase = args.phase
    poly_fn = os.path.join(output_dir, paras['model_output'] % phase)

    lvmodel = models.leftVentricle(label_io.loadVTKMesh(poly_fn))
    
    output_vol = os.path.join(paras['out_dir'], paras['patient_id'], paras['patient_id']+'-mesh-complete')
    lvmodel.remesh(paras['edge_size'], poly_fn, poly_fn=None, ug_fn=output_vol, mmg=False)
    lvmodel.writeMeshComplete(output_vol)
    end = time.time()
    print("Time spent in volume_mesh_main.py: ", end-start)
