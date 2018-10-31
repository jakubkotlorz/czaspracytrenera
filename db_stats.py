#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import datetime
import csv

sqlite_file = 'db.sqlite3'
app_name = 'managers'
table_names = ['city', 'country', 'employment', 'externallink', 'manager', 'season', 'team', 'teamseason']
out_file = 'statistics.csv'

def main():
    """ Main program """
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    data = [str(datetime.datetime.now().date())]
    for col in table_names:
        query = f"SELECT COUNT(*) FROM {app_name}_{col}"
        c.execute(query)
        count = c.fetchone()[0]
        item = f"{app_name}_{col}:{count}"
        data.append(item)
    line = ';'.join(data)
    print(line)
    return 0

if __name__ == "__main__":
    main()