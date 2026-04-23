# 🏦 Sistema Bancário em Python - Versão Modularizada

Este projeto implementa um sistema bancário completo em Python com operações básicas de depósito, saque, extrato, além de funcionalidades avançadas de cadastro de usuários e contas correntes.

## ✨ Funcionalidades Implementadas

### 🎯 Operações Bancárias Básicas
- **✅ Depósito**: Aceita apenas valores positivos com registro de data/hora
- **✅ Saque**: Limite de 3 saques diários com máximo de R$ 500,00 cada
- **✅ Extrato**: Exibe histórico completo com timestamps e saldo atual

### 👥 Gestão de Usuários
- **Cadastro de usuários** com validação de CPF único
- **Validação de dados**: Formato de data (dd/mm/aaaa) e CPF (11 dígitos)
- **Listagem de usuários** cadastrados no sistema
- **Endereço completo** no formato padronizado

### 💳 Gestão de Contas Correntes
- **Criação de contas** vinculadas a usuários existentes
- **Número sequencial** de contas e agência fixa "0001"
- **Seleção de conta** para operações bancárias
- **Listagem completa** de todas as contas com saldos

### 🔍 Recursos Avançados
- **Sistema de logs** automático para transações bem-sucedidas
- **Validações robustas** em todas as entradas de dados
- **Interface intuitiva** com menu organizado
- **Tratamento de erros** para entradas inválidas

## 🛠️ Tecnologias Utilizadas

- **Python 3.x** - Linguagem de programação principal
- **Módulo datetime** - Registro de data/hora nas transações
- **Expressões regulares (re)** - Validação de CPF e datas
- **Decoradores (@wraps)** - Sistema de logs automáticos
- **Estruturas de dados** - Dicionários e listas para armazenamento

## 🚀 Como Executar

1. **Clone o repositório**:
```bash
git clone https://github.com/renoalencar/dio-logbook.git
```

2. **Navegue até o diretório**:
```bash
cd dio-logbook/desafios/python/00-fundamentos/sistema-bancario-py-v02
```

3. **Execute o sistema**:
```bash
python sistema-bancario-py-v02.py
```

## 📋 Estrutura do Projeto

```
dio-bank/
├── 📄 sistema_bancario.py    # Arquivo principal do sistema
├── 📄 README.md              # Documentação do projeto
├── 📄 requirements.txt       # Dependências do projeto
└── 📄 LICENSE               # Licença de uso
```

## 💻 Menu de Operações

```
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
```

## 🎮 Exemplos de Uso

### Cadastro de Usuário:
```
=== CADASTRO DE USUÁRIO ===
Informe o nome completo: João Silva
Informe a data de nascimento (dd/mm/aaaa): 15/05/1985
Informe o CPF (apenas números): 12345678900

--- Endereço ---
Logradouro: Rua das Flores
Número: 123
Bairro: Centro
Cidade: São Paulo
Estado (sigla): SP

Usuário João Silva cadastrado com sucesso!
```

### Operação de Depósito:
```
Informe o valor do depósito: R$ 350.50
Depósito de R$ 350.50 realizado com sucesso!

--- REGISTRO DA OPERAÇÃO ---
Operação: DEPOSITAR
Detalhes: [15/05/2023 14:30:25] Depósito: R$ 350.50
Executada em: 15/05/2023 14:30:25
--------------------------
```

### Extrato Bancário:
```
================== EXTRATO ==================
[15/05/2023 14:30:25] Depósito: R$ 350.50
[15/05/2023 15:45:12] Saque:    R$ 200.00
-------------------------------------------
Saldo: R$ 150.50
===========================================
```

## ⚙️ Funcionalidades Técnicas

### Sistema de Logs Automático
```python
@log_transacao
def depositar(saldo, valor, extrato, /):
    # Implementação do depósito
    return saldo, extrato
```

### Validação de CPF
```python
def buscar_usuario_por_cpf(usuarios, cpf):
    cpf_numeros = re.sub(r'\D', '', cpf)
    return next((usuario for usuario in usuarios if usuario['cpf'] == cpf_numeros), None)
```

### Validação de Data
```python
padrao_data = r"^\d{2}/\d{2}/\d{4}$"
while not re.match(padrao_data, data_nascimento):
    print("Formato de data inválido!")
```

## 🔒 Regras de Negócio Implementadas

- ❌ **Saques sem saldo**: "Operação falhou! Saldo insuficiente."
- ❌ **Saques acima do limite**: "Operação falhou! Valor excede o limite."
- ❌ **Excesso de saques**: "Operação falhou! Limite de saques atingido."
- ❌ **CPF duplicado**: "CPF já cadastrado no sistema!"
- ❌ **Data inválida**: "Formato de data inválido!"
- ❌ **Valores inválidos**: "Valor informado é inválido."

## 👨‍💻 Autor

Desenvolvido como parte do desafio de programação da Digital Innovation One.

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](/LICENSE) para mais detalhes.

---

**💡 Observação**: Este sistema foi desenvolvido como segunda versão (v2). A primeira versão pode ser acessada em [sistema-bancario-py-v01.py](https://github.com/renoalencar/dio-sistema-bancario-simples).
