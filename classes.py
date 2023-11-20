import pandas as pd
import PySimpleGUI as sg
import os
import re
from babel.numbers import format_currency

class Usuario:
    @staticmethod
    def criar_tabela():
        # Cria a tabela de usuário se não existir
        if not os.path.exists('login.xlsx'):
            df = pd.DataFrame(columns=['Usuário', 'Senha'])
            df.to_excel('login.xlsx', index=False)

    @staticmethod
    def cadastrar_usuario(usuario, senha):
        # Cadastra um novo usuario na tabela
        Usuario.criar_tabela()

        df = pd.read_excel('login.xlsx', dtype=str)

        if usuario in df['Usuário'].values:
            sg.popup(f"Usuário '{usuario}' já cadastrado.")
            return

        novo_usuario = pd.DataFrame({'Usuário': [usuario], 'Senha': [senha]})
        df = pd.concat([df, novo_usuario], ignore_index=True)
        df.to_excel('login.xlsx', index=False)
        sg.popup(f"Usuário '{usuario}' cadastrado com sucesso!")

    @staticmethod
    def cadastrar_usuario_tela():
        # Interface gráfica para cadastrar um usuario
        layout = [
            [sg.Text('Página Cadastrar Usuário')],
            [sg.Text('Usuário:'), sg.InputText(key='-USUÁRIO-')],
            [sg.Text('Senha:'), sg.InputText(key='-SENHA-')],
            [sg.Button('Cadastrar'), sg.Button('Cancelar')]
        ]

        janela = sg.Window('Cadastrar Usuário', layout)

        while True:
            evento, valores = janela.read()

            if evento == sg.WIN_CLOSED or evento == 'Cancelar':
                break


            elif evento == 'Cadastrar':
                if valores['-USUÁRIO-'] == '' or valores['-SENHA-'] == '':
                    sg.popup("Por favor, preencha todos os campos corretamente antes de cadastrar o usuário.")
                else:
                    Usuario.cadastrar_usuario(valores['-USUÁRIO-'], valores['-SENHA-'])

        janela.close()

    def realizar_login(self, usuario, senha):
        # Realiza o login verificando as credenciais na tabela
        df = pd.read_excel(self.arquivo_login, dtype=str)
        if any((df['Usuário'] == usuario) & (df['Senha'] == senha)):
            mostrar_tela_home()
        else:
            sg.popup("Credenciais inválidas. Tente novamente.")

class Produtos:
    @staticmethod
    def criar_tabela():
        # Cria a tabela de produtos se não existir
        if not os.path.exists('produtos.xlsx'):
            df = pd.DataFrame(columns=['Nome', 'Quantidade', 'Valor'])
            df.to_excel('produtos.xlsx', index=False)

    @staticmethod
    def cadastrar_produto(nome, quantidade, valor):
        # Cadastra um novo produto na tabela
        Produtos.criar_tabela()

        df_produtos = pd.read_excel('produtos.xlsx', dtype=str)

        if nome in df_produtos['Nome'].values:
            # Se o produto já existir, atualiza a quantidade
            idx_produto = df_produtos.index[df_produtos['Nome'] == nome].tolist()[0]
            nova_quantidade = int(df_produtos.loc[idx_produto, 'Quantidade']) + int(quantidade)
            df_produtos.at[idx_produto, 'Quantidade'] = str(nova_quantidade)
            sg.popup(f"Quantidade do produto '{nome}' atualizada para {nova_quantidade}.")
        else:
            # Se o produto não existir, adiciona um novo registro
            novo_produto = pd.DataFrame({'Nome': [nome], 'Quantidade': [quantidade], 'Valor': [valor]})
            df_produtos = pd.concat([df_produtos, novo_produto], ignore_index=True)
            sg.popup(f"Produto '{nome}' cadastrado com sucesso!")

        df_produtos.to_excel('produtos.xlsx', index=False)

    @staticmethod
    def cadastrar_produto_tela():
        # Interface gráfica para cadastrar um produto
        layout = [
            [sg.Text('Página Cadastrar Produto')],
            [sg.Text('Nome do Produto:'), sg.InputText(key='-NOME_PRODUTO-')],
            [sg.Text('Quantidade:'), sg.InputText(key='-QUANTIDADE_PRODUTO-')],
            [sg.Text('Valor:'), sg.InputText(key='-VALOR_PRODUTO-', enable_events=True, justification='right')],
            [sg.Button('Cadastrar'), sg.Button('Cancelar')]
        ]

        janela = sg.Window('Cadastrar Produto', layout)

        while True:
            evento, valores = janela.read()

            if evento == sg.WIN_CLOSED or evento == 'Cancelar':
                break
            elif evento == 'Cadastrar':
                nome_produto = valores['-NOME_PRODUTO-']
                quantidade_produto = valores['-QUANTIDADE_PRODUTO-']
                valor_produto = valores['-VALOR_PRODUTO-']

                if nome_produto == '' or quantidade_produto == '' or valor_produto == '':
                    sg.popup("Por favor, preencha todos os campos antes de cadastrar o produto.")
                else:
                    if int(quantidade_produto) < 1:
                        sg.popup("A quantidade do produto deve ser maior ou igual a 1.")
                    else:
                        valor_formatado = format_currency(float(valor_produto), 'BRL', locale='pt_BR')
                        Produtos.cadastrar_produto(nome_produto, quantidade_produto, valor_formatado)

        janela.close()

