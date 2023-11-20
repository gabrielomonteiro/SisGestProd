from turtle import pd

from classes import Usuario, Produtos, Clientes, Vendas
import unittest
import os

class TestUsuario(unittest.TestCase):

  def setUp(self):
    # Inicializa o objeto Usuario para os testes
    self.usuario = Usuario()

  def test_criar_tabela(self):
    # Testa se criar uma tabela de usuários resulta na criação do arquivo
    self.usuario.criar_tabela()
    self.assertTrue(os.path.exists(self.usuario.arquivo_login))

  def test_usuario_existe(self):
    # Testa se o método identifica corretamente usuários existentes
    self.assertFalse(self.usuario.usuario_existe('test_user'))
    self.usuario.cadastrar_usuario('test_user', 'test_password')
    self.assertTrue(self.usuario.usuario_existe('test_user'))

  def test_cadastrar_usuario(self):
    # Testa se um novo usuário é adicionado com sucesso à tabela
    self.usuario.cadastrar_usuario('test_user', 'test_password')
    self.assertTrue(self.usuario.usuario_existe('test_user'))

  def test_realizar_login(self):
    # Testa se a função de login autentica com sucesso um usuário
    self.usuario.cadastrar_usuario('test_user', 'test_password')
    self.assertTrue(self.usuario.realizar_login('test_user', 'test_password'))

  def tearDown(self):
    # Limpeza removendo o arquivo criado
    os.remove(self.usuario.arquivo_login)



class TestProdutos(unittest.TestCase):

  def setUp(self):
    # Inicializa o objeto Produtos para os testes
    self.produtos = Produtos()

  def test_criar_tabela(self):
    # Testa se criar uma tabela de produtos resulta na criação do arquivo
    self.produtos.criar_tabela()
    self.assertTrue(os.path.exists('produtos.xlsx'))

  def test_cadastrar_produto(self):
    # Testa se um novo produto é adicionado com sucesso à tabela
    self.produtos.cadastrar_produto('TestProduct', 10, '50.00')
    df = pd.read_excel('produtos.xlsx')
    self.assertTrue('TestProduct' in df['Nome'].values)

  def test_cadastrar_produto_tela(self):
    # Escreva casos de teste para a interface gráfica do usuário
    # Explicação: Testes de interface gráfica geralmente envolvem interações complexas
    # e podem exigir ferramentas de teste especializadas, como unittest.mock.

  def tearDown(self):
    # Limpeza removendo o arquivo criado
    os.remove('produtos.xlsx')


class TestClientes(unittest.TestCase):

  def setUp(self):
    # Inicializa o objeto Clientes para os testes
    self.clientes = Clientes()

  def test_criar_tabela(self):
    # Testa se criar uma tabela de clientes resulta na criação do arquivo
    self.clientes.criar_tabela()
    self.assertTrue(os.path.exists('clientes.xlsx'))

  def test_validar_nome_cliente(self):
    # Testa se o método valida corretamente os nomes dos clientes
    self.assertTrue(self.clientes.validar_nome_cliente('John Doe'))
    self.assertFalse(self.clientes.validar_nome_cliente('1234'))

  def test_validar_telefone(self):
    # Testa se o método valida corretamente os números de telefone
    self.assertTrue(self.clientes.validar_telefone('(12) 34567-8901'))
    self.assertFalse(self.clientes.validar_telefone('12345678901'))

  def test_cadastrar_cliente(self):
    # Testa se um novo cliente é adicionado com sucesso à tabela
    self.clientes.cadastrar_cliente('TestClient', '(11) 98765-4321')
    df = pd.read_excel('clientes.xlsx')
    self.assertTrue('TestClient' in df['Nome'].values)

  def test_cadastrar_cliente_tela(self):
    # Escreva casos de teste para a interface gráfica do usuário
    # Explicação: Testes de interface gráfica geralmente envolvem interações complexas
    # e podem exigir ferramentas de teste especializadas, como unittest.mock.

  def tearDown(self):
    # Limpeza removendo o arquivo criado
    os.remove('clientes.xlsx')



class TestVendas(unittest.TestCase):

  def setUp(self):
    # Inicializa o objeto Vendas para os testes
    self.vendas = Vendas()

  def test_criar_tabela(self):
    # Testa se criar uma tabela de vendas resulta na criação do arquivo
    self.vendas.criar_tabela()
    self.assertTrue(os.path.exists('vendas.xlsx'))

  def test_cadastrar_venda(self):
    # Testa se uma nova venda é adicionada com sucesso à tabela
    self.vendas.cadastrar_venda('TestClient', 'TestProduct', 5)
    df = pd.read_excel('vendas.xlsx')
    self.assertTrue('TestClient' in df['Cliente'].values)

  def test_atualizar_estoque(self):
    # Testa se o estoque é atualizado corretamente após uma venda
    self.vendas.cadastrar_venda('TestClient', 'TestProduct', 5)
    df_produtos = pd.read_excel('produtos.xlsx')
    self.assertEqual(int(df_produtos[df_produtos['Nome'] == 'TestProduct']['Quantidade']), 5)

  def test_cadastrar_venda_tela(self):
    # Escreva casos de teste para a interface gráfica do usuário
    # Explicação: Testes de interface gráfica geralmente envolvem interações complexas
    # e podem exigir ferramentas de teste especializadas, como unittest.mock.

  def tearDown(self):
    # Limpeza removendo os arquivos criados
    os.remove('vendas.xlsx')
    os.remove('produtos.xlsx')



if __name__ == '__main__':
    unittest.main()