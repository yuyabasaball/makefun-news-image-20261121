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

import { copyFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
copyFileSync(new URL('./entry.png', import.meta.url), join(outDir, 'entry.png'));
