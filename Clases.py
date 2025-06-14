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