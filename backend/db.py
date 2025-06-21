
import mysql.connector
from flask import g

def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(
            host="db", user="root", password="example", database="ndis"
        )
    return g.db
