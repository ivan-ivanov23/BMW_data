import sqlite3
import os

basedir = os.path.abspath(os.path.dirname(__file__))
conn = sqlite3.connect(os.path.join(basedir, 'bmw_data.db'))
cursor = conn.cursor()
# Select 320d from the database
cursor.execute("SELECT * FROM E46 WHERE Modification = '320d'")
print(cursor.fetchall())