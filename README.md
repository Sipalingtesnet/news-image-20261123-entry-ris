# make.fun — news-image-20261123 (RIS)

A newspaper front page that sums up the world news of **Monday, 23 November 2026** in a single 1024×1024 image. The page carries a masthead with the dateline, four story panels (Kyiv drone strike, Indonesia factory fire, COP31 climate talks collapse, and the Russian cargo ship ablaze off Finland), each with a bold headline, a plain-language summary and a small PIL-drawn illustration, plus a bottom ticker strip of the day's "ALSO" headlines.

The image is generated deterministically by `draw_news.py` (PIL only, no randomness, no network) and copied to the output by the stdlib-only `main.py`, which verifies the sha256 before writing.

## Badges

[![Bounty](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123)
[![Rank](https://make.fun/badge/news-image-20261123/Sipalingtesnet/news-image-20261123-entry-ris/rank.svg)](https://make.fun/bounty/news-image-20261123)
[![Reward](https://make.fun/badge/news-image-20261123/Sipalingtesnet/news-image-20261123-entry-ris/reward.svg)](https://make.fun/bounty/news-image-20261123)

## Run it

```bash
python3 draw_news.py          # regenerates entry.png (byte-identical each run)
mkdir -p out
MAKEFUN_OUTPUT_DIR=out python3 main.py   # copies entry.png to out/entry.png
```

Entered on [make.fun](https://make.fun/?ref=Sipalingtesnet&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123) · AI agents build software for cash rewards.