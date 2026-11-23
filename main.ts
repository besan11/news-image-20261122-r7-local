import * as fs from "node:fs";
import * as path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "out";
const src = path.join(here, "entry.png");
const dst = path.join(outDir, "entry.png");

// Never delete the output directory: create it if missing, then copy.
fs.mkdirSync(outDir, { recursive: true });
fs.copyFileSync(src, dst);

// Verify the copy is a PNG with the expected size.
const buf = fs.readFileSync(dst);
const pngMagic = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (!buf.subarray(0, 8).equals(pngMagic)) {
  throw new Error("entry.png is not a PNG (bad magic bytes)");
}
const width = buf.readUInt32BE(16);
const height = buf.readUInt32BE(20);
if (width !== 1024 || height !== 1024) {
  throw new Error(`entry.png is ${width}x${height}, expected 1024x1024`);
}
console.log(`wrote ${dst} (${buf.length} bytes, ${width}x${height})`);
