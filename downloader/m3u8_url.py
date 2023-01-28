from urllib.parse import quote
import json
import requests

def build_gql_query(channel_login):
  str = ("{\"operationName\":"
   "\"PlaybackAccessToke"
   "n_Template\",\"query"
   "\":\"query PlaybackA"
   "ccessToken_Template("
   "$login: String!, $is"
   "Live: Boolean!, $vod"
   "ID: ID!, $isVod: Boo"
   "lean!, $playerType: "
   "String!) {  streamPl"
   "aybackAccessToken(ch"
   "annelName: $login, p"
   "arams: {platform: \\"
   "\"web\\\", playerBac"
   "kend: \\\"mediaplaye"
   "r\\\", playerType: $"
   "playerType}) @includ"
   "e(if: $isLive) {    "
   "value    signature  "
   "  __typename  }  vid"
   "eoPlaybackAccessToke"
   "n(id: $vodID, params"
   ": {platform: \\\"web"
   "\\\", playerBackend:"
   " \\\"mediaplayer\\\""
   ", playerType: $playe"
   "rType}) @include(if:"
   " $isVod) {    value "
   "   signature    __ty"
   "pename  }}\",\"varia"
   "bles\":{\"isLive\":t"
   "rue,\"login\":\"%s\",\"isVod\":fals"
   "e,\"vodID\":\"\",\"p"
   "layerType\":\"site\""
   "}}") % channel_login
  return str


def build_m3u8_url(channel_login, token, sig):
  token_econded = quote(token)
  str = f"https://usher.ttvnw.net/api/channel/hls/{channel_login}.m3u8?acmb=e30%3D&allow_source=true&fast_bread=true&player_backend=mediaplayer&playlist_include_framerate=true&reassignments_supported=true&sig={sig}&supported_codecs=avc1&token={token_econded}&cdm=wv&player_version=1.16.0"
  # str = f"{channel_login}.m3u8?acmb=e30%3D&allow_source=true&fast_bread=true&player_backend=mediaplayer&playlist_include_framerate=true&reassignments_supported=true&sig={sig}&supported_codecs=avc1&token={token_econded}&cdm=wv&player_version=1.16.0"
  # str = "https://api.ttv.lol/playlist/" + quote(str)
  if __name__ == "__main__":
    print("m3u8 url: " + str)
  return str


def get(channel_login):
  # 1. get token & sig from https://gql.twitch.tv/gql *streamer id goes in login
  # 2. https://usher.ttvnw.net/api/channel/hls/{channel_name}.m3u8? ...

  gql_url = "https://gql.twitch.tv/gql"

  s = requests.Session()
  client_id = "kimne78kx3ncx6brgo4mv6wki5h1ko"
  s.headers.update({"Client-ID": client_id})
  gql_query = build_gql_query(channel_login)
  gql_res = s.post(gql_url, data=gql_query)
  gql_data = json.loads(gql_res.text)
  token = gql_data['data']['streamPlaybackAccessToken']['value']
  sig = gql_data['data']['streamPlaybackAccessToken']['signature']
  if __name__ == "__main__":
    print("token: " + token)
  m3u8_url = build_m3u8_url(channel_login, token, sig)
  
  return m3u8_url


def main():
  # test
  channel_login = input("channel name: ")
  get(channel_login)

  
if __name__ == "__main__":
  main()