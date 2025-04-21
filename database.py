import sqlite3

def init_db():
    conn = sqlite3.connect("games.db")
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player1 TEXT,
            player2 TEXT,
            moves TEXT,
            winner TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_game(player1, player2, moves, winner):
    conn = sqlite3.connect("games.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO games (player1, player2, moves, winner) VALUES (?, ?, ?, ?)",
                (player1, player2, moves, winner))
    conn.commit()
    conn.close()
