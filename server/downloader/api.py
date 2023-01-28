from urllib.parse import quote
import requests


def get_playback_token(vod_id):
  try:
    data = """{{"operationName":"PlaybackAccessToken","variables":{{"isLive":false,"login":"","isVod":true,"vodID":"{0}","playerType":"channel_home_live"}},"extensions":{{"persistedQuery":{{"version":1,"sha256Hash":"0828119ded1c13477966434e15800ff57ddacf13ba1911c129dc2200705b0712"}}}}}}""".format(vod_id)
    headers = {
      'Client-Id': 'kimne78kx3ncx6brgo4mv6wki5h1ko',
      'Content-Type': 'text/plain',
      'Authorization': 'OAuth p755fb6rwziuih50ll4bslb60eahrf'
    }
    res = requests.post("https://gql.twitch.tv/gql", data=data, headers=headers)
    data = res.json()
    sig = data['data']['videoPlaybackAccessToken']['signature']
    token = quote(data['data']['videoPlaybackAccessToken']['value'])
    print(f"[INFO:2] get playback token {token}")
    return {'sig': sig, 'token': token}
  except Exception as e:
    print("[Err] api.py > get_playback_token() ", e)


def get_master_m3u8_content(vod_id, sig, token):
  try:
    url = f"https://usher.ttvnw.net/vod/{vod_id}.m3u8?sig={sig}&token={token}&allow_source=true"
    res = requests.get(url)
    return res.text
  except Exception as e:
    print("[Err] api.py > get_master_m3u8_content() ", e)

