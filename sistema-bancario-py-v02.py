import re
from datetime import datetime
from functools import wraps

# ==================== DECORADOR DE LOG ====================

def log_transacao(func):
    """
    Decorador que aplica um log de transação para as funções de operações bancárias.
    Exibe no console um registro detalhado sempre que uma transação é bem-sucedida.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Encontra o extrato nos argumentos para comparação posterior
        # Para 'sacar' (keyword args): kwargs['extrato']
        # Para 'depositar' (positional args): args[2]
        extrato_antes = kwargs.get('extrato', args[2] if len(args) > 2 else "")

        # Executa a função original (depositar ou sacar)
        resultado = func(*args, **kwargs)

        # O extrato atualizado está sempre na segunda posição do tuple retornado
        extrato_depois = resultado[1]

        # Se o extrato mudou, a transação foi bem-sucedida e o log é exibido
        if extrato_antes != extrato_depois:
            transacao_realizada = extrato_depois[len(extrato_antes):].strip()
            print("--- REGISTRO DA OPERAÇÃO ---")
            print(f"Operação: {func.__name__.upper()}")
            print(f"Detalhes: {transacao_realizada}")
            print(f"Executada em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
            print("--------------------------\n")
        
        return resultado
    return wrapper


# ==================== FUNÇÕES DE OPERAÇÕES BANCÁRIAS ====================

@log_transacao
def depositar(saldo, valor, extrato, /):
    """
    Realiza operação de depósito. Agora com registro de data/hora no extrato.
    """
    if valor > 0:
        saldo += valor
        timestamp = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        extrato += f"[{timestamp}] Depósito: R$ {valor:.2f}\n"
        print(f"Depósito de R$ {valor:.2f} realizado com sucesso!\n")
    else:
        print("Operação falhou! O valor informado é inválido.\n")
    
    return saldo, extrato


@log_transacao
def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    """
    Realiza operação de saque. Agora com registro de data/hora no extrato.
    """
    if valor > limite:
        print(f"Operação falhou! O valor do saque excede o limite de R$ {limite:.2f}.\n")
    elif numero_saques >= limite_saques:
        print("Operação falhou! Você atingiu o limite de saques.\n")
    elif valor > saldo:
        print("Operação falhou! Saldo insuficiente.\n")
    elif valor <= 0:
        print("Operação falhou! Valor informado é inválido.\n")
    else:
        saldo -= valor
        timestamp = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        extrato += f"[{timestamp}] Saque:    R$ {valor:.2f}\n"
        numero_saques += 1
        print(f"Saque de R$ {valor:.2f} realizado com sucesso!\n")
    
    return saldo, extrato, numero_saques


def exibir_extrato(saldo, /, *, extrato):
    """
    Exibe o extrato da conta.
    """
    print("\n================== EXTRATO ==================")
    print("Não foram realizadas movimentações." if not extrato else extrato, end="")
    print("-------------------------------------------")
    print(f"Saldo: R$ {saldo:.2f}")
    print("===========================================\n")


# ==================== FUNÇÕES DE USUÁRIO ====================

def criar_usuario(usuarios):
    """
    Cria um novo usuário no sistema.
    """
    print("\n=== CADASTRO DE USUÁRIO ===")
    
    nome = input("Informe o nome completo: ").strip()

    # Validação da data de nascimento com regex para o formato dd/mm/aaaa
    padrao_data = r"^\d{2}/\d{2}/\d{4}$"
    while True:
        data_nascimento = input("Informe a data de nascimento (dd/mm/aaaa): ").strip()
        if re.match(padrao_data, data_nascimento):
            break
        else:
            print("❌ Formato de data inválido! Por favor, use o formato dd/mm/aaaa.")
    
    # Validação e limpeza do CPF
    while True:
        cpf = input("Informe o CPF (apenas números): ").strip()
        if re.match(r"^\d{11}$", cpf):
            cpf_numeros = re.sub(r'\D', '', cpf)  # Remove tudo que não for dígito
            break  # Formato válido, sai do loop
        else:
            print("❌ CPF inválido! Por favor, digite 11 números.")
    
    if len(cpf_numeros) != 11:
        print("CPF inválido! Deve conter 11 dígitos.\n")
        return usuarios
    
    # Verifica se CPF já existe
    if any(usuario['cpf'] == cpf_numeros for usuario in usuarios):
        print("CPF já cadastrado no sistema!\n")
        return usuarios
    
    # Coleta endereço
    print("\n--- Endereço ---")
    logradouro = input("Logradouro: ").strip()
    numero = input("Número: ").strip()
    bairro = input("Bairro: ").strip()
    cidade = input("Cidade: ").strip()
    estado = input("Estado (sigla): ").strip().upper()
    
    endereco = f"{logradouro}, {numero}, {bairro}, {cidade}, {estado}"
    
    # Cria o usuário
    usuario = {
        'nome': nome,
        'data_nascimento': data_nascimento,
        'cpf': cpf_numeros,
        'endereco': endereco
    }
    
    usuarios.append(usuario)
    print(f"Usuário {nome} cadastrado com sucesso!\n")
    
    return usuarios


def buscar_usuario_por_cpf(usuarios, cpf):
    """
    Busca um usuário pelo CPF.
    """
    cpf_numeros = re.sub(r'\D', '', cpf)
    return next((usuario for usuario in usuarios if usuario['cpf'] == cpf_numeros), None)


def listar_usuarios(usuarios):
    """Lista todos os usuários cadastrados."""
    if not usuarios:
        print("Nenhum usuário cadastrado.\n")
        return
    
    print("\n=== USUÁRIOS CADASTRADOS ===")
    for i, usuario in enumerate(usuarios, 1):
        print(f"{i}. {usuario['nome']} - CPF: {usuario['cpf']}")
    print()


# ==================== FUNÇÕES DE CONTA ====================

def criar_conta(usuarios, contas):
    """
    Cria uma nova conta corrente.
    """
    print("\n=== ABERTURA DE CONTA ===")
    
    if not usuarios:
        print("Nenhum usuário cadastrado! Cadastre um usuário primeiro.\n")
        return contas
    
    cpf = input("Informe o CPF do titular: ").strip()
    usuario = buscar_usuario_por_cpf(usuarios, cpf)
    
    if not usuario:
        print("Usuário não encontrado! Cadastre o usuário primeiro.\n")
        return contas
    
    # Número da conta é sequencial
    numero_conta = len(contas) + 1
    agencia = "0001"
    
    conta = {
        'agencia': agencia,
        'numero': numero_conta,
        'usuario': usuario,
        'saldo': 0,
        'extrato': "",
        'numero_saques': 0
    }
    
    contas.append(conta)
    print(f"Conta {numero_conta} criada com sucesso para {usuario['nome']}!\n")
    
    return contas


def listar_contas(contas):
    """Lista todas as contas cadastradas."""
    if not contas:
        print("Nenhuma conta cadastrada.\n")
        return
    
    print("\n=== CONTAS CADASTRADAS ===")
    for conta in contas:
        print(f"Agência: {conta['agencia']} | Conta: {conta['numero']} | "
              f"Titular: {conta['usuario']['nome']} | Saldo: R$ {conta['saldo']:.2f}")
    print()


def selecionar_conta(contas):
    """
    Permite ao usuário selecionar uma conta.
    """
    if not contas:
        print("Nenhuma conta cadastrada.\n")
        return None
    
    print("\n=== SELECIONAR CONTA ===")
    listar_contas(contas)
    
    try:
        numero_conta = int(input("Digite o número da conta: "))
        conta = next((conta for conta in contas if conta['numero'] == numero_conta), None)
        
        if not conta:
            print("Conta não encontrada!\n")
            return None
        
        print(f"Conta selecionada: {numero_conta} - {conta['usuario']['nome']}\n")
        return conta
    
    except ValueError:
        print("Número inválido!\n")
        return None


# ==================== MENU E SISTEMA PRINCIPAL ====================

def exibir_menu_principal():
    """Exibe o menu principal do sistema."""
    return input("""
