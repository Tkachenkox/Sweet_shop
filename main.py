# -*- coding: utf-8 -*-
from datetime import datetime
from flask import Flask, render_template, request
import db

app = Flask(__name__)

def insert_db(type_c, price, date, term):
    data = db.Database('db.sql')
    data.insert(type_c, price, date, term)
    data.close_conn()

def get_db():
    data = db.Database('db.sql')
    rows = data.fetch()
    data.close_conn()
    return rows

def get_max():
    data = db.Database('db.sql')
    rows = data.get_max()
    data.close_conn()
    return rows

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
@app.route('/index', methods=['POST'])
def get_values():
    type_c = request.form['type']
    price = float(request.form['price'])
    date = request.form['date']
    term = int(request.form['term'])
    insert_db(type_c, price, date, term)
    return index()

@app.route('/list')
def get_list():
    rows = get_db()
    objs = []
    for i in rows:
        obj = {
                'type': i[0],
                'price': i[1],
                'date': i[2],
                'terms': i[3]
        }
        objs.append(obj)
    out_term = []
    for i in rows:
        date = i[2].split('.')
        date1 = str(date[2]) + '-' + str(date[1]) + '-' + str(date[0])
        date = datetime.strptime(date1, "%Y-%m-%d").date()
        cur_d = datetime.now().date()
        delta = cur_d - date
        if int(str(delta).split()[0]) > i[3]:
            obj = {
                    'type': i[0],
                    'price': i[1],
                    'date': i[2],
                    'terms': i[3]
            }
            out_term.append(obj)
    rows = get_max()
    obj = {
            'type': rows[0],
            'price': rows[1],
            'date': rows[2],
            'terms': rows[3]
    }
    return render_template('simple_list.html', obs = objs, objs=out_term, m_p=obj)
app.run()