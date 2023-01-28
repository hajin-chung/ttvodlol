import requests
import os

CLIENT_ID = os.environ.get('TWITCH_CLIENT_ID')
CLIENT_SECRET = os.environ.get('TWITCH_CLIENT_SECRET')


def get_token():
  # TODO: check token alive
  data = {
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
    'grant_type': 'client_credentials'
  }
  headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
  }

  # test mode
  # return "z0x2zzpyqmzi0h6jg9t1ewmgst68gl"
  
  try:
    res = requests.post("https://id.twitch.tv/oauth2/token", data=data, headers=headers)
    json = res.json()
    print(f"[DEBUG] get token json ", json)
    token = json['access_token']
    print(f"[INFO:2] twitch server api token {token}")
    return token
  except Exception as e:
    print("[Err] twitch.py > get_token() ", e)


def get_channel_vod(channel_id):
  token = get_token()
  headers = {
    'Authorization': f"Bearer {token}",
    'Client-Id': CLIENT_ID
  }
  
  try:
    res = requests.get(f"https://api.twitch.tv/helix/videos?user_id={channel_id}", headers=headers)
    json = res.json()
    return json
  except Exception as e:
    print("[Err] twitch.py > get_channel_vod() ", e)


def get_vod(vod_id):
  token = get_token()
  headers = {
    'Authorization': f"Bearer {token}",
    'Client-Id': CLIENT_ID
  }
  
  try:
    res = requests.get(f"https://api.twitch.tv/helix/videos?id={vod_id}", headers=headers)
    json = res.json()
    return json
  except Exception as e:
    print("[Err] twitch.py > get_vod() ", e)


def search_channel(query):
  token = get_token()
  headers = {
    'Authorization': f"Bearer {token}",
    'Client-Id': CLIENT_ID
  }

  try:
    res = requests.get(f"https://api.twitch.tv/helix/search/channels?query={query}", headers=headers)
    json = res.json()
    return json
  except Exception as e:
    print("[Err] twitch.py > search_channel() ", e)
  

if __name__ == "__main__":
  print("env variables ", CLIENT_ID, CLIENT_SECRET)
  query = input("search query: ")
  search_result = search_channel(query)
  print(search_result)
  channel_id = input("channel id: ")
  vod_result = get_channel_vod(channel_id)
  print(vod_result)