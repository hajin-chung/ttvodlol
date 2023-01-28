from downloader.download import download_vod
import time
import sqlite3
import utils

conn = sqlite3.connect("ttvodlol.sqlite", check_same_thread=False)
conn.row_factory = utils.dict_factory

queue_query = """
  SELECT id FROM vod WHERE queue=1;
"""

update_queue_query = """
  UPDATE vod SET queue=0 WHERE id=?;
"""

update_error_queue_query = """
  UPDATE vod SET queue=500 WHERE id=?;
"""

def check_queue(conn):
  cur = conn.cursor()
  cur.execute(queue_query)
  rows = cur.fetchall()
  cur.close()
  return rows

def update_queue(conn, vod_id):
  cur = conn.cursor()
  cur.execute(update_queue_query, (vod_id, ))
  conn.commit()
  cur.close()

def update_error_queue(conn, vod_id):
  cur = conn.cursor()
  cur.execute(update_error_queue, (vod_id, ))
  conn.commit()
  cur.close()

def main():
  while True:
    print("[INFO:2] Checking queue...")
    queue = check_queue(conn)
    print(f"[INFO:2] {len(queue)} vod(s) in queue")
    print(queue)
    for vod in queue:
      vod_id = vod['id']
      try:
        print(f"[INFO:2] starting {vod_id} download")
        download_vod(vod_id)
        print(f"[INFO:2] {vod_id} success")
        update_queue(conn, vod_id)
      except Exception as e:
        update_error_queue(conn, vod_id)
        print("[Err] main() ", e)

    time.sleep(60)

if __name__ == "__main__":
  main()