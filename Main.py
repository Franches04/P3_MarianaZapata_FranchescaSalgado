from Clases import Paciente, DicomHandler, ImagenHandler
import matplotlib.pyplot as plt
import cv2
import numpy as np

pacientes = {}
archivos_dicom = {}
archivos_imagenes = {}

def menu():
    while True:
        print("\nMenú Principal \n a). Cargar carpeta DICOM \n b) Crear paciente \n c) Cargar imagen JPG/PNG \n d) Trasladar imagen DICOM" \
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
                print(f"Se presentó un error al intentar cargar DICOM: {e}")
                
        elif op == 'b':
            clave = input("Clave del DICOM cargado: ").strip()
            if clave in archivos_dicom:
                try:
                    gestor = archivos_dicom[clave]
                    nombre, edad, ID = gestor.obtener_info_paciente()
                    paciente = Paciente(nombre, edad, ID, gestor.image_3d)
                    pacientes[ID] = paciente
                    print(f"El paciente fue registrado: {nombre}, Edad: {edad}, ID: {ID}")
                except Exception as e:
                    print(f"Ocurrió un error al crear paciente: {e}")
            else:
                print("La clave no se encontró. Primero se debe cargar el DICOM con la opción 'a' del menú.")

        
