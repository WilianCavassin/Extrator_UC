# Importações de bibliotecas

import os
import sys
import tkinter as tk
import functions
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox as mbox


root = tk.Tk()
root.title('Extrator de Casos de Uso (v0.2)')
root.resizable(False, False)
root.geometry('640x480')
text = tk.Text(root, height=26)
text.pack(side='top', anchor='nw', fill='both', expand='yes')
string_list = []
return_list = []
file_name = ''
file_path = ''
filetypes = {
    ('text files', '*.txt')
    }
integer_number_lines = 0

string_begin = '---BEM VINDO AO EXTRATOR DE CASOS DE USO V0.2---\n\
    \tPara começar o processamento, escolha um arquivo abaixo.\n\n\
    \tAs funções da aplicação são as seguintes:\n\
    \t-Selecione um arquivo: Carrega um arquivo no sistema e o exibe na tela;\n\
    \t-Limpar a tela: Retira o arquivo que fora processado anteriormente;\n\
    \t-Processar o arquivo: Gera os diagramas de casos de uso\n\
    \t para as User Stories selecionadas.\n\
    \n\
    Recomenda-se o uso máximo de 10 User Stories por diagrama.'
string_start = 'ARQUIVO CARREGADO:\n'

text.insert('1.0',string_begin)
text.config(state='disabled')

def open_text_file():
    global string_list
    global return_list
    global file_name
    global file_path
    
    f = fd.askopenfile(filetypes=filetypes)
    file_path = os.path.abspath(f.name)
    file_name = os.path.basename(f.name)
    string_list = f.readlines()
    
    # Chama o verificador de arquivo
    return_validate = functions.validate_file(string_list)
    return_type = return_validate[0]
    return_string = return_validate[1]
    return_list = return_validate[2]
    if return_type == 2:
        mbox.showinfo('Informação',return_string)
    if return_type == 1:
        mbox.showwarning('Alerta',return_string)
    if return_type == 0:
        mbox.showerror('Erro',return_string)
    return_list.insert(0,string_start)
    print(return_list)
    print(type(return_list))
    text.config(state='normal')
    text.delete('1.0','end')
    text.insert('1.0', return_list)
    text.replace("1.0", tk.END, text.get("1.0", tk.END).replace(' {', '-> ').replace('}','').replace('{',''))
    text.config(state='disabled')
    

def clear_text_file():
    global string_list
    global file_name
    global file_path
    global integer_number_lines
    string_list = ''
    file_name = ''
    file_path = ''
    integer_number_lines = 0
    text.config(state='normal')
    text.delete('1.0','end')
    text.insert('1.0',string_begin)
    text.config(state='disabled')

def process_text_file():
    global return_list
    print('String que será passada para a função:\n')
    print(len(return_list))
    print(return_list)
    return_list.pop(0)
    xmi_file_content = functions.processData(return_list,file_name)
    xmi_file_name = fd.asksaveasfilename(initialdir='',title='Salvar Arquivo XMI',filetypes=(('XMI Files','*.xmi'),('Todos os Arquivos','*.*')))
    print(xmi_file_name)
    if xmi_file_name == '.xmi' or xmi_file_name == '':
        mbox.showerror('Erro','A aplicação encontrou um erro e será encerrada.\nErro: Ponto de Salvamento Inválido.')
        sys.exit()
    #controle de tipagem de arquivo
    if not xmi_file_name.endswith('.xmi'):
        xmi_file_name += '.xmi'
    if xmi_file_name.endswith('.xmi.xmi'):
        xmi_file_name = xmi_file_name[:-4]
    with open(xmi_file_name,'w', newline='\n') as xmi_file_name_open:
        xmi_file_name_open.write(xmi_file_content)
    text.insert('1.0', string_list)
    print(string_list)
    mbox.showinfo('Sucesso','Diagrama gravado com sucesso.')

open_button = ttk.Button(
    root,
    text='Selecione um arquivo',
    command=open_text_file
)
open_button.pack(side='left',expand='yes',fill='both')
clear_button = ttk.Button(
    root,
    text='Limpar a tela',
    command = clear_text_file
)
clear_button.pack(side='left',expand='yes',fill='both')
process_button = ttk.Button(
    root,
    text='Processar o arquivo',
    command=process_text_file
)
process_button.pack(side='left',expand='yes',fill='both')
root.lift()
root.attributes('-topmost',True)
root.after_idle(root.attributes,'-topmost',False)
root.mainloop()