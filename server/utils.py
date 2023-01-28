def check_conn(db):
  try:
    db.cursor()
    return True
  except Exception as e:
    print("[Err] on db check", e)
    return False

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d