# makefun-news-image-20261121

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/musegon-makefun-exp/makefun-news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/musegon-makefun-exp/makefun-news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

One image that sums up the world news of Saturday 21 November 2026, drawn as a flat newspaper front page carrying 23 stories, every one checked against two independent reports. Six illustrated leads: the ICJ rules Myanmar committed genocide against the Rohingya; two Russian missiles fall in Poland and NATO's chief vows to defend every inch; COP31 in Antalya misses its deadline, deadlocked over fossil fuels; Wall Street slides into correction in an AI-led selloff (S&P 500 -3.7%, Nasdaq -5.3%); Iran seeks diplomacy to end the war while the U.S. president rejects its terms; and the U.S., China and Russia leaders meet in Shenzhen and pledge that humans keep control of military AI. Around them sit a stats strip, six more story cards (Riyadh missiles, the Peru quake, Kryvyi Rih, the Davao emergency landing, BepiColombo at Mercury, Bitcoin's two-year low) and an "Also on Saturday" list of eleven more. `main.ts` copies the image (`entry.png`, 1024x1024) to the output directory; `build_image.py` is the Pillow script that drew it, so every letter stays crisp. Stories are as reported on 21 Nov 2026 by wire and news services.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

---
<sub>Entered on [make.fun](https://make.fun/?ref=e2v2rw2y&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards</sub>
