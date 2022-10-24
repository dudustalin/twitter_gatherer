from db_tools import DBHandler
from tweet_handle import TweetHandle
import queries
import time

# Exemplo de conexão, é necessário preencher os dados
# do banco de dados gerado
conn_data = {
    "host": "localhost",
    "database": "testes",
    "user": 'seu_usuario',
    "password": 'sua_senha'
}

# Exemplos de query e parâmetros adicionais
query = "foo OR bar"
kw = {
    "loc": "pt"
}

db_hand = DBHandler(host=conn_data["host"],
                    database=conn_data["database"],
                    user=conn_data["user"],
                    password=conn_data["password"])
tw_hand = TweetHandle(query=query, **kw)

# Em um primeiro teste o método abaixo não funcionou,
# corretamente, no entanto, é possível (talvez até desejável)
# criar as tabelas à mão copiando e colando a consulta
# CREATE_DATABASE nas ferramentas de query e rodando-a
# db_hand.create_tables(query=queries.CREATE_DATABASE)




def t_record():
    """
    Esta função executará o passo a passo de recuperação do tweet
    até sua gravação nas tabelas
    """
    dic = tw_hand.get_tweet()
    for key, item in dic.items():
        db_hand.feed_database(query=queries.INSERT_TWEET_INFO, args=item)
        check = db_hand.verifier(query=queries.VERIFY_USER, args=item)
        if check:
            db_hand.feed_database(query=queries.UPDATE_TWITTER_USER, args=item)
        else:
            db_hand.feed_database(query=queries.INSERT_TWEET_USER, args=item)
        for mention in item["entities"]["user_mentions"]:
            special_case = {"id_tweet": item["id_tweet"],
                            "hashtag": item["entities"]["hashtags"],
                            "mention_name": mention["name"],
                            "mention_id": mention["id_str"]}
            db_hand.feed_database(query=queries.INSERT_TWEET_ENTITIES, args=special_case)

    # Tive problemas com este método, vou tentar consertá-lo
    # db_hand.terminate()


def loop_twitter(seconds):
    """
    Função recursiva para recuperar os tweets em intervalos de tempo regulares
    :param seconds: tempo em segundos
    :return: None
    """
    try:
        t_record()
        time.sleep(seconds)
    # A exceção abaixo irá imprimir no console a mensagem de erro
    # é possível implementar um alerta, ou um log de erros
    except Exception as error:
        print(error)
    finally:
        loop_twitter(seconds)


if __name__ == '__main__':
    loop_twitter(60)
