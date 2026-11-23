import mysql.connector

class Alunos:
    def __init__(self, conexao):
        self.conexao = conexao
        self.cursor = conexao.cursor()

    def criar(self, nome, profissao, nascimento, sexo, peso, altura, nacionalidade, Curso_preferido):
        nome = f'"{nome}"'
        profissao = "NULL" if profissao is None else f'"{profissao}"'
        nascimento = "NULL" if nascimento  is None else f'"{nascimento}"'
        sexo = "NULL" if sexo is None else f'"{sexo}"'
        peso = "NULL" if peso is None else peso
        altura = "NULL" if altura is None else altura
        nacionalidade = "NULL" if nacionalidade is None else f'"{nacionalidade}"'
        Curso_preferido = "NULL" if Curso_preferido is None else Curso_preferido

        comando = f""" 
            INSERT INTO alunos
                (nome, profissao, nascimento, sexo, peso,altura,
                nacionalidade, Curso_preferido)
            VALUES
                ({nome}, {profissao}, {nascimento}, {sexo}, {peso},
                {altura}, {nacionalidade}, {Curso_preferido})
        """

        self.cursor.execute(comando)
        self.conexao.commit()
        return self.cursor.lastrowid

    def listar_alunos(self):
        comando = """
            SELECT id, nome, profissao, nascimento, sexo, peso,
            altura, nacionalidade, Curso_preferido
            FROM ALUNOS 
            ORDER BY id
            """
        self.cursor.execute(comando)
        return self.cursor.fetchall()
    
    def atualizar_curso_preferido(self, criterio, valor, Curso_preferido):
        if criterio == "id":
            comando = f"UPDATE alunos SET Curso_preferido = {Curso_preferido} WHERE id = {valor}"
        elif criterio == "nome":
            comando = f'UPDATE alunos SET Curso_preferido = {Curso_preferido} WHERE nome = "{valor}"'
        else: 
            raise ValueError("Critério inválido. Use id ou nome.")

        self.cursor.execute(comando)
        self.conexao.commit()
        return self.cursor.rowcount
    
    def excluir_aluno(self, criterio, valor):
        if criterio == "id":
            comando = f"DELETE FROM alunos WHERE id = {valor}"
        elif criterio == "nome":
            comando = f'DELETE FROM  alunos WHERE nome = "{valor}"'
        else:
            raise ValueError("Critério inválido. Use id ou nome.")

        self.cursor.execute(comando)
        self.conexao.commit()
        return self.cursor.rowcount
    
    def fechar(self):
        self.cursor.close()

def mensagem_erro(erro):
    if isinstance(erro, mysql.connector.IntegrityError) and erro.errno == 1452:
        return "Curso preferido inválido. Informe um idcurso que exista na tabela cursos."
    return f"Erro no banco de dados: {erro}"

