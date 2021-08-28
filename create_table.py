import psycopg2
from config import config


def create_tables():
    """ Creates PostgreSQL tables of trade executions
        and historical candles"""
    commands = (
        """
        CREATE TABLE IF NOT EXISTS trade_executions (
            id BIGSERIAL PRIMARY KEY,
            time TIMESTAMPTZ NOT NULL,
            pair TEXT NOT NULL,
            trade_id INTEGER UNIQUE NOT NULL,
            price NUMERIC NOT NULL,
            size NUMERIC NOT NULL,
            side TEXT NOT NULL,
            liquidation BOOLEAN NOT NULL
        );
        """,        
        """
        CREATE TABLE IF NOT EXISTS candles (
            id BIGSERIAL PRIMARY KEY,
            time TIMESTAMPTZ UNIQUE NOT NULL,
            pair TEXT NOT NULL,
            open NUMERIC NOT NULL,
            high NUMERIC NOT NULL,
            low NUMERIC NOT NULL,
            close NUMERIC NOT NULL,
            volume NUMERIC NOT NULL,
            interval INTEGER NOT NULL
        );
        """)

    conn = None
    try:
        params = config()

        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        for command in commands:
            cur.execute(command)

        cur.close()
        conn.commit()
    except Exception as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    create_tables()