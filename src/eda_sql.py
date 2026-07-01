#==================================================================================================================================================================
#                          EXPLORATORY DATA ANALYSIS USING SQL
#==================================================================================================================================================================

from sqlalchemy import create_engine
import pandas as pd
import sqlite3

#creating connection

con = sqlite3.connect("my_data1.db")
cur = con.cursor()

engine = create_engine('sqlite:///mydatabase.db')
conn = sqlite3.connect('mydatabase.db')
df.to_sql("SPACEXTBL", conn, if_exists='replace', index=False, method="multi")

df1.to_sql("SPACEXTBL", conn, if_exists='replace', index=False, method="multi")
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS SPACEXTABLE;")
cur.execute("CREATE TABLE SPACEXTABLE AS SELECT * FROM SPACEXTBL WHERE Date IS NOT NULL;")
conn.commit() # Commit the changes to the database
print("Table SPACEXTABLE created successfully, filtering out null dates.")

cur.execute("select * from SPACEXTABLE limit 5")
rows = cur.fetchall()
for row in rows:
    print(row)
conn.commit()

cur.execute("""SELECT LandingPad, COUNT(Outcome) AS NumberOfSuccesses FROM SPACEXTABLE WHERE Outcome IN ('True ASDS', 'True RTLS', 'True Ocean') GROUP BY LandingPad;""")

success_by_landing_pad = cur.fetchall()

print("Number of successful landings grouped by LandingPad:")
for row in success_by_landing_pad:
    print(f"LandingPad: {row[0]}, Successes: {row[1]}")
