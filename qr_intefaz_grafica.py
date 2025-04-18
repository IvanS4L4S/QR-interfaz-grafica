import tkinter as tk
from tkinter import filedialog, messagebox
import qrcode 
from PIL import Image, ImageTk #libreria para generar una imagen dentro del qr
from qrcode.image.pil import PilImage
import os, sys


#ruta absoluta de las imagnes utilizadas, nesarias para evitar problemas 
# al momento de genrar un .exe por la ubicacion de las imagenes
def ruta_absoluta(nombre_archivo):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, nombre_archivo)

# Metodo para que funciones de copiar, cortar y pegar en el entry
def mostrar_menu_contextual(event, entry_widget):
    menu = tk.Menu(ventana, tearoff=0)
    menu.add_command(label="Cortar", command=lambda: entry_widget.event_generate("<<Cut>>"))
    menu.add_command(label="Copiar", command=lambda: entry_widget.event_generate("<<Copy>>"))
    menu.add_command(label="Pegar", command=lambda: entry_widget.event_generate("<<Paste>>"))
    menu.tk_popup(event.x_root, event.y_root)



# Creacion del procedimiento
def generar_qr():
    data=entrada.get()
    if not data:
        messagebox.showwarning("Ojito","Mi estimad@ ingrese URL o texto")
        return


    # Crear el objeto QR, quie se encuenta el tamaño y el borde de la misma
    qr = qrcode.QRCode(version=1,box_size=10,border=5)

    # Agregar la data
    qr.add_data(data)
    qr.make(fit=True)



    # Generar la imagen con colores por defecto es negro y blanco
    #img = qr.make_image(fill_color='black', back_color='white')
    img = qr.make_image(image_factory=PilImage, fill_color='black', back_color='white').convert("RGBA")






    # Insertar LOGO en el centro del QR
    try:
        logo = Image.open(ruta_absoluta("centroQR.png")).convert("RGBA")
        logo = logo.resize((40, 70))
        pos = ((img.size[0] - logo.size[0]) // 2, (img.size[1] - logo.size[1]) // 2)
        img.paste(logo, pos, mask=logo)  # Usamos el canal alfa si lo tiene
    except FileNotFoundError:
        messagebox.showwarning("Logo no encontrado", "No se encontró 'logo.png'. Se guardará sin logo.")



    # Guardar la imagen de tipo png y donde se eligira ubicación 
    tipo_archivo=filedialog.asksaveasfilename(defaultextension=".png",filetypes=[("PNG files","*.png")])
    if tipo_archivo:
        img.save(tipo_archivo)
        messagebox.showinfo("Gracias",f"codigo QR guardado en :\n{tipo_archivo}")
        entrada.delete(0,tk.END) # limpia contenido del label
        

# Interfaz grafica principal
ventana=tk.Tk()
ventana.configure(bg="#E9E5CC")  # cambia color de fondo general
ventana.iconbitmap(ruta_absoluta("icono.ico"))

ventana.title("QR JUJUY")
ventana.geometry("400x350")#tamaño de la ventana general

#centrara la intefaz en el centro
ventana.update_idletasks()
ancho = ventana.winfo_width()
alto = ventana.winfo_height()
x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
y = (ventana.winfo_screenheight() // 2) - (alto // 2)
ventana.geometry(f"+{x}+{y}")



# Entrada de datos
tk.Label(ventana,text="Ingrese URL o TEXTO", bg="#E9E5CC", font=("Arial", 12, "bold")).pack(pady=5)

# Cargar imagen (asegúrate que el archivo esté en la misma carpeta o pon la ruta completa)
imagen = Image.open(ruta_absoluta("image.png"))  # Reemplaza con el nombre de tu imagen
imagen = imagen.resize((250, 237))  # Tamaño deseado
imagen_tk = ImageTk.PhotoImage(imagen)
label_imagen = tk.Label(ventana, image=imagen_tk, bg="#E9E5CC")
label_imagen.pack(pady=0)


entrada=tk.Entry(ventana,width=34,font=("Courier", 12))
entrada.pack(pady=5)

# Habilitar clic derecho con las opciones de copiar, pegar y cortar
entrada.bind("<Button-3>", lambda event: mostrar_menu_contextual(event, entrada))

# Botón que generara y guardara nuestro QR.png
tk.Button(ventana,text="crear",command=generar_qr,bg="#9E371D").pack(pady=5)

#raiz
ventana.mainloop()