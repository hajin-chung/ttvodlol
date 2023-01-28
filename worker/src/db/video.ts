import { getVideoURL } from "../twitch/api";

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

export const putVideo = async (
  db: D1Database,
  videoId: string,
  url: string
) => {
  const { success } = await db
    .prepare(`INSERT INTO queue (id, url) VALUES (?, ?)`)
    .bind(videoId, url)
    .run();
  return success;
};

export const upsertVideo = async (db: D1Database, videoId: string) => {
  console.log(`[*] upserting video ${videoId}`);
  const exists = await checkVideo(db, videoId);
  console.log(`[*] video ${videoId} exists ${exists}`);
  if (!exists) {
    const url = await getVideoURL(videoId);
    const success = await putVideo(db, videoId, url);
    console.log(`[*] put video ${videoId} success ${success}`);
    return true;
  }
  return false;
};

export const getQueue = async (db: D1Database) => {
  const { results } = await db
    .prepare("SELECT id, url FROM queue WHERE flag=0")
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
