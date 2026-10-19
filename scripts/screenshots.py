"""重新產生 README 用的截圖。

用法：uv run --with playwright python scripts/screenshots.py
（第一次需要先執行 uv run --with playwright playwright install chromium）
"""
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'docs' / 'screenshots'
PORT = 6199
BASE = f'http://127.0.0.1:{PORT}'


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    db = Path(tempfile.mkdtemp()) / 'demo.db'
    env = dict(os.environ, DATABASE_URL=f'sqlite:///{db}')
    flask = [sys.executable, '-m', 'flask', '--app', 'main']
    subprocess.run([*flask, 'seed-demo'], cwd=ROOT, env=env, check=True)
    server = subprocess.Popen([*flask, 'run', '--port', str(PORT)], cwd=ROOT, env=env,
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            for scheme in ('light', 'dark'):
                page = browser.new_page(viewport={'width': 1100, 'height': 760}, color_scheme=scheme,
                                        device_scale_factor=2)
                shoot(page, scheme)
                page.close()
            mobile = browser.new_page(viewport={'width': 390, 'height': 760}, color_scheme='dark',
                                      device_scale_factor=2)
            mobile.goto(f'{BASE}/posts/1')
            mobile.screenshot(path=OUT / 'mobile-dark.png')
            browser.close()
    finally:
        server.terminate()


def shoot(page, scheme):
    page.goto(f'{BASE}/')
    page.screenshot(path=OUT / f'home-{scheme}.png')
    page.goto(f'{BASE}/posts/1')
    page.screenshot(path=OUT / f'article-{scheme}.png', full_page=True)
    if scheme == 'light':
        page.goto(f'{BASE}/tags')
        page.screenshot(path=OUT / 'tags.png')
        page.goto(f'{BASE}/auth/register')
        page.click('button[type=submit]')
        page.screenshot(path=OUT / 'register-validation.png')
        page.goto(f'{BASE}/auth/login')
        page.fill('#user_id', 'admin')
        page.fill('#password', 'admin-pass!')
        page.click('button[type=submit]')
        page.goto(f'{BASE}/posts/manage')
        page.screenshot(path=OUT / 'admin-manage.png')
        page.goto(f'{BASE}/posts/1/edit')
        page.screenshot(path=OUT / 'admin-edit.png')


if __name__ == '__main__':
    main()
