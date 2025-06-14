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

    def trasladar_imagen(self, index=0, dx=10, dy=10):
        if index < 0 or index >= len(self.slices):
            raise IndexError("El indice está fuera de rango de cortes DICOM.")

        img = self.slices[index].pixel_array

        if img.dtype != np.uint8:
            img = cv2.convertScaleAbs(img, alpha=(255.0 / np.max(img)))

        row, col = img.shape[:2]
        MT = np.float32([[1, 0, dx], [0, 1, dy]])
        trasladada = cv2.warpAffine(img, MT, (col, row))

        return img, trasladada

class ImagenHandler:
    def binarizar(imagen, tipo='BINARIO', umbral=127):
        tipos = {
            'BINARIO': cv2.THRESH_BINARY,
            'BINARIO_INV': cv2.THRESH_BINARY_INV,
            'TRUNCADO': cv2.THRESH_TRUNC,
            'TOZERO': cv2.THRESH_TOZERO,
            'TOZERO_INV': cv2.THRESH_TOZERO_INV
        }
        tipo = tipo.strip().upper()
        if tipo not in tipos:
            raise ValueError(f"El tipo de binarización es inválido: {tipo}")
        _, resultado = cv2.threshold(imagen, umbral, 255, tipos[tipo])
        return resultado
    
    def morfologia(imagen, operacion='CIERRE', kernel_size=3):
        ops = {
            'EROSION': cv2.MORPH_ERODE,
            'DILATACION': cv2.MORPH_DILATE,
            'APERTURA': cv2.MORPH_OPEN,
            'CIERRE': cv2.MORPH_CLOSE
        }
        operacion = operacion.strip().upper()
        if operacion not in ops:
            raise ValueError(f"La operación morfológica es inválida: {operacion}")
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        return cv2.morphologyEx(imagen, ops[operacion], kernel)