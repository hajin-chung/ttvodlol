from . import api, parser, s3
import requests


# downloads actual vod to s3
# TODO: use threads
def download_vod(vod_id):
  # if so, parse m3u8 and find biggest bandwidth, set this as target 
  # save target to s3::/channel_login/video_id/target.m3u8 
  # parse target.m3u8 download ts files (feature: can use queue), 
  #   upload ts file to s3::/channel_login/video_id/*.ts

  # process to get target m3u8
  # 1. get playback token (gql.twitch.tv/gql)
  # 2. get master m3u8 content with token (usher.ttvnw.net)
  # 3. parse master m3u8 and get max bandwidth vod = target
  cred = api.get_playback_token(vod_id)
  master_m3u8_content = api.get_master_m3u8_content(vod_id, cred['sig'], cred['token'])
  print("[INFO:2] master m3u8 content ", master_m3u8_content[:100])
  target_uri = parser.get_max_bandwidth_target(master_m3u8_content)
  target_data, target_content = parser.parse_target(target_uri) 
  target_base = target_uri[:target_uri.rfind('/')] + '/'
  s3.upload_s3(f'{vod_id}/target.m3u8', target_content)
  segments = target_data['segments']
  for segment in segments:
    uri = target_base + segment['uri']
    file_name = f"{vod_id}/{segment['uri']}"
    res = requests.get(uri)
    s3.upload_s3(file_name, res.content)
