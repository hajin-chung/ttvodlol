from flask import Flask, request
import db
from downloader.download import download_vod
import sqlite3
import twitch
import utils


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
conn = sqlite3.connect("ttvodlol.sqlite", check_same_thread=False)
conn.row_factory = utils.dict_factory


@app.route('/')
def ping():
  return {"msg": "hi"}


@app.route('/status')
def status():
  return {
    "db": utils.check_conn(conn)
  }


@app.post('/register')
def register_channel():
  req = request.get_json()
  channel_id = req['channel_id']
  channel_name = req['channel_name']
  try:
    db.register_channel(conn, channel_id, channel_name)
    # TODO: register to web socket
    return {
      "success": True
    }
  except Exception as e:
    print("[Err] error on register_channel\n[Exception] ", e)
    return {
      "success": False
    }
    

@app.get('/channel/list')
def get_channel_list():
  try:
    channel_list = db.get_channel(conn)
    return {
      "success": True,
      "list": channel_list
    }
  except Exception as e:
    print("[Err] error on get channel list\n[Exception] ", e)
    return {
      "success": False
    }


@app.get('/channel/<channel_id>/list')
def get_vod_list(channel_id):
  try:
    vod_list = db.get_vod_in_channel(conn, channel_id) 
    return {
      "success": True,
      "list": vod_list
    }
  except Exception as e:
    print("[Err] error on get vod list\n[Exception] ", e)
    return {
      "success": False
    }


@app.post('/download/channel/<channel_id>')
def download_channel(channel_id):
  try:
    vod_data = twitch.get_channel_vod(channel_id)
    vod_list = vod_data['data']
    print("[INFO:2] vod list", vod_list)
    for vod_info in vod_list:
      vod_id = vod_info['id']
      channel_name = vod_info['user_name']
      title = vod_info['title']
      thumbnail_url = vod_info['thumbnail_url']
      created_at = vod_info['created_at']
      vod_exists = db.check_vod(conn, vod_id) 

      if vod_exists: 
        print(f"[INFO:2] {vod_id}:{title} already downloaded")
        continue

      print(f"[INFO:2] queued {vod_id}")
      # update db
      db.queue_vod(conn, vod_id, channel_id, channel_name, title, thumbnail_url, created_at)

    return {
      "success": True, "vod_list": vod_list
    }
  except Exception as e:
    print("[Err] app.py > download_channel() ", e)
    return {
      "success": False
    }


@app.post('/download/vod/<vod_id>')
def request_vod_download(vod_id):
  try:
    vod_data = twitch.get_vod(vod_id)
    vod_info = vod_data['data']
    channel_id = vod_info['user_id']
    channel_name = vod_info['user_name']
    title = vod_info['title']
    thumbnail_url = vod_info['thumbnail_url']
    created_at = vod_info['created_at']
    vod_exists = db.check_vod(conn) 

    if vod_exists: 
      return {"error": False, "msg": "vod already exists"}

    print(f"[INFO:2] queued {vod_id}")
    # update db
    db.queue_vod(conn, vod_id, channel_id, channel_name, title, thumbnail_url, created_at)

    return {"error": False, "vod_info": vod_info}
  except Exception as e:
    print("[Err] app.py > download_vod() ", e)
    return {"success": False}


@app.get('/vod/<vod_id>')
def get_vod(vod_id):
  # TODO: fetch vod info from db & url from s3
  pass

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=80, debug=False)