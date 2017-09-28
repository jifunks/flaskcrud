import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
        render_template, flash


app = Flask(__name__) # create application instance
app.config.from_object(__name__) # load config from this file

# config works similar to dictionary, can be updated w/ new values
app.config.update(dict(
    # in real application, use instance folder
    DATABASE=os.path.join(app.root_path, 'flaskcrud.db'),
    SECRET_KEY='TESTKEY',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKCRUD_SETTINGS', silent=True)
# define config file $FLASKCRUD_SETTINGS and it will be loaded. 

def connect_db():
    # connects to sqlite3 db
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.forw_factory = sqlite3.Row
    return rv

