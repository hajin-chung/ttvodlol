import { getVideoURL, Video } from "../twitch/api";

export const checkVideo = async (db: D1Database, videoId: string) => {
  console.log(`[*] check video ${videoId}`);
  try {
    const { results } = await db
      .prepare("SELECT id FROM queue WHERE id=?")
      .bind(videoId)
      .all();
    console.log(`[*] check video result ${results}`);
    return results?.length ?? 0;
  } catch (error) {
    console.error(error);
    return true;
  }
};

type VideoWithUrl = Video & { url: string };

export const putVideo = async (db: D1Database, video: VideoWithUrl) => {
  const { id, url, created_at, title } = video;
  const { success } = await db
    .prepare(`INSERT INTO queue (id, url, created_at) VALUES (?, ?, ?)`)
    .bind(id, url, created_at)
    .run();
  return success;
};

export const upsertVideo = async (db: D1Database, video: Video) => {
  const { id, created_at, title } = video;
  console.log(`[*] upserting video ${id}`);
  const exists = await checkVideo(db, id);
  console.log(`[*] video ${id} exists ${exists}`);
  if (!exists) {
    const url = await getVideoURL(id);
    const success = await putVideo(db, { ...video, url });
    console.log(`[*] put video ${id} success ${success}`);
    return true;
  }
  return false;
};

export const getQueue = async (db: D1Database) => {
  const { results } = await db
    .prepare("SELECT id, url, created_at FROM queue WHERE flag=0")
    .all();
  return results;
};

export const flagQueue = async (db: D1Database, id: string) => {
  try {
    const { success } = await db
      .prepare(`UPDATE queue SET flag=1 WHERE id=?`)
      .bind(id)
      .run();
    return success;
  } catch (error) {
    console.error(error);
    return false;
  }
};
