import tkinter as tk
from tkinter import ttk
import secrets
import string
import csv
import datetime
import os

# Janela do app
root = tk.Tk()
root.title("Senhas Seguras")
root.resizable(False, False)

var_upper = tk.BooleanVar(value=True)
var_lower = tk.BooleanVar(value=True)
var_digits = tk.BooleanVar(value=True)
var_symbols = tk.BooleanVar(value=True)

upper_chars = string.ascii_uppercase
lower_chars = string.ascii_lowercase
digit_chars = string.digits
symbol_chars = string.punctuation

def gerar_senha():
    try:
        comprimento = int(entry_comprimento.get())
        if comprimento <= 0:
            raise ValueError
    except ValueError:
        atualizar_status("Comprimento inválido!", "red")
        return
    
    caracteres = []
    if var_upper.get(): caracteres.extend(upper_chars)
    if var_lower.get(): caracteres.extend(lower_chars)
    if var_digits.get(): caracteres.extend(digit_chars)
    if var_symbols.get(): caracteres.extend(symbol_chars)
    
    if not caracteres:
        atualizar_status("Selecione pelo menos um tipo de caractere!", "red")
        return
    
    senha = ''.join(secrets.choice(caracteres) for _ in range(comprimento))
    entry_senha.config(state='normal')
    entry_senha.delete(0, tk.END)
    entry_senha.insert(0, senha)
    entry_senha.config(state='readonly')
    atualizar_status("Senha gerada com sucesso!", "green")

def copiar_senha():
    senha = entry_senha.get()
    if senha:
        root.clipboard_clear()
        root.clipboard_append(senha)
        atualizar_status("Senha copiada para a área de transferência!", "blue")
    else:
        atualizar_status("Nenhuma senha para copiar!", "red")

def salvar_senha():
    senha = entry_senha.get()
    if not senha:
        atualizar_status("Gere uma senha antes de salvar!", "red")
        return
    
    data_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    arquivo_existe = os.path.isfile('senhas.csv')
    
    try:
        with open('senhas.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            if not arquivo_existe:
                writer.writerow(['Data/Hora', 'Senha'])
            writer.writerow([data_hora, senha])
        atualizar_status("Senha salva em senhas.csv!", "green")
    except Exception as e:
        atualizar_status(f"Erro ao salvar: {str(e)}", "red")

def atualizar_status(mensagem, cor):
    label_status.config(text=mensagem, fg=cor)
    root.after(5000, lambda: label_status.config(text=""))

# Interface Gráfica
frame_principal = ttk.Frame(root, padding=20)
frame_principal.pack()


ttk.Label(frame_principal, text="Comprimento da Senha:").grid(row=0, column=0, sticky='w', pady=2)
entry_comprimento = ttk.Entry(frame_principal, width=5)
entry_comprimento.grid(row=0, column=1, sticky='w', padx=5)
entry_comprimento.insert(0, "12")

# Escolher os caracteres
frame_opcoes = ttk.LabelFrame(frame_principal, text="Tipos de Caracteres")
frame_opcoes.grid(row=1, column=0, columnspan=2, pady=10, sticky='w')

ttk.Checkbutton(frame_opcoes, text="Letras Maiúsculas", variable=var_upper).pack(anchor='w')
ttk.Checkbutton(frame_opcoes, text="Letras Minúsculas", variable=var_lower).pack(anchor='w')
ttk.Checkbutton(frame_opcoes, text="Números", variable=var_digits).pack(anchor='w')
ttk.Checkbutton(frame_opcoes, text="Símbolos", variable=var_symbols).pack(anchor='w')

# Botão de gerar
ttk.Button(frame_principal, text="Gerar Senha", command=gerar_senha).grid(row=2, column=0, columnspan=2, pady=10)

# senha
entry_senha = ttk.Entry(frame_principal, width=30, font=('Arial', 10), state='readonly')
entry_senha.grid(row=3, column=0, columnspan=2, pady=5)


frame_botoes = ttk.Frame(frame_principal)
frame_botoes.grid(row=4, column=0, columnspan=2, pady=5)

ttk.Button(frame_botoes, text="Copiar Senha", command=copiar_senha).pack(side='left', padx=5)
ttk.Button(frame_botoes, text="Salvar em CSV", command=salvar_senha).pack(side='left', padx=5)

label_status = ttk.Label(frame_principal, text="", font=('Arial', 9))
label_status.grid(row=5, column=0, columnspan=2, pady=5)

root.mainloop()