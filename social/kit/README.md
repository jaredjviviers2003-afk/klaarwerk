# Klaarwerk social media kit

Everything needed to make on-brand Klaarwerk posts without internet fonts (the fonts and logos are in this folder).

## Brand
- Colours: ground #F3F5F2, ink #13232B, muted #56656B, line #D6DDD8, green #0E6E55, sun (yellow) #F2BE22, mint #E3EDE7, red (only for "problem" crosses) #C8442C.
- Fonts: Bricolage Grotesque 800 for headlines (class `disp`), Familjen Grotesk for body, JetBrains Mono for small uppercase labels (class `mono`).
- Highlight a key word with `<span class="hlbox">` (yellow box) or `<span class="hl">` (yellow underline).
- Logos in img/: klaarwerk-logo-white.png (on green/ink), klaarwerk-logo.png (on light), klaarwerk-mark.png.
- Contact on every post: WhatsApp 066 205 4680 · @klaarwerk.media · from R6,500 · done for you in 14 days.
- Voice: plain, friendly South African English. Short sentences. Talk to small business owners (plumbers, electricians, salons, workshops, shops). No hype, no fake stats, no fake testimonials, no real business names or logos.

## Videos (1080x1920, 30 fps)
- Copy one of v1-costing.html, v2-14days.html, v3-google.html as a starting point and change the words and scenes. Keep the last 2.5 s as the green CTA scene.
- Animation: any element with `data-in="<seconds>"` (and optional `data-out`, `data-fx` = up | left | right | pop | rise | none) animates in/out. Scenes are `<section class="scene" data-in data-out data-din="0.01" data-fx="none">`. Extra per-frame logic goes in `window.custom = (t) => {...}` defined BEFORE engine.js is loaded.
- Keep text inside x 70–940 and y 150–1500 (TikTok and Reels cover the right edge and bottom with buttons and captions).
- Preview stills: `python3 render.py my.html <seconds> out/name 2.0 6.5 11` (writes out/name_t2.0.png …). Look at them before rendering.
- Render: `python3 render.py my.html <seconds> out/name` → out/name.mp4 (H.264, needs playwright + ffmpeg).
- Videos have no audio on purpose: Jared adds a trending sound in TikTok/Instagram.

## Image posts (1080x1350 portrait for feed, or 1080x1080)
- See examples/ for the existing launch posts. Build a single HTML page with a fixed-size div, link fonts the way examples/ do, and screenshot it with playwright at the exact size.
