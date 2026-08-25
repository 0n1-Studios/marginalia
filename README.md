# marginalia — stick notes on screenshots, hand them back to Claude

A [Claude Code](https://claude.com/claude-code) skill that turns a pile of screenshots into a
**published review board you can annotate**. You click a screenshot, a post-it lands where you
clicked, you type. Drag to move, ⚑ to mark it an issue, **Save notes** to write them back into
the page — and any Claude session can read them out again as structured input.

It exists because *"the spacing on the third card is off"* is a sentence nobody should have to
write. Point at the third card instead.

```
you                          the board                    claude
───                          ─────────                    ──────
"here are 6 screens"    →    published artifact
                             click → note → save     →    reads 14 positioned notes,
                                                          3 flagged, keyed to boards
```

## What makes it different from pasting a screenshot into chat

A pasted screenshot gets described in prose. **Position is the feedback** — which button, which
gap, which of the four things in that corner — and prose is a lossy channel for position. A
marginalia note carries the board it's on and its x/y as a percentage of the image, so a note
means the same thing after the screenshot is re-captured at a different size.

It also survives the session. The notes live *in the published page*, not in a transcript, so
tomorrow's session reads today's review without you re-explaining any of it.

## Install

Drop the folder into your skills directory:

```bash
git clone https://github.com/0n1-Studios/marginalia.git ~/.claude/skills/marginalia
```

Then in Claude Code, hand it some screenshots and say what you want:

```
here are 6 screens of the checkout flow — give me a board I can annotate
```

…or `/marginalia`. The description is written to trigger on the vaguer phrasings too
("let me add notes", "screencap I can mark up", "review board").

## How it works

The published page declares the `artifact` runtime capability. Saving regenerates the whole
document with the notes embedded — a `marginalia-notes` JSON block plus a plain-text **notes
ledger** — and calls `artifact.publish()`, so the artifact rewrites itself. Nothing is stored
anywhere else; the page *is* the database.

Claude reads it back by fetching the artifact URL and parsing either form:

```
#7 [Cart — desktop] (61.4%, 22.8%) ⚑ISSUE — promo field is below the fold on 13"
```

The JSON block is the machine copy; the ledger is the same data as plain text, so the notes
still arrive intact through anything that flattens HTML.

## What's in here

| File | What it is |
|---|---|
| `SKILL.md` | The skill itself — the build procedure, the read-back parse, the update-without-losing-notes rule |
| `assets/build.py` | Manifest → self-contained HTML. Inlines each screenshot as a data URI and fails loudly if the page won't fit the artifact budget |
| `assets/template.html` | The board: post-it rendering, drag, edit, flag, ledger, save-as-republish. No dependencies beyond Google Fonts |

A manifest is small enough to write by hand:

```json
{
  "title": "Checkout Marginalia",
  "out": "marginalia.html",
  "boards": [
    { "key": "cart_desktop", "title": "Cart — desktop", "chip": "build 412", "image": "cart.jpg" },
    { "key": "pay_phone",    "title": "Payment — iPhone", "image": "pay.jpg", "phone": true }
  ]
}
```

```bash
python3 ~/.claude/skills/marginalia/assets/build.py manifest.json
```

## Two things worth knowing before you rely on it

**Rebuilding overwrites saved notes.** To refresh a screenshot or add a board, Claude must pull
the current state out of the published page and rebuild with `--state state.json`. The skill
says so twice; it's the one way to lose work here.

**Only the owner can save.** In an unauthenticated view the board still renders and still reads,
but the save button can't publish — the page says so rather than pretending.

## Licence

MIT. Do whatever you like with it.

Built at [0n1 Studios](https://0n1studios.com).
