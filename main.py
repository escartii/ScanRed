import nmap
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox
import netifaces as ni
import os
import pyperclip

# Función que obtiene el rango de IP de la red local
def obtener_rango_ip():
    interfaz = ni.gateways()['default'][ni.AF_INET][1]
    ip_info = ni.ifaddresses(interfaz)[ni.AF_INET][0]
    ip_local = ip_info['addr']
    mascara = ip_info['netmask']
    
    # Convertimos la IP y máscara en un formato de red
    ip_red = '.'.join(ip_local.split('.')[:3]) + '.0/24'
    return ip_red

# Variable global para almacenar las IPs
ip_list = []

# Función que ejecuta el escaneo con nmap
def escanear_red(rango_ip, text_widget):
    global ip_list
    ip_list = []  # Reiniciar la lista de IPs
    nm = nmap.PortScanner()
    nm.scan(hosts=rango_ip, arguments='-sn')  # Escaneo de ping

    # Mostrar resultados en tiempo real en la ventana
    for host in nm.all_hosts():
        if 'hostnames' in nm[host]:
            hostname = nm[host]['hostnames'][0]['name'] if nm[host]['hostnames'] else 'Desconocido'
            ip_list.append(host)  # Agregar IP a la lista
            text_widget.insert(tk.END, f"Equipo: {hostname} - IP: {host}\n")
        else:
            ip_list.append(host)  # Agregar IP a la lista
            text_widget.insert(tk.END, f"Equipo: Desconocido - IP: {host}\n")
        
        # Actualizar la ventana con los resultados
        text_widget.see(tk.END)  # Desplazar el texto hacia el final para ver las actualizaciones en tiempo real
    
    text_widget.insert(tk.END, "\nEscaneo completo.\n")
    text_widget.config(state=tk.DISABLED)  # Desactivar edición una vez que se muestra todo

# Función que muestra la pantalla de carga y luego ejecuta el escaneo
def iniciar_escaneo():
    rango_ip = obtener_rango_ip()
    text_widget.config(state=tk.NORMAL)  # Permitir la inserción de texto
    text_widget.delete(1.0, tk.END)  # Limpiar cualquier texto previo
    text_widget.insert(tk.END, f"Escaneando la red: {rango_ip}\n")
    text_widget.insert(tk.END, "... Estamos preparando todo para ti ...\n")
    
    # Iniciar el escaneo en un hilo separado
    hilo = threading.Thread(target=escanear_red, args=(rango_ip, text_widget))
    hilo.start()

# Función para copiar las IPs al portapapeles
def copiar_ips():
    if ip_list:
        ips_string = ", ".join(ip_list)  # Unir las IPs en una sola línea, separadas por comas
        pyperclip.copy(ips_string)  # Copiar al portapapeles
        messagebox.showinfo("Éxito", "Las IPs han sido copiadas al portapapeles.")
    else:
        messagebox.showwarning("Advertencia", "No se encontraron IPs para copiar.")


# Comprobar si Nmap está instalado
def verificar_nmap():
    if os.system("which nmap") != 0:
        print("Instalando Nmap...")
        os.system("sudo apt-get update && sudo apt-get install -y nmap")

# Verificar que Nmap esté instalado
verificar_nmap()

# Crear la ventana principal de Tkinter
ventana = tk.Tk()
ventana.title("Escaneo de Red")
ventana.geometry("500x400")

# Crear un widget de texto para mostrar los resultados
text_widget = scrolledtext.ScrolledText(ventana, wrap=tk.WORD, state=tk.DISABLED)
text_widget.pack(expand=True, fill='both')

# Botón para iniciar el escaneo
boton_escanear = tk.Button(ventana, text="Iniciar Escaneo", command=iniciar_escaneo)
boton_escanear.pack(pady=10)

# Botón para copiar las IPs
boton_copiar = tk.Button(ventana, text="Copiar IPs", command=copiar_ips)
boton_copiar.pack(pady=10)

# Ejecutar la aplicación de Tkinter
ventana.mainloop()
