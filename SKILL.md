---
name: marginalia
description: Publish an annotatable screenshot review board as a Claude artifact — the user sticks draggable post-it notes on each screenshot, saves them into the page, and Claude reads them back as structured input. Use when the user wants to mark up screenshots, UI captures, or mockups with positioned feedback ("let me add notes", "screencap I can annotate", "review board").
---

# Marginalia — annotatable screenshot boards

Turn a set of screenshots into a published artifact the user annotates with
positioned post-it notes. Saved notes embed into the page itself; any session
reads them back.

## How it works

The page declares the `artifact` runtime capability. **Save** regenerates the
document with the notes embedded (a `marginalia-notes` JSON block + a plain-text
"NOTES LEDGER") and calls `artifact.publish(html)` — the artifact republishes
itself. The publishing session gets an `artifact-changed` notification when
that happens; any session can read the notes back with WebFetch.

## Build one

1. **Compress screenshots** into a working directory (the artifact budget is
   16MB total; base64 adds ~33%). `sips -Z 1600 -s format jpeg -s formatOptions 80
   in.png --out key.jpg` for desktop shots; resample phone shots to ~720w.
   (Linux: `convert in.png -resize 1600x1600\> -quality 80 key.jpg`.)
2. **Write `manifest.json`** next to the images — schema documented at the top
   of [assets/build.py](assets/build.py). One board per screenshot: stable
   `key`, human `title`, optional provenance `chip` / staleness `caveat`,
   `phone: true` for narrow portrait shots. Give the artifact a product-style
   name in `title`.
3. **Build:** `python3 ~/.claude/skills/marginalia/assets/build.py manifest.json`
4. **Publish** the output file with the Artifact tool:
   `capabilities: {"artifact": {}}`, favicon `📌` (keep it stable across
   redeploys). Load the `artifact-capabilities` skill first if this session
   hasn't already.
5. **Tell the user**: click a screenshot to stick a note, drag to move, click
   to edit, ⚑ marks issues, **Save notes** writes them back for Claude.

## Read notes back

WebFetch the artifact URL (it saves the full HTML locally), then parse:

```python
import re, json, html
t = open(saved_html_path, encoding="utf-8").read()
m = re.search(r'<script type="application/json" id="(?:marginalia-notes|ww-notes-data)">(.*?)</script>', t, re.S)
state = json.loads(html.unescape(m.group(1)))
# state["notes"]: [{id, board, x, y, text, flag, ts}] — x/y are % of the image box
```

The visible "NOTES LEDGER" `<pre>` block carries the same data as plain text
(`#id [Board title] (x%, y%) ⚑ISSUE — text`) and survives HTML→text conversion.

## Update boards without losing notes

A tool republish overwrites the user's saved state. To refresh screenshots or
add boards: WebFetch the current version first, extract `state` (above), write
it to a file, rebuild with `--state state.json`, then republish. Board `key`s
and %-coordinates are stable, so a same-aspect screenshot swap keeps existing
notes aligned. Never rebuild from the empty default over a board that has
saved notes.

## Constraints (inherited from the artifact runtime)

- Viewers who aren't the owner (or in an unauthenticated view) can't save —
  the page shows a banner and the read-only board still renders.
- A save conflict (two views saving) drops the loser; the page says so and
  asks for a reload. No auto-retry by design.
- Everything must stay self-contained: images are data URIs; only Google
  Fonts may load externally.
