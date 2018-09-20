import psycopg2 as pg
from psycopg2.extras import RealDictCursor


from user_api.config.config import ProductionConfig, BaseConfig, TestingConfig, DevelopmentConfig
from user_api.utils.singleton import Singleton


class DatabaseConnection(metaclass=Singleton):
    """
    Database connection class
    Handles all database related issues
    """
    __conn = None
    schema = ProductionConfig.SCHEMA_PRODUCTION

    class DbConnection(object):
        """
        Class creates connection object
        and sets autocommit to false
        """
        def __init__(self, schema):
            self.schema = schema
            self.conn = pg.connect(database=BaseConfig.DATABASE,
                                   DATABASE_URL=BaseConfig.DATABASE_URL,
                                   user=BaseConfig.USER,
                                   password=BaseConfig.PASSWORD,
                                   host=BaseConfig.HOST,
                                   port=BaseConfig.PORT,
                                   cursor_factory=RealDictCursor,
                                   options=f'-c search_path={self.schema}')
            self.conn.autocommit = False

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.conn.close()

    def init_db(self, app):
        """
        Provides a database connection object
        :param app:
        :return:
        """
        if app.config['TESTING']:
            self.schema = TestingConfig.SCHEMA_TESTING
            self.__conn.autocommit = True

        else:
            self.schema = DevelopmentConfig.SCHEMA_PRODUCTION

        try:
            if not self.__conn:
                self.__conn = self.DbConnection(self.schema).conn

        except pg.DatabaseError as ex:
            print("Error: " + str(ex))

    def insert(self, table, data):
        """
        handle all insertions into the database
        :param table:
        :param data:
        :return:
        """
        if not table or not data or not isinstance(data, dict):
            return False
        columns = tuple(data.keys())
        values = tuple(data.values())

        _top = f"""INSERT INTO {self.schema}.{table} ("""

        cols = ", ".join([f""" "{n}" """ for n in columns])

        middle = """) VALUES ("""

        val = ", ".join([f""" '{v}' """ for v in values])

        bottom = """)"""

        sql = _top + cols + middle + val + bottom

        cur = self.__conn.cursor()
        cur.execute(sql)
        self.__conn.commit()
        if cur:
            return cur
        return None

    def find(self, name_of_table, criteria=None, join=None):
        """
        handles all queries to retrieve data
        :param name_of_table:
        :param criteria:
        :param join:
        :return:
        """
        sql = ""
        if not criteria and not join:
            sql = f"""SELECT * FROM {self.schema}.{name_of_table}"""
        else:
            if criteria and not join:
                columns = tuple(criteria.keys())
                values = tuple(criteria.values())
                top1 = f"""SELECT * FROM {self.schema}.{name_of_table} WHERE ("""

                if len(columns) == 1:
                    crit = f""" "{columns[0]}"='{values[0]}' )"""
                else:
                    crit = " AND ".join([f""" "{k}" = '{v}' """ for k, v in
                                         criteria.items()]) + """)"""

                sql = top1 + crit
            else:
                pass
        cur = self.__conn.cursor()
        cur.execute(sql)
        self.__conn.commit()
        if cur:
            val = cur.fetchall()
            if len(val) == 1:
                return val[0]
            elif len(val) > 1:
                return val
        return None

    def update(self, table_name, selection, update):
        """
        Handles update queries
        :param table_name:
        :param selection:
        :param update:
        :return:
        """

        _top = f"""UPDATE {self.schema}.{table_name} SET """

        vals = ", ".join([f""" "{col1}"='{val1}' """ for col1, val1 in update.items()])

        middle = """ WHERE """

        cols = " AND ".join([f""" "{col}"='{val}' """ for col, val in selection.items()])

        sql = _top + vals + middle + cols

        cur = self.__conn.cursor()
        cur.execute(sql)
        self.__conn.commit()
        if cur:
            return cur
        return None

    def delete(self, table_name, selection):
        """
        handles delete queries
        :param table_name:
        :param selection:
        :return:
        """
        _top = f"""DELETE FROM {self.schema}.{table_name} WHERE """

        cols = " AND ".join([f""" "{col}"='{val}' """ for col, val in selection.items()])

        sql = _top + cols

        cur = self.__conn.cursor()
        cur.execute(sql)
        self.__conn.commit()
        if cur:
            return cur
        return None

    def drop_test_schema(self):
        """
        delete test schema after using it
        :return:
        """
        cur = self.__conn.cursor()
        cur.execute("""DELETE FROM tests.user""")
        self.__conn.commit()