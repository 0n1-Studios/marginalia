# Marginalia — roadmap

Annotatable screenshot review boards published as Claude artifacts; the studio's
first public repo (`0n1-Studios/marginalia`, MIT).

Last reviewed: 2026-08-25

## Now

_Nothing in flight. Shipped 2026-08-25; next move is real-use feedback._

## Next

- Confirm the repo/installed-skill mirror stays in sync after the first external
  contribution — today it is a manual `diff`, with no CI guard.
  (source: `CLAUDE.md` "The two-copy rule")

## Later-Ideas

- A CI check (or pre-commit hook) that fails when `SKILL.md`/`assets/` differ
  between this repo and `~/.claude/skills/marginalia/`, replacing the manual diff.
- Per-note threading or replies, so a board survives more than one review round.
- Export notes to Markdown/issues so feedback can leave the artifact.

## Under review (possibly stale)

_Empty — the repo is 1 day old._

## From Crucible

_No refined ideas filed yet._

## Recently shipped

- **2026-08-25** — Public release: `SKILL.md`, `assets/build.py`,
  `assets/template.html`, MIT licence, README with a real board screenshot.
  (commits `4ca815b`, `631d825`)
- **2026-08-25** — `CLAUDE.md` + `ROADMAP.md` added, bringing the repo onto the
  workspace doc contract.
