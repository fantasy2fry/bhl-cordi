class DatabaseHandler:
    def __init__(self, connection):
        self.connection = connection

    def execute_query(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result

    def get_user_data(self, username):
        query = f"SELECT * FROM users WHERE username = '{username}'"
        return self.execute_query(query)
