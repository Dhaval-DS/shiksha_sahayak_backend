import sqlite3

conn = sqlite3.connect('instance/database.db')
c = conn.cursor()

tables = ['teachers', 'school_classes', 'students', 'assignments', 'assignment_submissions', 'attendance_records']

for table in tables:
    c.execute(f"PRAGMA foreign_key_list({table})")
    fks = c.fetchall()
    if fks:
        print(f"\n{table} is connected to:")
        for fk in fks:
            print(f"   - {fk[2]} (via {fk[3]} → {fk[4]})")
    else:
        print(f"\n{table}: no foreign keys")

conn.close()