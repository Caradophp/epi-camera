from mysql import connector

class Mysql:
    @staticmethod
    def _getCon():
        return connector.connect(
            host="localhost",
            user="epi_api_user",
            password="123Mudar",
            database="epis"
        )
        
    @staticmethod
    def execute(sql, params=None):
        conn = Mysql._getCon()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(sql, params or ())
            if sql.strip().upper().startswith("SELECT"):
                return cursor.fetchall()
            conn.commit()
            return cursor.lastrowid
        finally:
            cursor.close()
            conn.close()