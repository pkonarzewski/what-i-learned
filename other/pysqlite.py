# %%
import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
# create_connection("./pythonsqlite.db")

# %%
from contextlib import closing

conn = sqlite3.connect("./pythonsqlite.db")

sql = ["SELECT * FROM test_me", "SELECT 2"]
sql1 = "SELECT * FROM test_me"

first_only = False


def test_bla(conn, sql):
    res = []
    with closing(conn) as conn:
        cursor = conn.cursor()
        with closing(cursor) as cur:
            for sql_statement in sql:
                cur.execute(sql_statement)

            if first_only:
                res.append(cur.fetchone())
            else:
                res.append(cur.fetchall())
    return res


def testz():
    return test_bla(conn, sql1)

testz()

#%%
class TestMe:

    def __init__(self):
        pass

    def get_conn(self):
        return sqlite3.connect("./pythonsqlite.db")

    def _get_sql(self, sql, parameters, first_only=False):
        if isinstance(sql, str):
            sql = [sql]
        parameters = () if parameters is None else parameters

        with closing(self.get_conn()) as conn:
            with closing(conn.cursor()) as cur:
                for sql_statement in sql:
                    cur.execute(sql_statement, parameters)

                if first_only:
                    return cur.fetchone()
                else:
                    return cur.fetchall()

    def get_records(self, sql, parameters=None):
        return self._get_sql(sql, parameters, first_only=True)


bla = TestMe()

print("TEST 1:", bla.get_records('SELECT 1'))

print("TEST 2:", bla.get_records(["select * FROM test_me", "SELECT 2"]))

# %%

print([()] or None)
# %%
ll = []

ll.append(None)

#%%
len(ll)
ll[0]
