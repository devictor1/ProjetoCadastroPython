# 1º Passo: Importar as bibliotecas necessárias
import mysql.connector
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import *

# 2º Passo: Estabelecer a conexão com o banco de dados com a função de conexão MySQL
def conectar_bd():
    return mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='root',
    database='cadastro1'
)
# Adições para melhor usabilidade
# Placeholders para os campos de entrada

# Placeholder para Nome
def focusInNome(event):
    # Função para esconder o placeholder quando o campo de entrada está em foco.
    if entry_nome.get() == 'Nome Sobrenome': # se estiver com o placeholder 
        entry_nome.delete(0, tk.END)  # Limpa o campo
        entry_nome.config(fg='black')  # Restaura a cor do texto
def focusOutNome(event):
    #Função para mostrar o placeholder quando o campo de entrada está vazio.
    if entry_nome.get() == '': # se estiver vazio
        entry_nome.insert(0, 'Nome Sobrenome') # placeholder
        entry_nome.config(fg='grey') # Cor do texto do placeholder

# Placeholder para Data de Nascimento
def focusInDataNascimento(event):
    # Função para esconder o placeholder quando o campo de entrada está em foco.
    if entry_dataNascimento.get() == 'AAAA/MM/DD':
        entry_dataNascimento.delete(0, tk.END)  # Limpa o campo
        entry_dataNascimento.config(fg='black')  # Restaura a cor do texto
def focusOutDataNascimento(event):
    #Função para mostrar o placeholder quando o campo de entrada está vazio.
    if entry_dataNascimento.get() == '':
        entry_dataNascimento.insert(0, 'AAAA/MM/DD') # placeholder
        entry_dataNascimento.config(fg='grey') # Cor do texto do placeholder

# Placeholder para Email
def focusInEmail(event):
    # Função para esconder o placeholder quando o campo de entrada está em foco.
    if entry_email.get() == 'exemplo@dominio.com':
        entry_email.delete(0, tk.END)  # Limpa o campo
        entry_email.config(fg='black')  # Restaura a cor do texto
def focusOutEmail(event):
    #Função para mostrar o placeholder quando o campo de entrada está vazio.
    if entry_email.get() == '':
        entry_email.insert(0, 'exemplo@dominio.com') # placeholder
        entry_email.config(fg='grey') # Cor do texto do placeholder

# Placeholder para Telefone
def focusInTelefone(event):
    # Função para esconder o placeholder quando o campo de entrada está em foco.
    if entry_telefone.get() == '(XX)9XXXX-XXXX/(XX)XXXX-XXXX': # se estiver com o placeholder 
        entry_telefone.delete(0, tk.END)  # Limpa o campo
        entry_telefone.config(fg='black')  # Restaura a cor do texto
def focusOutTelefone(event):
    #Função para mostrar o placeholder quando o campo de entrada está vazio.
    if entry_telefone.get() == '': # se estiver vazio
        entry_telefone.insert(0, '(XX)9XXXX-XXXX/(XX)XXXX-XXXX') # placeholder
        entry_telefone.config(fg='grey') # Cor do texto do placeholder

# Formatação do telefone
def formatar_telefone_input(event):
     # Remove todos os caracteres não numéricos
    telefone = ''.join(filter(str.isdigit, entry_telefone.get()))
    
    # Formatação do telefone
    if len(telefone) > 11:
        telefone = telefone[:11]  # Limita a 11 dígitos
    if len(telefone) >= 6:  # (XX) XXXXX-XXXX
        telefone_formatado = f"({telefone[:2]}) {telefone[2:7]}-{telefone[7:]}"
    elif len(telefone) >= 3:  # (XX) XXXX-XXXX
        telefone_formatado = f"({telefone[:2]}) {telefone[2:6]}-{telefone[6:]}"
    elif len(telefone) >= 2:  # (XX)
        telefone_formatado = f"({telefone[:2]}) {telefone[2:]}"
    elif len(telefone) >= 1:  # (X)
        telefone_formatado = f"({telefone[:2]})"
    else:  # vazio
        telefone_formatado = ''
    
    entry_telefone.delete(0, tk.END)  # Limpa o campo
    entry_telefone.insert(0, telefone_formatado)  # Insere o telefone formatado


