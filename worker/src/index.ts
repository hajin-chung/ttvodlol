/**
 * Welcome to Cloudflare Workers! This is your first worker.
 *
 * - Run `wrangler dev src/index.ts` in your terminal to start a development server
 * - Open a browser tab at http://localhost:8787/ to see your worker in action
 * - Run `wrangler publish src/index.ts --name my-worker` to publish your worker
 *
 * Learn more at https://developers.cloudflare.com/workers/
 */

export interface Env {
  // Example binding to KV. Learn more at https://developers.cloudflare.com/workers/runtime-apis/kv/
  // MY_KV_NAMESPACE: KVNamespace;
  //
  // Example binding to Durable Object. Learn more at https://developers.cloudflare.com/workers/runtime-apis/durable-objects/
  // MY_DURABLE_OBJECT: DurableObjectNamespace;
  //
  // Example binding to R2. Learn more at https://developers.cloudflare.com/workers/runtime-apis/r2/
  // MY_BUCKET: R2Bucket;
  DB: D1Database;
}

import { Router } from "itty-router";
import { upsertVideo } from "./db/video";
import { getToken, getVideosByBroadCaster } from "./twitch/api";

const router = Router();
router.get("/ping", async (req) => {
  return new Response(
    JSON.stringify({
      message: "pong",
    })
  );
});

router.get("/tables", async (req, env) => {
  try {
    const { results } = await (env.DB as D1Database).prepare(".tables").run();
    return new Response(
      JSON.stringify({
        results,
      })
    );
  } catch (error) {
    console.error(error);
    return new Response(JSON.stringify({ error }));
  }
});

router.get("/download/all", async (req, env) => {
  try {
    const token = await getToken();
    if (!token) {
      throw Error("token undefined");
    }
    const videos = await getVideosByBroadCaster("150664679", token);
    await Promise.all(videos.map(async ({ id }) => upsertVideo(env.DB, id)));
    return new Response(
      JSON.stringify({
        videos,
        message: "success",
      })
    );
  } catch (error) {
    return new Response(
      JSON.stringify({
        error,
        message: "error",
      })
    );
  }
});

router.get("/download/:id", async (req, env) => {
  const id = req.params.id;
  const success = upsertVideo(env.DB, id);
  return new Response(
    JSON.stringify({
      error: !success,
    })
  );
});

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    return router.handle(request, env);
  },
};
