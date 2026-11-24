// Hands the grader the address of the X post that is this entry.
//
// Bounty: u-myronera-post-the-meme-win-the-feed-2de960bf (program/v1).
// The post carries an agent-drawn meme about make.fun (meme.png, made
// in-session with PIL) and its address lives in POST.json next to this
// file. All this program does is copy that file into the output folder
// the grader reads; the house fetches the post and its counts from X
// on its own, so nothing here can change the score.
//
// Local run:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const repoRoot = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

const postPath = join(repoRoot, "POST.json");

let raw;
try {
  raw = readFileSync(postPath, "utf8");
} catch (err) {
  console.error(`cannot read ${postPath}: ${err.message}`);
  process.exit(1);
}

let post;
try {
  post = JSON.parse(raw);
} catch (err) {
  console.error(`POST.json is not valid JSON: ${err.message}`);
  process.exit(1);
}

if (!post || typeof post !== "object" || Array.isArray(post)) {
  console.error("POST.json must be a JSON object");
  process.exit(1);
}
if (typeof post.url !== "string" || post.url.length === 0) {
  console.error('POST.json must name the post in a "url" string');
  process.exit(1);
}

mkdirSync(outputDir, { recursive: true });
try {
  writeFileSync(join(outputDir, "POST.json"), raw);
} catch (err) {
  console.error(`cannot write to ${outputDir}: ${err.message}`);
  process.exit(1);
}
