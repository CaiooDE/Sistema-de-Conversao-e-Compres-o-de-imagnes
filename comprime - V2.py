from PIL import Image
import os
import tkinter as tk
from tkinter import filedialog
import subprocess
import sys

def install_dependencies():
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "Pillow"])
    except Exception as e:
        print(f"Erro ao instalar dependências: {e}")

def compress_to_1mb(folder_path, log_text):
    if not os.path.exists(folder_path):
        log_text.configure(state='normal')
        log_text.insert(tk.END, f'O diretório {folder_path} não existe.\n')
        log_text.configure(state='disabled')
        return

    files = os.listdir(folder_path)

    for file_name in files:
        if file_name.lower().endswith('.jpg') or file_name.lower().endswith('.jpeg'):
            image_path = os.path.join(folder_path, file_name)
            log_text.configure(state='normal')
            log_text.insert(tk.END, f'Comprimindo {file_name}...\n')
            log_text.see(tk.END)

            # Inicializa a qualidade da imagem como 20
            quality = 20

            # Loop para ajustar a qualidade até que o tamanho seja inferior a 1 MB
            while True:
                img = Image.open(image_path)
                img.save(image_path, optimize=True, quality=quality)

                # Verifica o tamanho do arquivo
                file_size_mb = os.path.getsize(image_path) / (1024 * 1024)  # Tamanho em MB

                if file_size_mb < 1:
                    log_text.insert(tk.END, f'{file_name} comprimido com sucesso para {file_size_mb:.2f} MB\n')
                    log_text.see(tk.END)
                    break

                # Aumenta a qualidade para reduzir o tamanho do arquivo
                quality -= 5

    log_text.configure(state='disabled')

def browse_button():
    folder_path = filedialog.askdirectory()
    path_entry.delete(0, tk.END)
    path_entry.insert(tk.END, folder_path)

def compress_images():
    install_dependencies()
    folder_path = path_entry.get()
    log_text.configure(state='normal')
    log_text.delete(1.0, tk.END)
    log_text.insert(tk.END, f'Comprimindo imagens para até 1MB no diretório: {folder_path}\n')
    log_text.configure(state='disabled')
    compress_to_1mb(folder_path, log_text)

root = tk.Tk()
root.title("Compressor de Imagens")

frame = tk.Frame(root)
frame.pack(padx=20, pady=20)

path_label = tk.Label(frame, text="Caminho do Diretório:")
path_label.grid(row=0, column=0, sticky="w")

path_entry = tk.Entry(frame, width=40)
path_entry.grid(row=0, column=1)

browse_button = tk.Button(frame, text="Navegar", command=browse_button)
browse_button.grid(row=0, column=2, padx=5)

compress_button = tk.Button(frame, text="Comprimir", command=compress_images)
compress_button.grid(row=1, columnspan=3, pady=10)

log_text = tk.Text(frame, height=10, width=50)
log_text.grid(row=2, columnspan=3, pady=10)

root.mainloop()
