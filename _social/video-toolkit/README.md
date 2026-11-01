# Video toolkit (non-AI parts)

Selected parts of [digitalsamba/claude-code-video-toolkit](https://github.com/digitalsamba/claude-code-video-toolkit) (MIT licence, see `LICENSE`), copied at commit `4f0d7e6`, added 1 Nov 2026 at Charlie's request.

Only the parts that fit the social playbook (config key `social_playbook`) are here. The playbook still wins: **no AI voices, AI footage, AI images or AI people, and no copyrighted music.** The toolkit's AI tools (Qwen3-TTS, ElevenLabs, FLUX, Ideogram, LTX-2, ACE-Step, SadTalker, voice cloning) were deliberately left out. `lib/components/NarratorPiP.tsx` is for AI narrators: don't use it.

## What's here

| Folder | Use it for |
|---|---|
| `skills/remotion`, `skills/remotion-official` | Know-how for Remotion (React-based video): animated title cards, transitions, captions |
| `skills/playwright-recording` + `playwright/` | Recording a real website in a real browser as video (e.g. a portfolio site served locally with `python3 -m http.server`) |
| `skills/ffmpeg` | Converting, trimming, resizing and checking video |
| `lib/` | Shared Remotion components and transitions (`AnimatedBackground`, `SlideTransition`, `Label`, `Captions`, …) |
| `examples/hello-world` | A minimal Remotion project that renders with no API keys: a starting point for a NEMORA template |

## How it fits with our tools

`../tools/reel.mjs` stays the default video maker: it is simple, uses our fonts and colours, and is already checked against the playbook. Use this toolkit when a video needs more than reel.mjs can do (smoother transitions, animated lists, a recorded click-through of a real site), then make sure the result meets the same specs: 1080 x 1920 MP4, H.264 + silent AAC, 6 to 45 s, under 50 MB, NEMORA fonts (`assets/fonts`) and colours.

Remotion (`npm install` in a project folder) needs Node 18+ and downloads its own headless browser on first render. Remotion is free for individuals and companies of up to 3 people; NEMORA qualifies. Check remotion.dev/license if the team grows.

Never commit `node_modules/`, renders or recordings here: finished media goes in `/social/YYYY-MM/` only.
