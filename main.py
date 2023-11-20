from classes import Usuario, Produtos, Clientes, Vendas
import PySimpleGUI as sg

def main():
    # Função principal do programa
    Usuario().criar_tabela()
    Produtos().criar_tabela()
    Clientes().criar_tabela()
    Vendas().criar_tabela()

    layout_cadastro = [
        [sg.Text('Nome de Usuário:'), sg.InputText(key='-USUARIO_CAD-')],
        [sg.Text('Senha:'), sg.InputText(key='-SENHA_CAD-', password_char='*')],
        [sg.Button('Cadastrar'), sg.Button('Cancelar')]
    ]

    layout_login = [
        [sg.Text('Nome de Usuário:'), sg.InputText(key='-USUARIO_LOGIN-')],
        [sg.Text('Senha:'), sg.InputText(key='-SENHA_LOGIN-', password_char='*')],
        [sg.Button('Login', bind_return_key=True), sg.Button('Cancelar'), sg.Button('Cadastrar')]
    ]

    janela_login = sg.Window('Tela de Login', layout_login)

    while True:
        evento, valores = janela_login.read()

        if evento == sg.WIN_CLOSED or evento == 'Cancelar':
            break
        elif evento == 'Cadastrar':
            Usuario().cadastrar_usuario_tela()
        elif evento == 'Login':
            Usuario().realizar_login(valores['-USUARIO_LOGIN-'], valores['-SENHA_LOGIN-'])

    janela_login.close()

if __name__ == "__main__":
    main()
