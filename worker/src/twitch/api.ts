import { env } from "../env";

export const getToken = async () => {
  const res = await fetch("https://id.twitch.tv/oauth2/token", {
    method: "POST",
    body: new URLSearchParams({
      client_id: env.CLIENT_ID,
      client_secret: env.CLIENT_SECRET,
      grant_type: "client_credentials",
    }),
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
  });
  const json = (await res.json()) as any;
  return json["access_token"];
};

export type Video = {
  id: string;
  user_name: string;
  title: string;
  created_at: string;
};

export const getVideosByBroadCaster = async (userId: string, token: string) => {
  let data:Video[] = [];
  let cursor: string | undefined = undefined;
  do {
    const res = (await (
      await fetch(
        `https://api.twitch.tv/helix/videos?user_id=${userId}${
          cursor ? `&after=${cursor}` : ""
        }`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
            "Client-Id": env.CLIENT_ID,
          },
        }
      )
    ).json()) as any;
    console.log(res);
    data.push(...res.data as Video[]);
    cursor = res.pagination.cursor as string | undefined;
  } while (cursor);
  return data;
};

export const getVideoInfo = async (videoId: string, token: string) => {
  const res = await (
    await fetch(`https://api.twitch.tv/helix/videos?id=${videoId}`, {
      headers: {
        Authorization: `Bearer ${token}`,
        "Client-Id": env.CLIENT_ID,
      },
    })
  ).json();
  return res as Video;
};

export const getPlaybackToken = async (videoId: string) => {
  const data = {
    operationName: "PlaybackAccessToken",
    variables: {
      isLive: false,
      login: "",
      isVod: true,
      vodID: videoId,
      playerType: "channel_home_live",
    },
    extensions: {
      persistedQuery: {
        version: 1,
        sha256Hash:
          "0828119ded1c13477966434e15800ff57ddacf13ba1911c129dc2200705b0712",
      },
    },
  };
  const headers = {
    "Client-Id": "kimne78kx3ncx6brgo4mv6wki5h1ko",
    "Content-Type": "text/plain",
    Authorization: "OAuth p755fb6rwziuih50ll4bslb60eahrf",
  };
  const res = await fetch("https://gql.twitch.tv/gql", {
    method: "POST",
    body: JSON.stringify(data),
    headers,
  });
  const obj = (await res.json()) as any;
  const sig = obj["data"]["videoPlaybackAccessToken"]["signature"] as string;
  const token = encodeURIComponent(
    obj["data"]["videoPlaybackAccessToken"]["value"]
  );
  return { sig, token };
};

export const getVideoURL = async (videoId: string) => {
  const { sig, token } = await getPlaybackToken(videoId);
  console.log({ sig, token });
  const url = `https://usher.ttvnw.net/vod/${videoId}.m3u8?sig=${sig}&token=${token}&allow_source=true`;
  return url;
};
