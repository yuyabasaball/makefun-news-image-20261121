// Entry for make.fun's news-image-20261121 bounty:
// "Sum up 21 November's world news in one image."
//
// The picture beside this file (entry.png, drawn by build_image.py) is the
// entry. This program copies it, byte for byte, to the output directory as
// entry.png, so every run produces exactly the same file. Node 22, standard
// library only, no network.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const png = readFileSync(new URL('./entry.png', import.meta.url));

// Guard the entry's format limits before writing anything: the bounty takes
// a PNG or JPEG of at most 1 MiB. Fail loudly rather than emit a bad file.
const PNG_SIGNATURE = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];
const isPng = PNG_SIGNATURE.every((byte, i) => png[i] === byte);
const isJpeg = png[0] === 0xff && png[1] === 0xd8;
if (!isPng && !isJpeg) throw new Error('entry.png is neither PNG nor JPEG');
if (png.byteLength > 1_048_576) throw new Error('entry.png exceeds 1 MiB');

mkdirSync(outDir, { recursive: true });
writeFileSync(join(outDir, 'entry.png'), png);
