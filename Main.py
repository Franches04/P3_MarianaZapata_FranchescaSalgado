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
                
        elif op == 'c':
            try:
                ruta = input("Ruta imagen JPG o PNG: ").strip()
                clave = input("Clave para guardar imagen: ").strip()
                img = cv2.imread(ruta)
                if img is None:
                    raise ValueError("No fue posible leer la imagen.")
                archivos_imagenes[clave] = img
                plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
                plt.title("Imagen cargada")
                plt.axis('off')
                plt.show()
            except Exception as e:
                print(f"Sucedió un error al cargar la imagen: {e}")
                
        elif op == 'd':
            print("\n Trasladar imagen DICOM cargada")
            clave = input("Clave DICOM: ").strip()
            if clave in archivos_dicom:
                handler = archivos_dicom[clave]
                try:
                    index = input("Índice del corte (Enter para usar 0): ")
                    index = int(index) if index.strip() != "" else 0

                    print("\nSelecciona una de las siguientes opciones para la dirección de traslación:")
                    print("1) dx=50, dy=0 (Se va a mover a la derecha)")
                    print("2) dx=-50, dy=0 (Se va a mover a la izquierda)")
                    print("3) dx=0, dy=-130 (Va a moverse hacia arriba)")
                    print("4) dx=0, dy=100 (Se moverá hacia abajo)")

                    opcion = input("¿Qué opción desea de 1 a 4?: ").strip()

                    if opcion == '1':
                        dx, dy = 50, 0
                    elif opcion == '2':
                        dx, dy = -50, 0
                    elif opcion == '3':
                        dx, dy = 0, -130
                    elif opcion == '4':
                        dx, dy = 0, 100
                    else:
                        print("La opción es inválida. Se usará dx=10 y dy=10 por defecto.")
                        dx, dy = 10, 10

                    original, trasladada = handler.trasladar_imagen(index=index, dx=dx, dy=dy)

                    fig, axs = plt.subplots(1, 2, figsize=(10, 4))
                    axs[0].imshow(original, cmap='gray')
                    axs[0].set_title("Original")
                    axs[1].imshow(trasladada, cmap='gray')
                    axs[1].set_title(f"Imagen Trasladada (dx={dx}, dy={dy})")
                    for ax in axs:
                        ax.axis('off')
                    plt.tight_layout()
                    plt.show()

                    nombre_archivo = f"trasladada_{clave}_dx{dx}_dy{dy}_index{index}.png"
                    cv2.imwrite(nombre_archivo, trasladada)
                    print(f"La imagen trasladada fue guardada como {nombre_archivo}")

                except Exception as e:
                    print(f"Hubo un error al trasladar la imagen: {e}")
            else:
                print("La clave no fue encontrada.")
        
        

        
