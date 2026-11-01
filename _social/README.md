# NEMORA social media toolkit

Used by NEMORA's social media agent (a scheduled Claude task). Not published on the website: Jekyll skips folders that start with `_`.

- `tools/card.mjs` makes on-brand 1080 x 1350 JPEG photos from real words and real screenshots.
- `tools/reel.mjs` makes 1080 x 1920 MP4 videos (H.264, silent AAC) from title cards, real screenshots and real websites scrolled in a phone-sized browser.
- `video-toolkit/` holds the non-AI parts of digitalsamba/claude-code-video-toolkit (Remotion, Playwright screen recording, ffmpeg know-how) for videos that need more than reel.mjs. See `video-toolkit/README.md`; the playbook's no-AI rules still apply.
- Finished media goes in `/social/YYYY-MM/` at the repo root, which GitHub Pages serves at `https://nemora.uk/social/YYYY-MM/<file>`. The NEMORA admin publishes from those URLs to Facebook and Instagram. `/social/` is blocked in robots.txt.

Rules live in the NEMORA database (`config` key `social_playbook`), shown in the admin under Settings.

```bash
node _social/tools/card.mjs spec.json social/2026-11/business-package.jpg
node _social/tools/reel.mjs spec.json social/2026-11/spitfire-comedy.mp4
```

To scroll a real site from its source: `cd <site repo> && python3 -m http.server 8800` and use `http://localhost:8800/` as the scene URL. Screenshots of the portfolio sites are in `assets/work/`.
- `tools/motion-reel-example.mjs` is a worked example of a smoother reel (word-by-word captions, a camera push-in, a phone hand-off, a colour change between sections), built by following `video-toolkit/skills/remotion/motion-craft.md` with the Playwright already installed. Copy it for a new video when reel.mjs looks too plain: `node _social/tools/motion-reel-example.mjs . social/YYYY-MM/<slug>.mp4` (add a third argument such as `2,5,9` to save stills to check first).

## Learning from results (added 1 Nov 2026)

- The admin fills `social_posts.insights` every hour for 30 days after a post goes out: `{ ig: { reach, views, likes, comments, shares, saves, interactions }, fb: { reach, views, likes or reactions, comments, shares, clicks }, error }`, with `insights_at` showing when. Charlie sees the same numbers in the Social tab.
- When planning, compare reach, saves, shares and comments by kind and topic, and note in each post's `idea` what the numbers suggested. Saves and shares say more than likes for a small local account.
- An `error` mentioning permissions means the Page token needs `read_insights` and `instagram_manage_insights`: tell Charlie in the run's one notification.
- The motion version of the Spitfire Comedy reel (`tools/motion-reel-example.mjs`, made at Charlie's request) is the standard for the weekly video. Videos stay silent (his choice, 1 Nov 2026).
- Charlie is allowing the session to reach nemora.uk, the client sites and *.demositeforyou.workers.dev. Try live sites first for real scroll-throughs, and check pushed media URLs load.
