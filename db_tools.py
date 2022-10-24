import psycopg2


class DBHandler:
    def __init__(self, host, database, user, password):
        """
        Funciona apenas com bancos de dados POSTGRESSQL

        Executa todas as funções necessárias para a inserção
        dos tweets recuperados nas tabelas que serão criadas

        :param host: hostname do servidor
        :param database: nome da base de dados
        :param user: nome do usuário
        :param password: senha do usuário
        """
        self.conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password)
        self.cur = self.conn.cursor()

    def create_tables(self, query):
        """
        Cria a base de dados a ser utilizada
        :param query: Consulta de criação das tabelas
        :return:
        """
        self.cur.execute(query)
        self.conn.commit()

    def feed_database(self, query, args):
        """
        Alimenta a base de dados com uma consulta
        :param query: consulta a ser realizada
        :param args: dicionário com os parâmetros a serem
        modificados na consulta
        :return:
        """
        self.cur.execute(query, args)
        self.conn.commit()

    def incremental_feed(self, query, args):
        for data in args:
            self.feed_database(query, data)

    def verifier(self, query, args):
        """
        Verifica se uma query realizada trouze ou não resultado,
        não trazendo, a função é encerrada

        :param query: Consulta a ser realizada
        :param args: dicionário com os parâmetros a serem
        modificados na consulta
        :return: booleano
        """
        check = self.cur.execute(query, args)
        if check is not None:
            return True
        else:
            return False

    def terminate(self):
        """
        Fecha conexão e cursor
        :return: None
        """
        self.cur.close()
        self.conn.close()
