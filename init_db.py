import sqlite3

def init_db(db_path="database.db"):
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS bookings (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                name        TEXT    NOT NULL,
                email       TEXT    NOT NULL,
                origin      TEXT    NOT NULL,
                destination TEXT    NOT NULL,
                amount      REAL    NOT NULL,
                created     TEXT    NOT NULL
            )
            """
        )
    print("✔ database.db initialised")

if __name__ == "__main__":
    init_db()
