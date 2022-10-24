import requests
import os


class TweetHandle:
    def __init__(self, query: str,  **kwargs):
        """
        Cria um dicionário com os tweets recuperados que se ajusta ao
        modelo utilizado no banco de dados

        **IMPORTANTE**
        É fundamental ler a documentação da API do Twitter
        Utilizei a API 1.1 para construir o script, não funciona
        para a API 2.0. Acesse o link a seguir para verificar como
        montar buscas elaboradas

        https://developer.twitter.com/en/docs/twitter-api/v1

        :param query:
        Uma string contendo a palavra a ser procurada

        Para procurar tweets com ao menos uma de um
        grupo de palavras use o operador OR entre as
        palavras

        Para procurar tweets em que ocorrem exatamente
        as palavras em um conjunto de palavras use o
        operador AND. Por exemplo:

        'esporte OR lazer' retornará tweets que contém
        ou 'esporte', ou 'lazer', ou ambas

        'esporte AND lazer' retornará apenas os tweets
        em que ambas as palavras ocorrem


        :param kwargs:
        um dicionário contendo outros parâmetros de pesquisa,
        conforme pode ser visto em

        https://developer.twitter.com/en/docs/twitter-api/v1/rules-and-filtering/search-operators

        """
        self.url = os.environ['URL']
        self.api_key = os.environ['API_KEY']
        self.k_secret = os.environ['API_KEY_SECRET']
        self.b_token = os.environ['API_BEARER_TOKEN']
        self.params = {key: item for key, item in kwargs.items()}
        self.params["q"] = query
        self.header = {
            "Authorization": f"Bearer {self.b_token}"
        }

    def concat_dic(self, key, *args):
        """
        Função desenhada apenas para aglutinar alguns itens
        No caso, a função é utilizada para transformar todas
        hashtags de um tweet em uma única string. Pode ser
        utilizada para algutinar outras porções que sejam do
        interesse do usuário, por exemplo, usuários mencionados,
        símbolos, entre outros

        :param key: a chave do texto a ser aglutinado
        :param args:
        :return: string aglutinada, por exemplo '#emoção, #ballet, '
        """
        if not args:
            string = ""
            for dic in args:
                string += dic[key] + ","
            return string
        else:
            pass

    def get_tweet(self):
        """
        Recupera os tweets recentes de acordo com a documentação
        da API 1.1 do twitter

        :return: dicionário contendo os tweets mais recentes de acordo com
        a busca
        """
        req = requests.get(url=self.url, params=self.params, headers=self.header)
        print(req.raise_for_status())

        # print(req.text)

        dic = {}

        for i in req.json()["statuses"]:
            dic[i["id_str"]] = {
                "id_tweet": i["id_str"],
                "base_text": i["text"],
                "created_at": i["created_at"],
                "has_entities": any([any(item) for key, item in i["entities"].items()]),
                "reply_to_status": True if (i["in_reply_to_status_id"] is not None) else False,
                "reply_to_user": True if (i["in_reply_to_user_id"] is not None) else False,
                "user_id": i["user"]["id"],
                "user_name": i["user"]["name"],
                "screen_name": i["user"]["screen_name"],
                "user_location": i["user"]["location"],
                "count_followers": i["user"]["followers_count"],
                "count_friends": i["user"]["friends_count"],
                "statuses_count": i["user"]["statuses_count"],
                "user_source": "",
                "geo_loc": i["geo"],
                "retweets": i["retweet_count"],
                "favorites_count": i["favorite_count"],
                "entities": {
                    "user_mentions": i["entities"]["user_mentions"],
                    "hashtags": self.concat_dic("text", i["entities"]["hashtags"])
                }
            }
        return dic
