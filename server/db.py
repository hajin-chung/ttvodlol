import sqlite3

create_live_table_sql = """
  DROP TABLE IF EXISTS live;
  CREATE TABLE live (
    channel_login TEXT PRIMARY KEY,
    working_on TEXT NOT NULL
  );
"""

create_channel_table_sql = """
  DROP TABLE IF EXISTS channel;
  CREATE TABLE channel (
    channel_id TEXT PRIMARY KEY,
    channel_name TEXT NOT NULL
  );
"""

create_vod_table_sql = """
  DROP TABLE IF EXISTS vod;
  CREATE TABLE vod (
    id TEXT PRIMARY KEY,
    channel_id STRING NOT NULL,
    channel_name STRING NOT NULL,
    title STRING,
    thumbnail_url STRING,
    created_at STRING,
    queue INTEGER
  );
"""

register_new_channel_sql = """
  INSERT INTO channel VALUES (?, ?);
"""

get_vod_in_channel_sql = """
  SELECT * FROM vod WHERE channel_id=?;
"""

get_channel_list_sql = """
  SELECT * FROM channel;
"""

check_vod_exists_sql = """
  SELECT * FROM vod WHERE id=?;
"""

queue_vod_sql = """
  INSERT INTO vod(id, channel_id, channel_name, title, thumbnail_url, created_at, queue) VALUES (?, ?, ?, ?, ?, ?, 1)
"""

insert_vod_sql = """
  INSERT INTO vod(id, channel_id, channel_name, title, thumbnail_url, created_at, queue) VALUES (?, ?, ?, ?, ?, ?, 0)
"""

def register_channel(conn, channel_id, channel_name): 
  cur = conn.cursor()
  cur.execute(register_new_channel_sql, (channel_id, channel_name))
  conn.commit()
  cur.close()

def get_vod_in_channel(conn, channel_id):
  cur = conn.cursor()
  cur.execute(get_vod_in_channel_sql, (channel_id, ))
  rows = cur.fetchall()
  cur.close()
  return rows

def get_channel(conn):
  cur = conn.cursor()
  cur.execute(get_channel_list_sql)
  rows = cur.fetchall()
  cur.close()
  return rows

def check_vod(conn, vod_id):
  cur = conn.cursor()
  cur.execute(check_vod_exists_sql, (vod_id, ))
  rows = cur.fetchall()
  cur.close()
  print(rows)
  if (len(rows) == 0): return False
  return True

def queue_vod(conn, vod_id, channel_id, channel_name, title, thumbnail_url, created_at):
  cur = conn.cursor()
  cur.execute(queue_vod_sql, (vod_id, channel_id, channel_name, title, thumbnail_url, created_at))
  conn.commit()
  cur.close()

def insert_vod(conn, vod_id, channel_id, channel_name, title, thumbnail_url, created_at):
  cur = conn.cursor()
  cur.execute(insert_vod_sql, (vod_id, channel_id, channel_name, title, thumbnail_url, created_at))
  conn.commit()
  cur.close()

def init_live():
  print("Initializing live table ...")
  db = sqlite3.connect("ttvodlol.sqlite")
  db.executescript(create_live_table_sql)
  print("done")

def init_channel():
  print("Initializing channel table ...")
  db = sqlite3.connect("ttvodlol.sqlite")
  db.executescript(create_channel_table_sql)
  print("done")

def init_vod():
  print("Initializing vod table ...")
  db = sqlite3.connect("ttvodlol.sqlite")
  db.executescript(create_vod_table_sql)
  print("done")

def test_query():
  conn = sqlite3.connect("ttvodlol.sqlite", check_same_thread=False)
  query = input("query: ")
  cur = conn.cursor() 
  cur.execute(query)
  rows = cur.fetchall()
  print(rows)

def main():
  print("==========[ ttvodlol db setup ]==========")
  option = 0
  print("1) initialize all tables")
  print("2) initialize only live download table")
  print("3) initialize only registered channel table")
  print("4) initialize only vod table")
  print("5) test queries")
  option = int(input())

  if option == 1:
    init_live()
    init_channel()
    init_vod()
  elif option ==2:
    init_live()
  elif option == 3:
    init_channel()
  elif option == 4:
    init_vod()
  elif option == 5:
    test_query()
  else:
    print("[Err] invalid option")

if __name__ == "__main__":
  main()