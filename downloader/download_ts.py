import m3u8
import m3u8_url

def get_source_url(m3u8_url):
  m3u8_parsed = m3u8.load(m3u8_url)
  max_bandwidth = 0
  playlist_url = ""
  for playlist in m3u8_parsed.playlists:
    if max_bandwidth < int(playlist.stream_info.bandwidth):
      max_bandwidth = playlist.stream_info.bandwidth
      playlist_url = playlist.uri
  print(max_bandwidth, playlist_url)
  return playlist_url


def download_ts(source_url):
  source_parse = m3u8.load(source_url)
  print (len(source_parse.segments))
  for segment in source_parse.segments:
    print(segment.uri)
    print("\n")


def main():
  channel_login = input("channel login: ")
  url = m3u8_url.get(channel_login)
  source_url = get_source_url(url)
  download_ts(source_url)

if __name__ == "__main__":
  main()