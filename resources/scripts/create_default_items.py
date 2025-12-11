import csv
import os
from datetime import datetime
from typing import List
from uuid import uuid4

import psycopg

INSERT_ITEM = 'INSERT INTO item (id, "name", created_at, updated_at, deleted_at, created_by, updated_by, workspace_id, unit_of_measurement) values (%s, %s, %s, %s, %s, %s, %s, %s, %s);'
DB_NAME = os.environ.get("DB_NAME", "")
DB_USER = os.environ.get("DB_USER", "")
DB_PASS = os.environ.get("DB_PASS", "")
DB_HOST = os.environ.get("DB_HOST", "127.0.0.1")
DB_PORT = os.environ.get("DB_PORT", "5433")

INPUT_FILE_PATH = "default_items.csv"
PROJECT_ID = "ea8f1004-7537-4b8c-bad5-5f39bfcc78b1"
USER_ID = "10000000-0000-0000-0000-000000000001"
WORKSPACE_ID = "10000000-0000-0000-0000-000000000001"
NOW = datetime.now()


conn = psycopg.connect(f"dbname={DB_NAME} user={DB_USER} password={DB_PASS} host={DB_HOST} port={DB_PORT}")
cursor = conn.cursor()


def load_items_from_file() -> List[dict]:
    with open(INPUT_FILE_PATH, "r") as input_file:
        reader = csv.DictReader(input_file)
        result = []
        for row in reader:
            result.append({
                "id": str(uuid4()),
                "name": row["Material"],
                "unit_of_measurement": row["Unidade"],
            })

    return result


def insert_items(items: List[dict]):
    for item in items:
        # id, "name", created_at, updated_at, deleted_at, created_by, updated_by, workspace_id, unit_of_measurement
        item_to_insert = (item["id"], item["name"], NOW, NOW, None, USER_ID, USER_ID, WORKSPACE_ID, item["unit_of_measurement"])
        cursor.execute(INSERT_ITEM, item_to_insert)
        print(f'insert {item["name"]} - {item["unit_of_measurement"]}')

    conn.commit()


def main():
    items = load_items_from_file()
    insert_items(items)


if __name__ == '__main__':
    main()
