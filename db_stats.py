#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import datetime
import csv

sqlite_file = 'db.sqlite3'
app_name = 'managers'
column_names = ['city', 'country', 'employment', 'externallink', 'manager', 'season', 'team', 'teamseason']
out_file = 'statistics.csv'

def main():
    """ Main program """
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()

    values = dict()
    values['date'] = str(datetime.datetime.now().date())
    columns = [f"{app_name}_{col}" for col in column_names]
    for col in columns:
        query = f"SELECT COUNT(*) FROM {col}"
        c.execute(query)
        count = c.fetchone()[0]
        values[col] = count

    with open(out_file, 'a') as file:
        writer = csv.DictWriter(file, values.keys())
        writer.writerow(values)
        file.close()
    return 0

if __name__ == "__main__":
    main()