#!/usr/bin/env python3
"""Build a Marginalia review board from a manifest.

Usage:  python3 build.py manifest.json [--state state.json]

manifest.json:
{
  "title": "Checkout Marginalia",             # page <title> (product-style name)
  "mark":  "📌 CHECKOUT · MARGINALIA",        # optional toolbar wordmark
  "out":   "marginalia.html",                 # output path (relative to manifest dir)
  "boards": [
    { "key":   "cart_desktop",                # stable id — notes are keyed to it
      "title": "Cart — desktop",              # human title (shown + used in the ledger)
      "chip":  "build 412 · Aug 24",          # provenance chip (optional)
      "caveat": "pre-copy-pass",              # optional dashed warning chip
      "image": "cart_desktop.jpg",            # path relative to manifest dir
      "phone": false }                        # true → narrow centered column
  ]
}

--state state.json  re-embeds previously saved notes (extract them from the
published artifact first; see SKILL.md). Without it the board starts empty.
Keys and coordinates are stable, so replacing a board's screenshot with a
same-aspect capture keeps existing notes aligned.
"""
import base64, html, json, mimetypes, pathlib, sys

TEMPLATE = pathlib.Path(__file__).parent / "template.html"
MAX_BYTES = 15_000_000   # artifact hard cap is 16MB; leave headroom

def board_html(b):
    caveat = f'<span class="caveat">{html.escape(b["caveat"])}</span>' if b.get("caveat") else ""
    chip = f'<span class="chip">{html.escape(b["chip"])}</span>' if b.get("chip") else ""
    phone = " phone" if b.get("phone") else ""
    return f'''  <section class="board{phone}" id="b-{b["key"]}" data-board="{b["key"]}">
    <div class="bhead"><h2 class="board-title">{html.escape(b["title"])}</h2>{chip}{caveat}<span class="bnotes"></span></div>
    <div class="shotwrap"><img src="__IMG_{b["key"]}__" alt="{html.escape(b["title"])}"><div class="layer"></div></div>
  </section>'''

def main():
    manifest_path = pathlib.Path(sys.argv[1]).resolve()
    root = manifest_path.parent
    m = json.loads(manifest_path.read_text())
    state = '{"v":1,"nextId":1,"savedAt":null,"notes":[]}'
    if "--state" in sys.argv:
        sp = root / sys.argv[sys.argv.index("--state") + 1]
        state = json.dumps(json.loads(sp.read_text())).replace("<", "\\u003c")

    t = TEMPLATE.read_text()
    t = t.replace("__TITLE__", html.escape(m["title"]))
    t = t.replace("__MARK__", html.escape(m.get("mark", "\U0001F4CC " + m["title"].upper())))
    # The plain-text ledger header. Derived from the title so a published board
    # names itself in every form it can be read back as.
    t = t.replace("__LEDGER__", json.dumps(m["title"].upper())[1:-1].replace("<", "\\u003c"))
    t = t.replace("__STATE__", state)
    t = t.replace("__BOARDS__", "\n\n".join(board_html(b) for b in m["boards"]))

    for b in m["boards"]:
        p = root / b["image"]
        mime = mimetypes.guess_type(p.name)[0] or "image/jpeg"
        uri = f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()
        key = f'__IMG_{b["key"]}__'
        assert key in t, f"board key mismatch: {key}"
        t = t.replace(key, uri)
    assert "__IMG_" not in t and "__BOARDS__" not in t and "__LEDGER__" not in t

    if len(t) > MAX_BYTES:
        sys.exit(f"page is {len(t)} bytes > {MAX_BYTES}; compress images harder "
                 "(smaller resample width / lower jpeg quality)")
    out = root / m.get("out", "marginalia.html")
    out.write_text(t)
    print(f"wrote {out} ({len(t)} bytes, {len(m['boards'])} boards)")

if __name__ == "__main__":
    main()
