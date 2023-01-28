import m3u8
import requests


def get_max_bandwidth_target(content):
  m3u8_obj = m3u8.loads(content)
  print(content[:20])
  streams = m3u8_obj.data['playlists']
  target_stream = streams[0]
  for stream in streams:
    if stream['stream_info']['bandwidth'] > target_stream['stream_info']['bandwidth']:
      target_stream = stream
  return target_stream['uri']


def parse_target(target_uri):
  res = requests.get(target_uri, headers={'user-agent': 'insomnia/2022.6.0'})
  m3u8_obj = m3u8.loads(res.text)
  return (m3u8_obj.data, res.content)