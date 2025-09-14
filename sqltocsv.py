import psycopg2
import os

# Connection parameters
DB_NAME = "name-of-ur-dump"
DB_USER = "name-of-ur-user"
DB_PASSWORD = "password-of-your-db"  # Change this!
DB_HOST = "localhost"

# Output directory (change to your preferred folder)
OUTPUT_DIR = "/home/shutdown/pg_exports"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Connect to DB
conn = psycopg2.connect(
    dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST
)
cur = conn.cursor()

# Get all table names in public schema
cur.execute("""
    SELECT tablename FROM pg_tables
    WHERE schemaname = 'public';
""")
tables = [row[0] for row in cur.fetchall()]

for table in tables:
    output_path = os.path.join(OUTPUT_DIR, f"{table}.csv")
    print(f"Exporting {table} to {output_path}")
    sql = f"COPY (SELECT * FROM {table}) TO STDOUT WITH CSV HEADER"
    with open(output_path, "w") as f:
        cur.copy_expert(sql, f)

cur.close()
conn.close()
print("All tables exported!")