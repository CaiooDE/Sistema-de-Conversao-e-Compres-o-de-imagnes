import os
import subprocess
import sys
import tkinter as tk
from tkinter import filedialog, messagebox

def install_dependencies():
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "Pillow"])
        subprocess.run([sys.executable, "-m", "pip", "install", "pyheif"])
    except Exception as e:
        print(f"Erro ao instalar dependências: {e}")

def convert_heic_to_jpg(folder_path, log_text):
    if not os.path.exists(folder_path):
        messagebox.showerror("Erro", f"O diretório {folder_path} não existe.")
        return

    files = os.listdir(folder_path)

    for file_name in files:
        if file_name.lower().endswith('.heic'):
            heic_file = os.path.join(folder_path, file_name)
            log_text.configure(state='normal')  # Habilita para inserir texto
            log_text.insert(tk.END, f'Convertendo {heic_file} para JPG...\n')
            log_text.configure(state='disabled')  # Desabilita edição novamente

            # Chama o imagemagick para converter HEIC para JPG
            jpg_file = os.path.splitext(heic_file)[0] + '.jpg'
            subprocess.run(['magick', heic_file, jpg_file])

            log_text.configure(state='normal')  # Habilita para inserir texto
            log_text.insert(tk.END, f'{file_name} convertido para {jpg_file}\n')
            log_text.see(tk.END)  # Mantém a visualização do log atualizada
            log_text.configure(state='disabled')  # Desabilita edição novamente

def browse_directory(log_text):
    folder_path = filedialog.askdirectory()
    if folder_path:
        convert_heic_to_jpg(folder_path, log_text)

def main():
    install_dependencies()

    root = tk.Tk()
    root.title("Conversor HEIC para JPG")

    label = tk.Label(root, text="Selecione o diretório das fotos HEIC:", font=("Arial", 12))
    label.pack(pady=10)

    browse_button = tk.Button(root, text="Escolher diretório", command=lambda: browse_directory(log), font=("Arial", 10))
    browse_button.pack(pady=5)

    log = tk.Text(root, height=10, width=50)
    log.pack(pady=10)
    log.configure(state='disabled')  # Impede a edição do log

    root.mainloop()

if __name__ == "__main__":
    main()