class Clientes:
    @staticmethod
    def criar_tabela():
        # Cria a tabela de clientes se não existir
        if not os.path.exists('clientes.xlsx'):
            df = pd.DataFrame(columns=['Nome', 'Telefone'])
            df.to_excel('clientes.xlsx', index=False)

    @staticmethod
    def validar_nome_cliente(nome):
        # Valida se o nome do cliente contém apenas letras e espaços
        return bool(re.match("^[A-Za-z ]+$", nome))

    @staticmethod
    def validar_telefone(telefone):
        # Valida se o telefone está no formato desejado (XX) XXXXX-XXXX
        return bool(re.match(r'^\(\d{2}\) \d{5}-\d{4}$', telefone))

    @staticmethod
    def cadastrar_cliente(nome, telefone):
        # Cadastra um novo cliente na tabela
        Clientes.criar_tabela()

        df = pd.read_excel('clientes.xlsx', dtype=str)

        if nome in df['Nome'].values:
            sg.popup(f"Cliente '{nome}' já cadastrado.")
            return

        novo_cliente = pd.DataFrame({'Nome': [nome], 'Telefone': [telefone]})
        df = pd.concat([df, novo_cliente], ignore_index=True)
        df.to_excel('clientes.xlsx', index=False)
        sg.popup(f"Cliente '{nome}' cadastrado com sucesso!")

    @staticmethod
    def cadastrar_cliente_tela():
        # Interface gráfica para cadastrar um cliente com máscara de entrada
        layout = [
            [sg.Text('Página Cadastrar Cliente')],
            [sg.Text('Nome do Cliente:'), sg.InputText(key='-NOME_CLIENTE-', enable_events=True, size=(20, 1),
                                                        justification='center', tooltip='Somente letras e espaços')],
            [sg.Text('Telefone:'),
             sg.InputText(key='-TELEFONE_CLIENTE-', enable_events=True, size=(15, 1), justification='center')],
            [sg.Button('Cadastrar'), sg.Button('Cancelar')]
        ]

        janela = sg.Window('Cadastrar Cliente', layout)

        while True:
            evento, valores = janela.read()

            if evento == sg.WIN_CLOSED or evento == 'Cancelar':
                break
            elif evento == '-NOME_CLIENTE-':
                valores['-NOME_CLIENTE-'] = ''.join(
                    [c.upper() for c in valores['-NOME_CLIENTE-'] if c.isalpha() or c.isspace()])
                janela['-NOME_CLIENTE-'].update(valores['-NOME_CLIENTE-'])
            elif evento == '-TELEFONE_CLIENTE-':
                # Adiciona a máscara de telefone (xx) xxxxx-xxxx
                input_text = valores['-TELEFONE_CLIENTE-']
                if len(input_text) == 2 and not input_text.endswith('('):
                    janela['-TELEFONE_CLIENTE-'].update(f"({input_text}) ")
                elif len(input_text) == 10 and not input_text.endswith('-'):
                    janela['-TELEFONE_CLIENTE-'].update(f"{input_text}-")
                elif len(input_text) == 15:
                    janela['-TELEFONE_CLIENTE-'].update(f"{input_text}")

            elif evento == 'Cadastrar':
                if valores['-NOME_CLIENTE-'] == '' or valores['-TELEFONE_CLIENTE-'] == '' or not Clientes.validar_telefone(
                        valores['-TELEFONE_CLIENTE-']):
                    sg.popup("Por favor, preencha todos os campos corretamente antes de cadastrar o cliente.")
                else:
                    Clientes.cadastrar_cliente(valores['-NOME_CLIENTE-'], valores['-TELEFONE_CLIENTE-'])

        janela.close()

