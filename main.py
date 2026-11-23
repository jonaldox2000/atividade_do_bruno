import mysql.connector
from crud import Alunos, mensagem_erro



def mostrar_alunos(lista_dos_alunos):
    for i in lista_dos_alunos:
        print(f'{i.ljust(10)[0]} | {i.ljust(10)[1]} | {i.ljust(10)[2]} | {i.ljust(10)[3]} | {i.ljust(10)[4]} | {i.ljust(10)[5]} | {i.ljust(10)[6]} | {i.ljust(10)[7]}')

def ler_criterio():
    while True:
        print("1 - ID")
        print("2 - Nome")
        opcao = input("Criterio: ").strip()
        if opcao == "1":
            return "id", input("ID: ")
        if opcao == "2":
            nome = input("Nome: ", obrigatorio=True)
            return "nome", nome
        print("Opção inválida.")


def cadastrar(alunos):
    print("\n--- Cadastrar aluno ---")
    nome = input("Nome: ", obrigatorio=True)
    profissao = input("Profissao: ")
    nascimento = int(input("Nascimento (AAAA-MM-DD): "))
    sexo = input('Qual é sua sexualidade: ')
    peso = float(input("Peso: "))
    altura = float(input('Qual sua altura: '))
    nacionalidade = input("Nacionalidade (Enter = Brasil): ") or "Brasil"
    Curso_preferido = input("Curso preferido (idcurso, ou Enter para vazio): ")
    
    try:
        novo_id = alunos.criar(
            nome,
            profissao,
            nascimento,
            sexo,
            peso,
            altura,
            nacionalidade,
            Curso_preferido,
        )
    except mysql.connector.Error as erro:
        print(mensagem_erro(erro))
        return

    print(f"Aluno cadastrado com ID {novo_id}.")

def listar(alunos):
    print("\n--- Alunos ---")
    try:
        mostrar_alunos(alunos.listar_alunos())
        print('teste')
    except mysql.connector.Error as erro:
        print(mensagem_erro(erro))
    

def atualizar(alunos):
    print("\n--- Atualizar curso preferido ---")
    criterio, valor = ler_criterio()
    curso_preferido = input("Novo curso preferido (idcurso): ")

    try:
        quantidade = alunos.atualizar_curso_preferido(criterio, valor, curso_preferido)
    except mysql.connector.Error as erro:
        print(mensagem_erro(erro))
        return

    if quantidade:
        print(f"Curso preferido atualizado em {quantidade} aluno(s).")

    else:
        print("Nenhum aluno encontardo com esse critério.")


def excluir(alunos):
    print("\n--- Excluir aluno ---")
    criterio, valor = ler_criterio()
    confirma = input("Confirmar exclusão (S/N): ").strip().upper()
    if confirma != "S":
        print("Exclusão cancelada.")
        return 

    try:
        quantidade = alunos.excluir_aluno(criterio, valor)
    except mysql.connector.Error as erro:
        print(mensagem_erro(erro))
        return
    if quantidade:
        print(f"{quantidade} aluno(s) excluído(s).")
    else:
        print("Nenhum aluno encontrado com esse critério.")


def menu(conexao):
    alunos = Alunos(conexao)
    try:
        while True:
            print("\n=== CRUD ALUNOS ===") 
            print("1 - Cadastrar (Create)")  #INSERT INTO
            print("2 - Listar (Read)")    #SELECT
            print("3 - Atualizar curso preferido (Update)")  #UPDATE
            print("4 - Excluir (Delete)")  #DELETE
            print("0. Sair")
            opcao = input('Escolha uma opção: ').strip()

            if opcao == "0":
                print("Encerrando.")
                break
            if opcao == "1":
                cadastrar(alunos)
            elif opcao == "2":
                listar(alunos)
            elif opcao == "3":
                atualizar(alunos)
            elif opcao == "4":
                excluir(alunos)
            else:
                 print('Opção inválida!')
    finally:
        alunos.fechar()
        conexao.close()


if __name__ == "__main__":
    #conexao feita no arquivo principal. Ajuste a senha se o Mysql exigir.

    try:
        conexao = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password="",
            database='cadastro'
        )
        menu(conexao)   
    except mysql.connector.Error as erro:
        print(mensagem_erro(erro)) 
        print("confira se o MySQL está ativo, se o banco cadastro foi importado e se usuario/senha estão corretos")