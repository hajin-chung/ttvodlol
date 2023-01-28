import { describe, test } from "vitest";
import { getToken, getVideosByBroadCaster, getVideoURL } from "./twitch/api";

describe("twitch api", () => {
  test("test", () => {
    console.log("hi");
  });
  test("get token", async () => {
    const token = await getToken();
    console.log(token);
  });
  test("get videos", async () => {
    const token = await getToken();
    if (!token) {
      throw Error("token undefined");
    }
    const videos = await getVideosByBroadCaster("150664679", token);
    console.log(videos.length, videos[3]);
  });
  test("get video url", async () => {
    const videoUrl = await getVideoURL("1719822060");
    console.log(videoUrl);
  });
});
