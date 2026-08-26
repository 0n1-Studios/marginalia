# Marginalia

A Claude Code skill that turns screenshots into a **published, annotatable review
board**: the user clicks a screenshot, a post-it lands at that point, they type,
and any later session reads the notes back as structured input keyed to board +
x/y percentage. The point is that *position is the feedback* — prose is a lossy
channel for "the third card".

## The two-copy rule (load-bearing)

This repo and the installed skill at `~/.claude/skills/marginalia/` are **mirrors**.
A change to either is owed to the other — they drift silently otherwise, and the
installed copy is the one that actually runs.

```bash
diff -r ~/Development/Marginalia ~/.claude/skills/marginalia \
  --exclude=.git --exclude=docs --exclude='*.md' --exclude=LICENSE
```

Only `SKILL.md` and `assets/` are mirrored; `README.md`, `LICENSE` and `docs/`
are repo-only.

## This is the studio's first PUBLIC repo

`0n1-Studios/marginalia`, MIT. Everything committed here is world-readable, so
it holds a different bar from the rest of the workspace:

- No paths, hostnames, ports, or ecosystem internals (Odin/Vault/Forge, `:31xx`)
  in anything that ships. The skill must work for someone who has never heard of
  Multitude.
- No screenshots of the user's own projects in `docs/` unless they are meant to
  be public — `docs/board.jpg` is the deliberate exception.
- README is the front door for strangers; keep the install path copy-pasteable.

## Layout

| File | What it is |
|---|---|
| `SKILL.md` | The skill — build procedure, read-back parse, the update-without-losing-notes rule |
| `assets/build.py` | Manifest → self-contained HTML. Inlines screenshots as data URIs, fails loudly if the page exceeds the artifact budget |
| `assets/template.html` | The board: post-it render, drag, edit, flag, ledger, save-as-republish. No dependencies beyond Google Fonts |

## Footguns

- **Rebuilding overwrites saved notes.** A refresh or a new board must pull the
  published page's current state and rebuild with `--state state.json`. This is
  the one way to lose a user's work here.
- **Only the owner can save.** An unauthenticated viewer still renders and reads
  the board, but cannot publish — the page says so rather than failing silently.
- **The page must stay self-contained.** Artifact CSP blocks every external host
  except Google Fonts, so screenshots ride as data URIs and count against the
  16MB budget. `build.py` enforces this; don't route around it.

## Roadmap

[ROADMAP.md](ROADMAP.md) is the single home of future work — update it in the
same pass as shipping (workspace Docs Sync rule). Bugs go to GitHub issues with
the `code-review` label, never the roadmap.

## Conversation Title

`MARGINALIA: brief description`
