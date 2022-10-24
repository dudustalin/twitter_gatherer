# QUERY PARA CRIAR A BASE DE DADOS
# RECOMENDO CRIAR VIA ALGUM SGBD POSTGRESSQL
CREATE_DATABASE = """"
        CREATE TABLE IF NOT EXISTS public.search_type
        (
            search_id integer NOT NULL DEFAULT nextval('search_type_search_id_seq'::regclass),
            date_added date DEFAULT CURRENT_TIMESTAMP,
            date_ended timestamp without time zone,
            search_theme character varying(100) COLLATE pg_catalog."default",
            CONSTRAINT search_type_pkey PRIMARY KEY (search_id)
        );
        
        CREATE TABLE IF NOT EXISTS public.tweet_base
        (
            internal_id integer NOT NULL DEFAULT nextval('tweet_base_internal_id_seq'::regclass),
            date_added date DEFAULT CURRENT_TIMESTAMP,
            search_id integer,
            created_at timestamp without time zone,
            id_tweet character varying(40) COLLATE pg_catalog."default",
            base_text character varying(480) COLLATE pg_catalog."default",
            has_entities boolean,
            reply_to_status boolean,
            reply_to_user boolean,
            user_id character varying(40) COLLATE pg_catalog."default",
            retweets integer,
            CONSTRAINT tweet_base_pkey PRIMARY KEY (internal_id)
        );
        
        CREATE TABLE IF NOT EXISTS public.tweet_entities
        (
            id_tweet character varying(40) COLLATE pg_catalog."default",
            hashtag character varying(80) COLLATE pg_catalog."default",
            mention_name character varying(50) COLLATE pg_catalog."default",
            mention_id character varying(40) COLLATE pg_catalog."default"
        );
        
        CREATE TABLE IF NOT EXISTS public.tweet_users
        (
            user_id character varying(40) COLLATE pg_catalog."default",
            user_name character varying(50) COLLATE pg_catalog."default",
            screen_name character varying(50) COLLATE pg_catalog."default",
            user_location character varying(50) COLLATE pg_catalog."default",
            count_followers integer,
            count_friends integer,
            favorites_count integer,
            statuses_count integer,
            user_source character varying(100) COLLATE pg_catalog."default",
            geo_loc character varying(50) COLLATE pg_catalog."default"
        );
        """

# QUERY QUE INSERE NA TABELA tweet_entities AS ENTIDADES ASSOCIADAS AO TWEET
# SÃO ELAS: HASHTAGS, SÍMBOLOS, MENÇÕES A USUÁRIOS E URLS. AQUI ESCOLHI
# MANTER APENAS HASHTAGS E MENÇÕES AO USUÁRIO
INSERT_TWEET_ENTITIES = """
            INSERT INTO tweet_entities (id_tweet, hashtag, mention_name,mention_id) VALUES 
            (%(id_tweet)s,%(hashtag)s, %(mention_name)s, %(mention_id)s)
            """

# QUERY QYE INSERE AS INFORMAÇÕES BÁSICAS DE CADA TWEET NA TABELA tweet_base
INSERT_TWEET_INFO = """
            INSERT INTO tweet_base (search_id, created_at, id_tweet, 
            base_text, has_entities, reply_to_status, reply_to_user, user_id, retweets) VALUES
            (1, %(created_at)s, %(id_tweet)s, %(base_text)s, %(has_entities)s,
            %(reply_to_status)s, %(reply_to_user)s, %(user_id)s, %(retweets)s);
            """

# QUERY QYE INSERE NA TABELA tweet_users INFORMAÇÕES SOBRE O USUÁRIO QUE
# CRIOU OU RETWEETOU O TWEET
INSERT_TWEET_USER = """
            INSERT INTO tweet_users (user_id, user_name , screen_name, user_location, count_followers,
            count_friends, favorites_count, statuses_count, user_source, geo_loc) VALUES
            (%(user_id)s, %(user_name)s, %(screen_name)s, %(user_location)s, %(count_followers)s,
            %(count_friends)s, %(favorites_count)s, %(statuses_count)s, %(user_source)s, %(geo_loc)s);
            """
# QUERY QUE ATUALIZA AS INFORMAÇÕES DE ALGUM USUÁRIO JÁ EXISTENTE NA TABELA tweet_users
UPDATE_TWITTER_USER = """
            UPDATE 
                tweet_users
            SET 
                user_name = %(user_name)s,
                screen_name = %(screen_name)s,
                user_location = %(user_location)s,
                count_followers = %(count_followers)s,
                count_friends = %(count_friends)s,
                favorites_count = %(favorites_count)s,
                statuses_count = %(statuses_count)s,
                user_source = %(user_source)s,
                geo_loc = %(geo_loc)s
            WHERE 
                user_id = %(user_id)s
            """

# QUERY QUE BUSCA O ID DE UM USUÁRIO NA TABELA tweet_users
VERIFY_USER = """
            SELECT user_id FROM tweet_users WHERE user_id = %(user_id)s::VARCHAR
        """