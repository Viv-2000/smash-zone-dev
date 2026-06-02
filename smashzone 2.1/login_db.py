import sqlite3, os


class Login_DB:
    def __init__(self, db_name="login.db"):

        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(base_dir, "data")

        os.makedirs(data_dir, exist_ok=True)
        self.db_path = os.path.join(data_dir, db_name)



    def get_connection(self):
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            return conn
        
        except Exception as e:
            print('database connection error:', e)
            raise




    def create_table(self):
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()

                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS login_db (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        email TEXT NOT NULL UNIQUE,
                    )
                """)
        except Exception as e:
            print('Error creating table:', e)
            raise



    def create_account(self, account):
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO login_db (name, email) VALUES (?, ?)",
                    (account.name, account.email)
                )
                new_id = cursor.lastrowid
                account.id = new_id
                return account.to_dict()

        except sqlite3.IntegrityError:
            return {"error": "This email is already in use..."}
        
        except Exception as e:
            return {"error": f"Some unknown error occured creating the booking: {e}"}

