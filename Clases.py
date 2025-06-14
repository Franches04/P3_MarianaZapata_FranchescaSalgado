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
    
    def reconstruir_3D(self):
        return np.stack([s.pixel_array for s in self.slices])

    def obtener_info_paciente(self):
        ds = self.slices[0]
        nombre = str(getattr(ds, 'PatientName', 'Anonimo'))
        edad = str(getattr(ds, 'PatientAge', '000'))
        ID = str(getattr(ds, 'PatientID', '0000'))
        return nombre, edad, ID
    
    def mostrar_cortes(self):
        volumen = self.image_3d
        z, y, x = volumen.shape

        def preparar_img(img):
            if img.dtype != np.uint8:
                return cv2.convertScaleAbs(img, alpha=(255.0 / img.max()))
            return img

        plt.figure(figsize=(12, 4))

        plt.subplot(131)
        plt.imshow(preparar_img(volumen[:, :, x // 2]), cmap='gray')
        plt.title("Coronal")

        plt.subplot(132)
        plt.imshow(preparar_img(volumen[z // 2, :, :]), cmap='gray')
        plt.title("Sagital")

        plt.subplot(133)
        plt.imshow(preparar_img(volumen[:, y // 2, :]), cmap='gray')
        plt.title("Transversal")

        plt.tight_layout()
        plt.show()