import os
import sqlite3

from flask import Flask, request, session, g, redirect, url_for,abort, render_template, flash

app = Flask(__name__)
app.config.from_object(__name__)  #从当前文件下加载config

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'), #app.root_path app's path
    SECRET_KEY='development key',

    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode = 'r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    init_db()
    print('Initialized the database.')

def get_db():
    if not hasattr(g, 'sqlite_db'):     #g 与当前应用 上下文有关的 通用变量
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext   #装饰器 会在每次应用环境销毁时调用。
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


