"""
IO functions for importing and exporting label maps and mesh surfaces

@author: Fanwei Kong

"""
import SimpleITK as sitk
import numpy as np
import os
import vtk

def loadLabelMap2Py(fn):
    """ 
    This function imports the label map as numpy arrays.

    Args: 
        fn: filename of the label map

    Return:
        label: numpy array of the label map
        spacing: spacing information of the label map
    """
    mask = sitk.ReadImage(fn)
    label = sitk.GetArrayFromImage(mask)
    spacing = mask.GetSpacing()

    return label, spacing

def loadLabelMap(fn):
    """ 
    This function imports the label map as sitk image.

    Args: 
        fn: filename of the label map

    Return:
        label: label map as a sitk image
    """
    label = sitk.ReadImage(fn)

    return label

def exportPy2Sitk(npArr, sitkIm):
    """
    This function exports the numpy array to a sitk image
    
    Args:
        npArr: input numpy array
        sitkIm: reference sitk image
    Return:
        outSitkIm: output sitk image

    """
    outSitkIm = sitk.GetImageFromArray(npArr)
    outSitkIm.SetSpacing(sitkIm.GetSpacing())
    outSitkIm.SetOrigin(sitkIm.GetOrigin())
    outSitkIm.SetDirection(sitkIm.GetDirection())
    return outSitkIm

def writeSitkIm(sitkIm, fn):
    """
    This function writes a sitk image to disk
    Args:
        sitkIm: the sitk image to write
        fn: file name
    Return:
        None

    """
    writer = sitk.ImageFileWriter()
    writer.SetFileName(fn)
    writer.Execute(sitkIm)

    return

def isoSurf2VTK(verts, faces):
    """
    This function creates a polydata from numpy arrays

    Args:
        verts: vertice coordinates of the isosurface
        faces: connectivity
    Returns:
        poly: VTK polydata

    """
    vtkPts = vtk.vtkPoints()
    vtkPts.SetNumberOfPoints(verts.shape[0])
    for i in range(verts.shape[0]):
        vtkPts.SetPoint(i, verts[i,:])

    vtkCells = vtk.vtkCellArray()
    #vtkCells.SetNumberOfCells(faces.shape[0])
    for i in range(faces.shape[0]):
        if faces.shape[-1]==3:
            cell = vtk.vtkTriangle()
        else:
            raise ValueError('Inconsistent number of face id')
        for j in range(faces.shape[-1]):
            cell.GetPointIds().SetId(j, faces[i,j])

        vtkCells.InsertNextCell(cell)
    poly = vtk.vtkPolyData()
    poly.SetPoints(vtkPts)
    poly.SetPolys(vtkCells)
    def _fixNormals(poly):
        normAdj = vtk.vtkPolyDataNormals()
        normAdj.SetInputData(poly)
        normAdj.SplittingOff()
        normAdj.ConsistencyOn()
        normAdj.FlipNormalsOn()
        normAdj.Update()
        poly = normAdj.GetOutput()
        return poly

    poly = _fixNormals(poly)
    return poly

def writeVTKPolyData(poly, fn):
    """
    This function writes a vtk polydata to disk
    Args:
        poly: vtk polydata
        fn: file name
    Returns:
        None
    """
    
    print('Writing vtp with name:', fn)
    if (fn == ''):
        return 0

    _ , extension = os.path.splitext(fn)

    if extension == '.vtk':
        writer = vtk.vtkPolyDataWriter()
    elif extension == '.vtp':
        writer = vtk.vtkXMLPolyDataWriter()
    else:
        raise ValueError("Incorrect extension"+extension)
    writer.SetInputData(poly)
    writer.SetFileName(fn)
    writer.Update()
    writer.Write()
    return

def writeVTKImage(vtkIm, fn):
    """
    This function writes a vtk image to disk
    Args:
        vtkIm: the vtk image to write
        fn: file name
    Returns:
        None
    """
    print("Writing vti with name: ", fn)

    _, extension = os.path.splitext(fn)
    if extension == '.vti':
        writer = vtk.vtkXMLImageDataWriter()
    elif extension == '.mhd':
        writer = vtk.vtkMetaImageWriter()
    else:
        raise ValueError("Incorrect extension " + extension)
    writer.SetInputData(vtkIm)
    writer.SetFileName(fn)
    writer.Update()
    writer.Write()
    return

def exportSitk2VTK(sitkIm):
    """
    This function creates a vtk image from a simple itk image

    Args:
        sitkIm: simple itk image
    Returns:
        imageData: vtk image
    """
    img = sitk.GetArrayFromImage(sitkIm)
    
    from vtk.util.numpy_support import numpy_to_vtk, get_vtk_array_type
    
    vtkArray = numpy_to_vtk(num_array=img.flatten('F'), deep=True,
                                        array_type=get_vtk_array_type(img.dtype))
    imageData = vtk.vtkImageData()
    imageData.SetOrigin(sitkIm.GetOrigin())
    imageData.SetSpacing(sitkIm.GetSpacing())
    imageData.SetDimensions(img.shape)
    imageData.GetPointData().SetScalars(vtkArray)
    
    return imageData
