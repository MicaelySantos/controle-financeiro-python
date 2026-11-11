
import json
from pathlib import Path
from datetime import datetime

ARQUIVO = Path(__file__).with_name("movimentacoes.json")


# Carrega as movimentacoes salvas
def carregar_dados():
    if ARQUIVO.exists():
        try:
            with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
                if isinstance(dados, list):
                    return dados
        except (json.JSONDecodeError, OSError):
            print("Nao foi possivel carregar os dados.")

    return []


# Salva as movimentacoes
def salvar_dados(movimentacoes):
    with open(ARQUIVO, "w", encoding="utf-8") as arquivo:
        json.dump(movimentacoes, arquivo, indent=4,
                  ensure_ascii=False)


# Le valores monetarios
def ler_valor():
    while True:
        entrada = input("Valor (R$): ").strip()
        entrada = entrada.replace(",", ".")

        try:
            valor = float(entrada)

            if 0 < valor < float("inf"):
                return round(valor, 2)

            print("Digite um valor positivo e valido.")

        except ValueError:
            print("Valor invalido. Tente novamente.")


# Cadastra receitas ou despesas
def cadastrar_movimentacao(movimentacoes, tipo):
    print(f"\n--- CADASTRAR {tipo.upper()} ---")

    descricao = input("Descricao: ").strip()

    if not descricao:
        print("A descricao nao pode estar vazia.")
        return

    categoria = input("Categoria: ").strip()

    if not categoria:
        print("A categoria nao pode estar vazia.")
        return

    valor = ler_valor()

    movimentacao = {
        "tipo": tipo,
        "descricao": descricao,
        "categoria": categoria,
        "valor": valor,
        "data": datetime.now().strftime("%d/%m/%Y %H:%M")
    }

    movimentacoes.append(movimentacao)
    salvar_dados(movimentacoes)

    print(f"\n{tipo.capitalize()} cadastrada com sucesso!")


# Lista todas as movimentacoes
def listar_movimentacoes(movimentacoes):
    print("\n--- MOVIMENTACOES FINANCEIRAS ---")

    if not movimentacoes:
        print("Nenhuma movimentacao cadastrada.")
        return

    for indice, mov in enumerate(movimentacoes, start=1):
        print(f"\nMovimentacao {indice}")
        print(f"Tipo: {mov['tipo'].capitalize()}")
        print(f"Descricao: {mov['descricao']}")
        print(f"Categoria: {mov['categoria']}")
        print(f"Valor: R$ {mov['valor']:.2f}")
        print(f"Data: {mov['data']}")
        print("-" * 30)


# Calcula receitas, despesas e saldo
def calcular_totais(movimentacoes):
    receitas = sum(
        mov["valor"] for mov in movimentacoes
        if mov["tipo"] == "receita"
    )

    despesas = sum(
        mov["valor"] for mov in movimentacoes
        if mov["tipo"] == "despesa"
    )

    saldo = receitas - despesas

    return receitas, despesas, saldo


# Mostra o saldo
def consultar_saldo(movimentacoes):
    receitas, despesas, saldo = calcular_totais(movimentacoes)

    print("\n--- SALDO FINANCEIRO ---")
    print(f"Total de receitas: R$ {receitas:.2f}")
    print(f"Total de despesas: R$ {despesas:.2f}")
    print(f"Saldo disponivel: R$ {saldo:.2f}")


# Gera um relatorio financeiro
def relatorio_financeiro(movimentacoes):
    print("\n--- RELATORIO FINANCEIRO ---")

    if not movimentacoes:
        print("Nenhuma movimentacao cadastrada.")
        return

    receitas, despesas, saldo = calcular_totais(movimentacoes)

    print(f"Quantidade de movimentacoes: {len(movimentacoes)}")
    print(f"Total de receitas: R$ {receitas:.2f}")
    print(f"Total de despesas: R$ {despesas:.2f}")
    print(f"Saldo final: R$ {saldo:.2f}")

    print("\nDESPESAS POR CATEGORIA")

    categorias = {}

    for mov in movimentacoes:
        if mov["tipo"] == "despesa":
            categoria = mov["categoria"]
            categorias[categoria] = (
                    categorias.get(categoria, 0) + mov["valor"]
            )

    if not categorias:
        print("Nenhuma despesa cadastrada.")
    else:
        for categoria, valor in sorted(categorias.items()):
            print(f"{categoria}: R$ {valor:.2f}")


# Exibe o menu principal
def mostrar_menu():
    print("\n================================")
    print("   CONTROLE FINANCEIRO PESSOAL")
    print("================================")
    print("1 - Cadastrar receita")
    print("2 - Cadastrar despesa")
    print("3 - Listar movimentacoes")
    print("4 - Consultar saldo")
    print("5 - Relatorio financeiro")
    print("0 - Sair")
    print("================================")


# Funcao principal
def main():
    movimentacoes = carregar_dados()

    while True:
        mostrar_menu()
        opcao = input("Escolha uma opcao: ").strip()

        if opcao == "1":
            cadastrar_movimentacao(movimentacoes, "receita")

        elif opcao == "2":
            cadastrar_movimentacao(movimentacoes, "despesa")

        elif opcao == "3":
            listar_movimentacoes(movimentacoes)

        elif opcao == "4":
            consultar_saldo(movimentacoes)

        elif opcao == "5":
            relatorio_financeiro(movimentacoes)

        elif opcao == "0":
            print("\nEncerrando o sistema...")
            print("Seus dados foram salvos. Ate a proxima!")
            break

        else:
            print("\nOpcao invalida!")


if __name__ == "__main__":
    main()
