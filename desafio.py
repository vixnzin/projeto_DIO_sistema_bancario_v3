
import re
import textwrap
from datetime import datetime
from abc import ABC, abstractmethod

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacoes(self, conta, transacao):
        transacao.registrar(conta)
        
    def adicionar_conta(self, conta):
        self.contas.append(conta)

class Pessoa_fisica(Cliente):
    def __init__(self,nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome= nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0 
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()


    @classmethod 
    def nova_conta(cls, numero, cliente):
        return cls(numero, cliente)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    
    def sacar(self, valor):
        saldo = self._saldo
        excedeu_saldo = valor > saldo
    
        if excedeu_saldo:
            print("\n### Operação falhou! Você não tem saldo suficiente. ###")

        elif valor > 0:
            self._saldo -= valor
            print(f"\n=== Saque realizado com sucesso! O valor de R$ {valor:.2f} foi sacado da sua conta. ===")
            return True

        else:
            print("\n### Operação falhou! O valor informado é inválido. ###")
            return False
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print(f"\n=== Depósito realizado com sucesso! O valor de R$ {valor:.2f} foi depositado à sua conta. ===")
            
        else:
            print("\n### Operação falhou! O valor informado é inválido. ###")
            return False
        
        return True
        
class Conta_Corrente(Conta):
    def __init__(self, numero, cliente, limite = 500, limite_saque = 3 ):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saque = limite_saque
       
    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__])

        excedeu_limite = valor > self.limite
        excedeu_limite_saques = numero_saques >= self.limite_saque

        if excedeu_limite:
            print("\n### Operação falhou! Você excedeu o limite de valor permitido no saque ###")
        
        elif excedeu_limite_saques:
            print("\n### Operação falhou! Você excedeu o limite diário de saques ###")

        else:
            return super().sacar(valor)
        

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """
        
class Historico:
    def __init__(self):
        self._transacoes = []


    @property
    def transacoes(self):
        return self._transacoes


    def adicionar_transacao(self, transacao):
           self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor  


    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

def menu():
    menu2 = """\n
    =======================MENU==============================

    Bem-vindo a sua Conta Bancária!

    Por favor, para avançar selecione uma das opções abaixo:

    [1]\tDepositar
    [2]\tSacar
    [3]\tExtrato
    [4]\tNova conta
    [5]\tListar contas
    [6]\tNovo Usuário
    [0]\tSair

    Digite sua opção abaixo:
    => """
    return input(textwrap.dedent(menu2))
            
def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]  
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_clientes(cliente):
    if not cliente.contas:
        print("\n### Conta do seu usuário não foi encontrada! ###")
        return None
    
    if len(cliente.contas) == 1:
        return cliente.contas[0]    
    
    print("===============================================")

    print("\nContas disponíveis:")
    for i, conta in enumerate(cliente.contas):
        print(f"[{i}] Agência: {conta.agencia} | Nº: {conta.numero}")


    try:
        indice = int(input("Escolha o número da conta: "))
        return cliente.contas[indice]
    except (ValueError, IndexError):
        print("\n### Opção inválida. Operação cancelada. ###")
        return None
     

def depositar(clientes):
    cpf = input("Informe o CPF do usuário: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("### Usuário não foi encontrado, insira novamente seu CPF! ###")
        return
    
    entrada = input("Informe o valor do depósito: ").strip().replace(',', '.')
    try:
        valor = float(entrada)
        transacao = Deposito(valor)
    except ValueError:
        print("Valor inválido! Use apenas números (ex: 20.50 ou 20,50).")
        return

    conta = recuperar_conta_clientes(cliente)
    if not conta:
        return
    
    cliente.realizar_transacoes(conta, transacao)

def sacar(clientes):
    cpf = input("Informe o CPF do usuário: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n### Usuário não foi encontrado, insira novamente seu CPF! ###")
        return
    
    entrada = input("Informe o valor do Saque: ").strip().replace(',', '.')
    try:
        valor = float(entrada)
        transacao = Saque(valor)
    except ValueError:
        print("Valor inválido! Use apenas números (ex: 20.50 ou 20,50).")
        return

    conta = recuperar_conta_clientes(cliente)
    if not conta:
        return
    
    cliente.realizar_transacoes(conta, transacao)

def exibir_extrato(clientes):
    cpf = input("Informe o CPF do usuário: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n### Usuário não foi encontrado, insira novamente seu CPF ###")
        return

    if not cliente.contas:
        print("\n### Este usuário ainda não possui nenhuma conta criada ###")
        return

    print("\n================ EXTRATO ====================")

    for conta in cliente.contas: 
        print(f"\n--- Conta {conta.numero} | Agência: {conta.agencia} ---")

        transacoes = conta.historico.transacoes

        extrato = ""
        if not transacoes:
            extrato = "Ainda não há registros de movimentação"
        else:
            for transacao in transacoes:
                extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}\n\t{transacao['data']}"


        print(extrato)
        print(f"\nSaldo atual: R$ {conta.saldo:.2f}")
        print("===============================================")


def validar_cpf(cpf):
    return bool(re.fullmatch(r'\d{3}\.?\d{3}\.?\d{3}-?\d{2}', cpf))

def validar_data_nascimento(data_nasc_str):
    try:
        nascimento = datetime.strptime(data_nasc_str, "%d/%m/%Y")
        hoje = datetime.today()
        idade = hoje.year - nascimento.year - ((hoje.month, hoje.day) < (nascimento.month, nascimento.day))
        return 18 <= idade <= 120
    except ValueError:
        return False

def criar_cliente(clientes):
    cpf = input("Informe o CPF (formato 123.456.789-09): ") 
    if not validar_cpf(cpf):
        print("CPF inválido!")
        return
    
    cliente = filtrar_cliente(cpf, clientes)
    if cliente:
        print("\n### Já existe um usuário cadastrado com este CPF! ###")
        return

    nome = input("Informe seu nome completo: ")

    data_nascimento = input("Informe sua data de nascimento (DD/MM/AAAA): ")
    if not validar_data_nascimento(data_nascimento):
        print("Data inválida!")
        return
    
    endereco = input("Informe seu endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = Pessoa_fisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco= endereco)
    clientes.append(cliente)

    print("\n === Usuário criado com sucesso! ===")

def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do usuário: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n### Usuário não foi encontrado, crie um usuário antes de tentar criar uma conta! ###")
        return
    
    conta = Conta_Corrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.adicionar_conta(conta)

    print("\n=== Conta criada com sucesso! ===")

def listar_contas(contas):
    for conta in contas:
        print("=" * 45)
        print(textwrap.dedent(str(conta))) 

    if not contas:
        print("\n### Ainda não há registros de contas! ###")    

def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()
        

        if opcao == "1":
            depositar(clientes)

        elif opcao == "2":
            sacar(clientes)

        elif opcao == "3":
            exibir_extrato(clientes)

        elif opcao == "4":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "5":
            listar_contas(contas)
        
        elif opcao == "6":
            criar_cliente(clientes)

        elif opcao == "0":
            print("\n=== Obrigado por usar nossos serviços ===\n===Tenha um Bom Dia! ===\n")
            break

        else:
           print("\n### Operação inválida, por favor selecione novamente a operação desejada. ###")
            

main()