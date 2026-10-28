# Alikraken's Blog in Brainfuck

The whole Jekyll site now lives in `site.bf`: the layouts and includes, the four writeups, the index, archive, about and 404 pages, the atom feed and the sitemap. It reads the current year on stdin and prints every file of the site, each one starting with byte 28 (file separator), its path and a newline.

`build.py` runs it and writes the files into `_site`; the Pages workflow then copies `assets`, `css`, `license.md` and `robots.txt` next to them.

```sh
python3 build.py _site
```

Any 8-bit Brainfuck interpreter runs `site.bf` too: `echo 2026 | bf site.bf`.
