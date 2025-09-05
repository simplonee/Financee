import sqlite3

con = sqlite3.connect('test.db')
cur = con.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS daily
            (sku text PRIMARY KEY, name text, size text, price real)''')

cur.execute('''INSERT OR IGNORE INTO daily VALUES
            ('SKU123', 'BACK LOGO', 'Medium', '19.99')''')
        
con.commit()

for row in cur.execute('''SELECT * FROM daily'''):
    print(row)