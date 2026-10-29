import sys, os, subprocess, shutil
from playwright.sync_api import sync_playwright
html, dur, out = sys.argv[1], float(sys.argv[2]), sys.argv[3]
preview = sys.argv[4:]  # optional list of times -> pngs only
fps = 30
d = os.path.abspath(out + "_frames"); shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width":1080,"height":1920})
    pg.goto("file://" + os.path.abspath(html)); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(500)
    if preview:
        for t in preview:
            pg.evaluate(f"render({t})"); pg.screenshot(path=f"{out}_t{t}.png")
    else:
        n = int(dur * fps)
        for i in range(n):
            pg.evaluate(f"render({i/fps})"); pg.screenshot(path=f"{d}/{i:05d}.jpg", type="jpeg", quality=92)
    b.close()
if not preview:
    subprocess.run(["ffmpeg","-y","-loglevel","error","-framerate",str(fps),"-i",f"{d}/%05d.jpg","-c:v","libx264","-preset","veryfast","-crf","18","-pix_fmt","yuv420p","-movflags","+faststart",out+".mp4"],check=True)
    shutil.rmtree(d)
    print("ok", out+".mp4")
