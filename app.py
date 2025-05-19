from flask import Flask, request, redirect, render_template, flash
from flask_mysqldb import MySQL
import random, string

app = Flask(__name__)
app.secret_key = 'abcxyz'

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Vidhan@123'
app.config['MYSQL_DB'] = 'tinyurl_db'

mysql = MySQL(app)

# Generate short code
def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        long_url = request.form['long_url']
        short_code = generate_short_code()

        # Ensure uniqueness
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM urls WHERE short_code = %s", (short_code,))
        while cur.fetchone():
            short_code = generate_short_code()

        # Insert into DB
        cur.execute("INSERT INTO urls (long_url, short_code) VALUES (%s, %s)", (long_url, short_code))
        mysql.connection.commit()
        cur.close()

        short_url = request.host_url + short_code
        flash(f'Short URL: {short_url}')
        return redirect('/')

    return render_template('index.html')

@app.route('/<short_code>')
def redirect_to_long_url(short_code):
    cur = mysql.connection.cursor()
    cur.execute("SELECT long_url FROM urls WHERE short_code = %s", (short_code,))
    result = cur.fetchone()
    cur.close()

    if result:
        return redirect(result[0])
    else:
        return 'URL not found', 404

if __name__ == '__main__':
    app.run(debug=True)
