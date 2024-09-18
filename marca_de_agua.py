import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk, ImageDraw, ImageFont

# Función para remover marca de agua
def remover_marca(image_path, output_path):
    img = cv2.imread(image_path)
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    rojo_bajo1 = np.array([0, 50, 50])
    rojo_alto1 = np.array([10, 255, 255])
    rojo_bajo2 = np.array([160, 50, 50])
    rojo_alto2 = np.array([180, 255, 255])
    
    mask1 = cv2.inRange(img_hsv, rojo_bajo1, rojo_alto1)
    mask2 = cv2.inRange(img_hsv, rojo_bajo2, rojo_alto2)
    mask = mask1 | mask2
    
    resultado = cv2.inpaint(img, mask, inpaintRadius=3, flags=cv2.INPAINT_TELEA)
    cv2.imwrite(output_path, resultado)

# Funciones para la interfaz gráfica
def cargar_imagen():
    global imagen, imagen_cv, image_path
    image_path = filedialog.askopenfilename(filetypes=[("Archivos de imagen", "*.jpg;*.jpeg;*.png")])
    if image_path:
        imagen_cv = cv2.imread(image_path)
        imagen = Image.fromarray(cv2.cvtColor(imagen_cv, cv2.COLOR_BGR2RGB))
        mostrar_imagen(imagen)

def mostrar_imagen(imagen):
    imagen.thumbnail((400, 400)) 
    imagen_tk = ImageTk.PhotoImage(imagen)
    label_img.config(image=imagen_tk)
    label_img.image = imagen_tk

def aplicar_remover_marca():
    global imagen_cv, image_path
    if imagen_cv is not None:
        try:
            output_path = "output_image.jpg"
            remover_marca(image_path, output_path)
            
            # Cargar y mostrar la imagen sin marca de agua
            imagen_resultante = Image.open(output_path)
            mostrar_imagen(imagen_resultante)
            messagebox.showinfo("Éxito", "La marca de agua ha sido removida correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")
    else:
        messagebox.showwarning("Advertencia", "Primero debes cargar una imagen.")

def agregar_marca_de_agua():
    global imagen
    if imagen:
        try:
            opcion = simpledialog.askstring("Agregar Marca de Agua", "¿Texto o Imagen?")
            
            if opcion.lower() == "texto":
                texto = simpledialog.askstring("Texto", "Escribe el texto para la marca de agua:")
                font_size = simpledialog.askinteger("Tamaño de fuente", "Introduce el tamaño de la fuente (ej. 30):", initialvalue=30)
                
                # Creamos el objeto para dibujar sobre la imagen
                draw = ImageDraw.Draw(imagen)
                font = ImageFont.truetype("arial.ttf", font_size)
                
                posicion_x = simpledialog.askinteger("Posición X", "Introduce la posición X de la marca de agua:", initialvalue=10)
                posicion_y = simpledialog.askinteger("Posición Y", "Introduce la posición Y de la marca de agua:", initialvalue=10)
                
                draw.text((posicion_x, posicion_y), texto, fill=(255, 255, 255), font=font)
                
                mostrar_imagen(imagen)
            
            elif opcion.lower() == "imagen":

                marca_path = filedialog.askopenfilename(filetypes=[("Archivos de imagen", "*.png;*.jpg")])
                if marca_path:
                    marca = Image.open(marca_path)
                    
                    # Verificamos si tiene canal alfa, si no lo tiene, añadimos uno
                    if marca.mode != 'RGBA':
                        marca = marca.convert("RGB")
                        alpha = Image.new('L', marca.size, 255)
                        marca.putalpha(alpha)
                    
                    marca = marca.resize((100, 100)) 
                    
                    posicion_x = simpledialog.askinteger("Posición X", "Introduce la posición X de la marca de agua:", initialvalue=10)
                    posicion_y = simpledialog.askinteger("Posición Y", "Introduce la posición Y de la marca de agua:", initialvalue=10)
                    
                    imagen.paste(marca, (posicion_x, posicion_y), marca)
                    

                    mostrar_imagen(imagen)
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al agregar la marca de agua: {e}")
    else:
        messagebox.showwarning("Advertencia", "Primero debes cargar una imagen.")

def guardar_imagen():
    global imagen
    if imagen:
        file_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png")])
        if file_path:
            imagen.save(file_path)
            messagebox.showinfo("Guardar Imagen", "Imagen guardada correctamente.")
    else:
        messagebox.showwarning("Advertencia", "Primero debes cargar una imagen.")

# Configuración de la interfaz gráfica 
ventana = tk.Tk()
ventana.title("Editor de Marca de Agua")

label_img = tk.Label(ventana)
label_img.pack()


frame_botones = tk.Frame(ventana)
frame_botones.pack(pady=20)

boton_cargar = tk.Button(frame_botones, text="Cargar Imagen", command=cargar_imagen)
boton_cargar.pack(side=tk.LEFT, padx=10)

boton_remover_marca = tk.Button(frame_botones, text="Remover Marca de Agua", command=aplicar_remover_marca)
boton_remover_marca.pack(side=tk.LEFT, padx=10)

boton_agregar_marca = tk.Button(frame_botones, text="Agregar Marca de Agua", command=agregar_marca_de_agua)
boton_agregar_marca.pack(side=tk.LEFT, padx=10)

boton_guardar = tk.Button(frame_botones, text="Guardar Imagen", command=guardar_imagen)
boton_guardar.pack(side=tk.LEFT, padx=10)

ventana.mainloop()