# 3º Passo: Criar a função de cadastro de usuario
def cadastrar():

# 4º Passo: Preparar os campos de entrada
    nome = entry_nome.get() # recebe o nome
    dataNascimento = entry_dataNascimento.get() # recebe a data de nascimento
    email = entry_email.get() # recebe o email
    telefone =  entry_telefone.get() # recebe o telefone

    telefone_limpo = ''.join(filter(str.isdigit, telefone)) # remove a formatação antes de guardar o valor
    telefone = telefone_limpo
    conexao = conectar_bd()
    cursor = conexao.cursor()

# 5º Passo: Executar a query de cadastro
    dados = (nome, dataNascimento, email, telefone)
    cursor.execute("INSERT INTO usuarios (nome, dataNascimento, email, telefone) VALUES (%s,%s,%s,%s)", dados)

 # 6º Passo: Confirmar o cadastro
    conexao.commit()
    conexao.close()

# 7º Passo: Mostrar mensagem de sucesso
    messagebox.showinfo("Sucesso!", "Cadastro realizado com sucesso!")

# 8º Passo: Limpar os campos de entrada
    limparCampos()

# 9º Passo: Função para mostrar todos os registros
def mostrar_todos():
    tree.delete(*tree.get_children()) # limpa os registros mostrados anteriormente
    conexao = conectar_bd() # conectar com o Banco de Dados
    cursor = conexao.cursor() # criar um cursor que executa os comandos MySQL
    cursor.execute("select * from usuarios") # execução do comando
    registros = cursor.fetchall() # coletar todos os registros
    for registro in registros:
        tree.insert('', 'end', values=registro)
    conexao.close() # fechar conexão

# 10º Passo: Função para edição de registros
def selecionar_registro(event):
    print(f"Registro selecionado")  # Debug
    selected_item = tree.selection()  # Selecionar o registro
    if selected_item:  # Verifica se algum item está selecionado
        registro = tree.item(selected_item)['values']  # Coletar os valores do registro
        entry_nome.delete(0, tk.END)
        entry_nome.insert(0, registro[1])  # Nome
        entry_dataNascimento.delete(0, tk.END)
        entry_dataNascimento.insert(0, registro[2])  # Data de Nascimento
        entry_email.delete(0, tk.END)
        entry_email.insert(0, registro[3])  # E-mail
        entry_telefone.delete(0, tk.END)
        entry_telefone.insert(0, registro[4])  # Telefone

def editar():
    selected_item = tree.selection() # selecionar usuario
    if not selected_item:  # Verifica se algum item está selecionado
        messagebox.showwarning("Atenção!", "Nenhum registro selecionado para editar.")
        return
    id_usuario = tree.item(selected_item)['values'][0] # coletar a ID do usuário escolhido
    nome = entry_nome.get() # coletar nome do usuário
    dataNascimento = entry_dataNascimento.get() # coletar data de nascimento
    email = entry_email.get() # coletar e-mail
    telefone =  entry_telefone.get() #coletar telefone    
    conexao =  conectar_bd() # conectar com o Banco de Dados
    cursor = conexao.cursor() # criar um cursor que executa os comandos MySQL
    dados = (nome, dataNascimento, email, telefone, id_usuario) # coletando os dados
    cursor.execute("UPDATE usuarios SET nome = %s, dataNascimento = %s, email = %s,  telefone = %s WHERE id = %s", dados) # criação do botão e sua localização
    conexao.commit() # confirmação da edição
    conexao.close() # fechamento da conexão
    messagebox.showinfo("Sucesso!","Registro atualizado com sucesso!") # mensagem confirmando a alteração
    limparCampos() # chamando função que limpa os campos de entrada usados
    mostrar_todos()