=============== SISTEMA BANCÁRIO ================
[d]  Depositar
[s]  Sacar
[e]  Extrato
[nu] Novo usuário
[lu] Listar usuários
[nc] Nova conta
[lc] Listar contas
[sc] Selecionar conta
[q]  Sair
=================================================
Escolha uma opção: """).lower().strip()


def main():
    """Função principal do sistema."""
    # Dados do sistema
    usuarios = []
    contas = []
    conta_atual = None
    
    # Constantes
    LIMITE_SAQUE = 500
    LIMITE_SAQUES = 3
    
    print("🏛️  Bem-vindo ao DIO Bank!")
    print("Para realizar operações, primeiro crie um usuário e uma conta.\n")
    
    while True:
        operacao = exibir_menu_principal()
        
        if operacao in ['d', 's', 'e']:
            if not conta_atual:
                print("❌ Nenhuma conta selecionada! Use a opção [sc] para selecionar uma conta.\n")
                continue
        
        if operacao == "d":
            try:
                valor = float(input("Informe o valor do depósito: R$ "))
                conta_atual['saldo'], conta_atual['extrato'] = depositar(
                    conta_atual['saldo'], valor, conta_atual['extrato']
                )
            except ValueError:
                print("Valor inválido! Digite um número.\n")
        
        elif operacao == "s":
            try:
                valor = float(input("Informe o valor do saque: R$ "))
                saldo, extrato, numero_saques = sacar(
                    saldo=conta_atual['saldo'],
                    valor=valor,
                    extrato=conta_atual['extrato'],
                    limite=LIMITE_SAQUE,
                    numero_saques=conta_atual['numero_saques'],
                    limite_saques=LIMITE_SAQUES
                )
                conta_atual['saldo'] = saldo
                conta_atual['extrato'] = extrato
                conta_atual['numero_saques'] = numero_saques
            except ValueError:
                print("Valor inválido! Digite um número.\n")
        
        elif operacao == "e":
            exibir_extrato(conta_atual['saldo'], extrato=conta_atual['extrato'])
        
        elif operacao == "nu":
            usuarios = criar_usuario(usuarios)
        
        elif operacao == "lu":
            listar_usuarios(usuarios)
        
        elif operacao == "nc":
            contas = criar_conta(usuarios, contas)
        
        elif operacao == "lc":
            listar_contas(contas)
        
        elif operacao == "sc":
            conta_selecionada = selecionar_conta(contas)
            if conta_selecionada:
                conta_atual = conta_selecionada
        
        elif operacao == "q":
            print("👋 Obrigado por usar nosso sistema! Até logo!")
            break
        
        else:
            print("❌ Operação inválida! Escolha uma opção válida do menu.\n")


# ==================== EXECUÇÃO ====================

if __name__ == "__main__":
    main()