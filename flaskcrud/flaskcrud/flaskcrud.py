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
    rv.row_factory = sqlite3.Row
    return rv


# flask provides two contexts: application context and request context
# request variable is request object associated w/ current request
# g is a general purpose variable associated with current application context
# helper function to create database connection for current context, successive
# calls will return already established connection
def get_db():
    # opens new database connection if one does not exist for current application context
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

# this decorator means function is executed every time application context tears down
@app.teardown_appcontext
def close_db(error):
    # closes DB at end of request
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

# flask command to initialize database using predefined schema.sql
def init_db():
    db = get_db()
    # app.open_resource helper function that opens resource and allows you to read from it
    with app.open_resource('schema.sql', mode='r') as f:
        # cursor object has method to execute a script
        # in this case, the schema.sql resource opened above
        db.cursor().executescript(f.read())
    # must commit changes explicitly
    db.commit()

# registers new command with flask script
@app.cli.command('initdb')
def initdb_command():
    # initializes database
    init_db()
    print('Initialized the database.')
