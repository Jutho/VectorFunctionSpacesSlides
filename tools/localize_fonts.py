#!/usr/bin/env python3
"""Make the reveal.js theme fonts work offline.

Several reveal.js themes (solarized, night, ...) @import their fonts from Google Fonts. This
rewrites those imports in the compiled theme CSS to a local copy next to it. The Google CSS
and font files are downloaded once into a cache directory, so later runs need no internet.

Runs as a Quarto post-render script (see _quarto-revealjs.yml), from the project root.
Offline, for a theme whose fonts are not cached yet, it warns and leaves the online font in place.
"""
import glob
import hashlib
import os
import pathlib
import re
import shutil
import sys
import urllib.request

# Google Fonts serves woff2 only to browsers it recognises.
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
IMPORT = re.compile(r'@import\s*(?:url\()?\s*["\']?(https://fonts\.googleapis\.com/[^"\')]+)["\']?\s*\)?\s*;')
FONT_URL = re.compile(r'url\((https://fonts\.gstatic\.com/[^)]+)\)')


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def cached_font_dir(cache, url):
    """Directory in the cache holding fonts.css plus font files for one Google Fonts URL."""
    d = cache / hashlib.sha1(url.encode()).hexdigest()[:12]
    if (d / "fonts.css").exists():
        return d
    tmp = d.with_suffix(".tmp")
    shutil.rmtree(tmp, ignore_errors=True)
    tmp.mkdir(parents=True)
    css = fetch(url).decode()
    for font_url in sorted(set(FONT_URL.findall(css))):
        name = hashlib.sha1(font_url.encode()).hexdigest()[:12] + pathlib.PurePosixPath(font_url).suffix
        (tmp / name).write_bytes(fetch(font_url))
        css = css.replace(font_url, name)
    (tmp / "fonts.css").write_text(f"/* {url} */\n" + css)
    tmp.rename(d)
    return d


CACHE = pathlib.Path(".cache/fonts")


def main():
    out = os.environ.get("QUARTO_PROJECT_OUTPUT_DIR", "_presentations")
    for theme_css in map(pathlib.Path, glob.glob(f"{out}/site_libs/revealjs/dist/theme/*.css")):
        text = theme_css.read_text()

        def localize(m):
            url = m.group(1)
            try:
                src = cached_font_dir(CACHE, url)
            except OSError as e:
                print(f"warning: could not fetch {url} ({e}); keeping the online font", file=sys.stderr)
                return m.group(0)
            dest = theme_css.parent / "gfonts" / src.name
            shutil.copytree(src, dest, dirs_exist_ok=True)
            return f'@import"./gfonts/{src.name}/fonts.css";'

        new = IMPORT.sub(localize, text)
        if new != text:
            theme_css.write_text(new)


if __name__ == "__main__":
    main()
