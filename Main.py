from Clases import Paciente, DicomHandler, ImagenHandler
import matplotlib.pyplot as plt
import cv2
import numpy as np

pacientes = {}
archivos_dicom = {}
archivos_imagenes = {}

def menu():
    while True:
        print("\nMenú Principal \n a. Cargar carpeta DICOM \n b) Crear paciente \n c) Cargar imagen JPG/PNG \n d) Trasladar imagen DICOM" \
        "\n e) Procesar imagen JPG/PNG \n f) Salir")
        op = input("Opción: ").lower() 
        
        if op == 'a':
            try:
                ruta = input("Ruta de carpeta DICOM: ").strip()
                clave = input("Clave para guardar: ").strip()
                gestor = DicomHandler(ruta)
                gestor.mostrar_cortes()
                archivos_dicom[clave] = gestor
            except Exception as e:
                print(f"Se presentó un error al intentar cargar DICOM: {e}"

        