# 11º Passo: Função para excluir registros
def excluir():
    selected_item = tree.selection()[0] # selecionar usuario
    id_usuario = tree.item(selected_item)['values'][0] # coletar a ID do usuário escolhido
    conexao = conectar_bd()# conectar com o Banco de Dados
    cursor = conexao.cursor() # criar um cursor que executa os comandos MySQL
    cursor.execute("DELETE FROM usuarios WHERE id = %s", (id_usuario,)) # executando o script SQL
    conexao.commit() # confirmação da edição
    conexao.close() # fechamento da conexão
    tree.delete(selected_item) # deletar o registro selecionado
    messagebox.showinfo("Sucesso!","Registro excluido com sucesso!") # mensagem confirmando a exclusão
    limparCampos() # chamando função que limpa os campos de entrada usados

# 12º Passo: Função para limpar os campos de entrada
def limparCampos():
    entry_nome.delete(0, tk.END) # limpar campo de nome
    entry_dataNascimento.delete(0, tk.END) # limpar campo de data
    entry_email.delete(0, tk.END) # limpar campo de email
    entry_telefone.delete(0, tk.END) # limpar campo de telefone

#  13º Passo: Gerar interface TKinter
root = tk.Tk() # criação da janela
root.title("Cadastro de Usuários") # título da janela

tk.Label(root, text="Nome").grid(row=0, column=1) # label para nome
entry_nome = tk.Entry(root, width=30) # campo de entrada
entry_nome.grid(row=0, column=2) # localização do campo de entrada
entry_nome.bind('<FocusIn>', focusInNome)
entry_nome.bind('<FocusOut>', focusOutNome)
entry_nome.insert(0, 'Nome Sobrenome')
entry_nome.config(fg='grey')

tk.Label(root, text="Data de Nascimento").grid(row=1, column=1)  # label para data de nascimento
entry_dataNascimento = tk.Entry(root, width=30) # campo de entrada
entry_dataNascimento.grid(row=1, column=2) # localização do campo de entrada
entry_dataNascimento.bind('<FocusIn>', focusInDataNascimento)
entry_dataNascimento.bind('<FocusOut>', focusOutDataNascimento)
entry_dataNascimento.insert(0, 'AAAA/MM/DD')
entry_dataNascimento.config(fg='grey')

tk.Label(root, text="E-mail").grid(row=2, column=1) # label para e-mail
entry_email = tk.Entry(root, width=30) # campo de entrada
entry_email.grid(row=2, column=2) # localização do campo de entrada
entry_email.bind('<FocusIn>', focusInEmail)
entry_email.bind('<FocusOut>', focusOutEmail)
entry_email.insert(0, 'exemplo@dominio.com')
entry_email.config(fg='grey')

tk.Label(root, text="Telefone").grid(row=3, column=1) # label para telefone
entry_telefone = tk.Entry(root, width=30) # campo de entrada
entry_telefone.grid(row=3, column=2) # localização do campo de entrada
entry_telefone.bind('<FocusIn>', focusInTelefone)
entry_telefone.bind('<FocusOut>', focusOutTelefone)
entry_telefone.insert(0, '(XX)9XXXX-XXXX/(XX)XXXX-XXXX')
entry_telefone.config(fg='grey')
entry_telefone.bind('<KeyRelease>', formatar_telefone_input) # formatação do telefone

#  14º Passo: Botões para realizar as ações
tk.Button(root, text="Cadastrar", command=cadastrar).grid(row=4, column=0, pady=10) # criação do botão de cadastro e sua localização na grid
tk.Button(root, text="Mostrar Todos", command=mostrar_todos).grid(row=4, column=1, pady=10) # criação do botão de mostrar todos e sua localização na grid
tk.Button(root, text="Editar", command=editar).grid(row=4, column=2, pady=10) # criação do botão de edição e sua localização na grid
tk.Button(root, text="Excluir", command=excluir).grid(row=4, column=3, pady=10) # criação do botão de exclusão e sua localização na grid

# 15º Passo: Criar a tabela de usuários
columns = ("ID", "Nome", "Data de Nascimento", "E-mail", "Telefone") # definindo as colunas
tree = ttk.Treeview(root, columns=columns, show="headings") # criando a tabela com as colunas definidas
for col in columns: # criando as colunas
    tree.heading(col, text=col) # definindo seus nomes
tree.grid(row=6, column=0, columnspan=4) # definindo a grid
tree.bind('<<TreeviewSelect>>', selecionar_registro) # seleciona registro sempre que clica em um na grid

root.mainloop() # iniciando a janela