class Vendas:
    @staticmethod
    def criar_tabela():
        # Cria a tabela de vendas se não existir
        if not os.path.exists('vendas.xlsx'):
            df = pd.DataFrame(columns=['Cliente', 'Produto', 'Quantidade', 'Valor Total'])
            df.to_excel('vendas.xlsx', index=False)

    @staticmethod
    def cadastrar_venda(cliente, produto, quantidade):
        # Cadastra uma nova venda na tabela
        Vendas.criar_tabela()

        df_produtos = pd.read_excel('produtos.xlsx', dtype=str)

        # Encontra o índice do produto na planilha de produtos
        idx_produto = df_produtos.index[df_produtos['Nome'] == produto].tolist()[0]

        estoque_atual = int(df_produtos.loc[idx_produto, 'Quantidade'])

        # Verifica se a quantidade em estoque é suficiente
        if estoque_atual < int(quantidade):
            sg.popup("Quantidade em estoque insuficiente. Venda não realizada.")
            return

        # Calcula o valor total da venda
        valor_unitario = float(df_produtos.loc[idx_produto, 'Valor'].replace('R$', '').replace(',', '.').strip())
        valor_total = valor_unitario * int(quantidade)

        df_vendas = pd.read_excel('vendas.xlsx', dtype=str)
        nova_venda = pd.DataFrame({'Cliente': [cliente], 'Produto': [produto], 'Quantidade': [quantidade],
                                   'Valor Total': [valor_total]})
        df_vendas = pd.concat([df_vendas, nova_venda], ignore_index=True)
        df_vendas.to_excel('vendas.xlsx', index=False)

        # Atualiza o estoque
        Vendas.atualizar_estoque(produto, quantidade)

        sg.popup(f"Venda para o cliente '{cliente}' do produto '{produto}' cadastrada com sucesso!")

    def atualizar_estoque(produto, quantidade_vendida):
        df_produtos = pd.read_excel('produtos.xlsx', dtype=str)

        # Encontra o índice do produto na planilha de produtos
        idx_produto = df_produtos.index[df_produtos['Nome'] == produto].tolist()[0]

        # Deduz a quantidade vendida do estoque
        estoque_atual = int(df_produtos.loc[idx_produto, 'Quantidade'])
        novo_estoque = estoque_atual - int(quantidade_vendida)

        # Verifica se o estoque fica negativo
        novo_estoque = max(novo_estoque, 0)

        # Atualiza o valor na planilha de produtos
        df_produtos.at[idx_produto, 'Quantidade'] = str(novo_estoque)
        df_produtos.to_excel('produtos.xlsx', index=False)

    @staticmethod
    def cadastrar_venda_tela():
        # Carrega a lista de clientes e produtos
        clientes = pd.read_excel('clientes.xlsx')['Nome'].tolist()
        produtos = pd.read_excel('produtos.xlsx')['Nome'].tolist()

        layout = [
            [sg.Text('Página Cadastrar Venda')],
            [sg.Text('Cliente:'), sg.Combo(clientes, key='-CLIENTE_VENDA-', enable_events=True)],
            [sg.Text('Produto:'), sg.Combo(produtos, key='-PRODUTO_VENDA-', enable_events=True)],
            [sg.Text('Quantidade:'), sg.InputText(key='-QUANTIDADE_VENDA-', enable_events=True)],
            [sg.Button('Cadastrar'), sg.Button('Cancelar')]
        ]

        janela = sg.Window('Cadastrar Venda', layout)

        while True:
            evento, valores = janela.read()

            if evento == sg.WIN_CLOSED or evento == 'Cancelar':
                break
            elif evento == 'Cadastrar':
                if valores['-CLIENTE_VENDA-'] == '' or valores['-PRODUTO_VENDA-'] == '' or valores[
                    '-QUANTIDADE_VENDA-'] == '':
                    sg.popup("Por favor, preencha todos os campos antes de cadastrar a venda.")
                else:
                    Vendas.cadastrar_venda(valores['-CLIENTE_VENDA-'], valores['-PRODUTO_VENDA-'],
                                    valores['-QUANTIDADE_VENDA-'])

        janela.close()

def mostrar_tela_home():
    # Interface gráfica da tela inicial
    layout_home = [
        [sg.Text('Bem-vindo à Tela Home')],
        [sg.Button('Produtos'), sg.Button('Clientes'), sg.Button('Vendas')]
    ]

    janela_home = sg.Window('Tela Home', layout_home)

    while True:
        evento, valores = janela_home.read()

        if evento == sg.WIN_CLOSED:
            break
        elif evento == 'Produtos':
            Produtos.cadastrar_produto_tela()
        elif evento == 'Clientes':
            Clientes.cadastrar_cliente_tela()
        elif evento == 'Vendas':
            Vendas.cadastrar_venda_tela()

    janela_home.close()