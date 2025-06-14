import os
import cv2
import numpy as np
import pydicom
import matplotlib.pyplot as plt

pacientes = {}
archivos_dicom = {}
archivos_imagenes = {}
class Paciente:
    def __init__(self, nombre, edad, ID, imagen_3D):
        self.nombre = nombre
        self.edad = edad
        self.ID = ID
        self.imagen_3D = imagen_3D
class DicomHandler:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.slices = self.cargar_dicom()
        self.image_3d = self.reconstruir_3D()
    def cargar_dicom(self):
        dicoms = []
        for archivo in os.listdir(self.folder_path):
            if archivo.endswith(".dcm"):
                try:
                    dicom = pydicom.dcmread(os.path.join(self.folder_path, archivo))
                    dicoms.append(dicom)
                except:
                    pass
        dicoms.sort(key=lambda x: int(getattr(x, 'InstanceNumber', 0)))
        return dicoms