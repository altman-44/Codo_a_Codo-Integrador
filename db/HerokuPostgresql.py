import psycopg2
import psycopg2.extras # Para poder tratar las filas del resultado obtenido de la query a la db como Dictionaries (en vez de acceder a empleado[1], podemos acceder a empleado['name'])

class HerokuPostgresql():
    __databaseUrl = ''

    def __init__(self, url):
        self.__databaseUrl = url
    
    def connect(self):
        return HerokuPostgresqlConnection(psycopg2.connect(self.__databaseUrl, sslmode='require'))

class HerokuPostgresqlConnection():
    __connection = ''

    def __init__(self, connection):
        self.__connection = connection

    def cursor(self):
        return self.__connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def commit(self):
        return self.__connection.commit()

    def close(self):
        return self.__connection.close()