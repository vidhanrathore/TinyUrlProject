from . import mysql

def insert_url(long_url, short_code):
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO urls (long_url, short_code) VALUES (%s, %s)", (long_url, short_code))
    mysql.connection.commit()
    cur.close()

def get_long_url(short_code):
    cur = mysql.connection.cursor()
    cur.execute("SELECT long_url FROM urls WHERE short_code = %s", (short_code,))
    result = cur.fetchone()
    cur.close()
    return result

def is_short_code_exists(short_code):
    cur = mysql.connection.cursor()
    cur.execute("SELECT 1 FROM urls WHERE short_code = %s", (short_code,))
    exists = cur.fetchone() is not None
    cur.close()
    return exists