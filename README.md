# 💰 Sistema Bancário em Python — `projeto_DIO_sistema_bancario_v3`

Projeto desenvolvido como parte de um desafio da [DIO](https://www.dio.me/), com o objetivo de consolidar conhecimentos em Programação Orientada a Objetos (POO) e manipulação de dados em Python.

Este sistema simula operações bancárias básicas e completas, com suporte a múltiplos usuários e múltiplas contas correntes, tudo via linha de comando.

---

## 🚀 Funcionalidades

- ✅ **Cadastro de clientes** com CPF, nome completo, data de nascimento e endereço  
- ✅ **Validação de CPF e data de nascimento** (usuário deve ter no mínimo 18 anos)  
- ✅ **Criação de múltiplas contas correntes** para um mesmo cliente  
- ✅ **Depósitos** com registro no histórico  
- ✅ **Saques** com:
  - Limite diário de **3 saques**
  - Limite de **R$500,00 por saque**
- ✅ **Emissão de extrato** por conta, com:
  - Saldo atual
  - Histórico detalhado (tipo, valor, data e hora)
- ✅ **Listagem de contas e clientes** cadastrados  
- ✅ Suporte a valores com **vírgula ou ponto decimal** (ex: `0,10` ou `0.10`)  
- ✅ **Interface simples e intuitiva** via terminal  

---

## 🛠️ Tecnologias utilizadas

- **Python 3.x**
- **POO — Programação Orientada a Objetos**
- Módulos padrão:
  - `re` (expressões regulares)
  - `textwrap` (formatação de texto)
  - `datetime` (manipulação de datas e horas)
  - `abc` (classes abstratas)

---

## ▶️ Como executar

1. **Clone o repositório:**

```bash
git clone https://github.com/vixnzin/projeto_DIO_sistema_bancario_v3.git
cd projeto_DIO_sistema_bancario_v3
```

2. **Execute o programa:**

```bash
python desafio.py
```

> 💡 Certifique-se de que o **Python 3** esteja instalado na sua máquina.

---

## 🧠 Estrutura do código

- `Cliente`, `Pessoa_fisica`, `Conta`, `Conta_Corrente` — classes principais que definem o modelo de usuários e contas
- `Transacao`, `Saque`, `Deposito` — modelo de movimentações financeiras
- `Historico` — armazena todas as transações com timestamp
- Funções auxiliares:
  - Cadastro de clientes e contas
  - Realização de depósitos e saques
  - Geração de extratos e listagens

---

## 👤 Autor

Feito com dedicação por **Vicenzo Cirilo**  
🔗 [github.com/vixnzin](https://github.com/vixnzin)

---

## 📜 Licença

Este projeto é de código aberto e está licenciado sob a [MIT License](LICENSE).
