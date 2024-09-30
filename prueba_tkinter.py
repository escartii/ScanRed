import tkinter as tk

# Crear la ventana principal de Tkinter
ventana = tk.Tk()
ventana.title("Prueba de Ventana Gráfica")
ventana.geometry("400x300")

# Crear un botón de ejemplo
boton = tk.Button(ventana, text="Cerrar", command=ventana.quit)
boton.pack(pady=20)

# Ejecutar el bucle principal de Tkinter
ventana.mainloop()
