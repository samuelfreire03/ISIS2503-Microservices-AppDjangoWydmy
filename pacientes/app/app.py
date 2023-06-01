from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask_mysqldb import MySQL

import psycopg2
from psycopg2 import DatabaseError

app = Flask(__name__)

@app.route('/')
def index():
    # return "<h1>UskoKruM2010 - Suscríbete!</h1>"
    cursos = ['PHP', 'Python', 'Java', 'Kotlin', 'Dart', 'JavaScript']
    data = {
        'titulo': 'Index123',
        'bienvenida': '¡Saludos!',
        'cursos': cursos,
        'numero_cursos': len(cursos)
    }
    return render_template('index.html', data=data)


@app.route('/contacto/<nombre>/<int:edad>')
def contacto(nombre, edad):
    data = {
        'titulo': 'Contacto',
        'nombre': nombre,
        'edad': edad
    }
    return render_template('contacto.html', data=data)


@app.route('/cursos')
def listar_cursos():

    rows = []
    
    try:
        connection = psycopg2.connect(
            host='10.128.0.25',
            port='5432',
            user='variables_user',
            password='Isis2503',
            database='variables_db'
        )

        print("Conexión exitosa.")
        cursor = connection.cursor()
        cursor.execute("SELECT version()")
        row = cursor.fetchone()
        print("Versión del servidor de PostgreSQL: {}".format(row))
        cursor.execute("SELECT * FROM curso")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    except DatabaseError as ex:
        print("Error durante la conexión: {}".format(ex))
    finally:  # Se cerró la conexión a la BD.
        print("La conexión ha finalizado.")
    return jsonify(rows)


def pagina_no_encontrada(error):
    # return render_template('404.html'), 404
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(debug=True,host="0.0.0.0", port=8080)
