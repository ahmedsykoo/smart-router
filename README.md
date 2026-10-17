# Smart Router

> راوتر لـClaude بيختار لكل رسالة الموديل الأرخص اللي يقدر يعملها (Opus / Sonnet / Haiku) والمتخصص المناسب — عربي (مصري) الأول.

A rules file + Claude skill that routes every message to **one of 16 specialists** and **the cheapest model tier that can do it**.
It runs a **real check** on the result (build, `ffprobe`, JSON parse), **escalates once** on failure, and ends each reply with a footer like `← coder · Sonnet`.
Keywords are **Egyptian Arabic first**, English second.

## Why / ليه

- **Cost:** Haiku for greetings and quick questions, Sonnet for normal work, Opus only for design, debugging, review and big projects.
  الموديل الغالي بس للحاجات اللي محتاجاه.
- **Real checks:** a subagent saying `STATUS: DONE` isn't enough when a command can prove it.
  مفيش "خلصت" من غير تشيك حقيقي لو فيه أمر يتأكد.
- **Arabic-first:** keyword tables are written in the dialect people actually type (`مش شغال`، `اعملّي`، `لخصلي`).
- **Content too, not only code:** voice, reels, motion, video editing, social design and writing have their own specialists.

## How it works / بيشتغل إزاي

| Step | What happens |
|---|---|
| 0. Answer mode | Just a question / opinion / comparison with nothing to produce → answer inline on Sonnet (Haiku if trivial). Skip to step 6. |
| 1. Tier | `!opus` / `!sonnet` / `!haiku` prefix → else any Opus keyword → else any Haiku keyword. |
| 2. Specialist | Walk the specialists table top to bottom; first keyword match wins. No match → `general`. |
| 3. Model | `manual \|\| Opus/Haiku keyword \|\| specialist default \|\| sonnet` |
| 4. Execute | Pick a `done_check` first. Same model as the router → do it inline; otherwise spawn one subagent with the brief + contract (`STATUS: DONE / UNSURE / FAILED`). Then run the check yourself. |
| 5. Escalate once | `UNSURE`, `FAILED` or a failed check → retry one level up (`haiku → sonnet → opus`), once. |
| 6. Footer + log | `← <specialist> · <Model>` (e.g. `← coder · Haiku ↑ Sonnet`), then log the task to an Artifact DB. |

`done_check` by deliverable: code → build/test/lint · video → `ffprobe` (duration, size, audio) · image → file exists at the asked size · JSON/YAML → parses · writing/research → no command, rely on STATUS.

## The 16 specialists / المتخصصين

Order matters: first match wins.

| # | Name | Default model | What it does |
|---|---|---|---|
| 1 | voice | Haiku | Text → speech in your cloned voice (Chatterbox Multilingual, Arabic) |
| 2 | motion-designer | Sonnet | Motion graphics / animation with HyperFrames, rendered MP4 |
| 3 | reels-maker | Sonnet | End-to-end 9:16 reels: script → visuals → voice → edit → captions |
| 4 | script-writer | Sonnet | Video scripts as a table: time, visual, voiceover, on-screen text |
| 5 | video-editor | Sonnet | Cut, merge, subtitles, audio sync with FFmpeg |
| 6 | social-designer | Sonnet | Posts, carousels, banners, thumbnails (HTML/CSS → PNG) |
| 7 | content-writer | Sonnet | Posts, captions, articles, LinkedIn, threads |
| 8 | ui-designer | Sonnet | Screens, landing pages, mockups, RTL-first |
| 9 | skill-builder | Opus | New Claude skills, subagent briefs, plugins, new router specialists |
| 10 | automation | Sonnet | n8n workflows, agents, webhooks, MCP servers |
| 11 | reviewer | Opus | Code / security review and tests, findings by severity |
| 12 | project | Opus | Multi-module builds: `.router/PLAN.md` (contracts first) → tasks per tier → `.router/PROGRESS.md` |
| 13 | architect | Opus | System design, data models, stack choices, hard debugging |
| 14 | researcher | Sonnet | Web / repo research with sources, license and Arabic-support flags |
| 15 | coder | Sonnet | Writes and fixes code, complete files |
| 16 | chat | Haiku | Greetings and small talk; says `UNSURE` if it turns into real work |

## Compared to smart-task-router / مقارنة

[celiktech24-cell/smart-task-router](https://github.com/celiktech24-cell/smart-task-router) is a good project with a different design; I took ideas from it (tier table, plan/verify), not code.

| | Smart Router (this) | smart-task-router |
|---|---|---|
| Routing | Keyword tables per message (cheap, predictable, editable) | Claude judges the tier per subtask from a spec / plan |
| Language | Egyptian Arabic + English keywords | English |
| Scope | Code **and** content: voice, reels, motion, video, social design | Coding tasks and code projects |
| Big code projects | `project` specialist: plan → per-task tier → check → progress file | Fuller pipeline: Haiku recon, Opus plan, per-task commits, Opus diff review |
| Effort control | Model only | Model + effort via agent files (Claude Code) |
| Verification | Real `done_check` per deliverable, escalate once | Real check per task, escalate on fail, re-plan after 2 Opus fails |

## Install / التثبيت

**(a) claude.ai (Projects)**
1. Add [`router-rules.md`](router-rules.md) to a Project's files.
2. Put one line in the Project instructions:
   `Follow router-rules.md (in the project files) for EVERY message, including greetings.`
3. For `voice`, also upload the skill in [`skills/smart-router/`](skills/smart-router/SKILL.md) (Settings → Capabilities → Skills).

**(b) Claude Code**
1. Copy [`router-rules.md`](router-rules.md) into your repo's `CLAUDE.md` (or reference it from `.claude/`).
2. Copy the skill: `cp -r skills/smart-router ~/.claude/skills/`

Then edit the **EDIT ME — your profile** block in Part 3 and the `<YOUR_ARTIFACT_URL>` in step 6 (or delete the logging block).
عدّل بلوك البروفايل وحط رابط الـArtifact بتاعك أو امسح خطوة اللوج.

## Customize / تخصيص

- **Edit `skills/smart-router/SKILL.md` only** — it's the source of truth. Then run `python check.py --sync` to regenerate `router-rules.md` and run the routing tests (CI fails if the two files drift).
  عدّل في `SKILL.md` بس، وبعدين `python check.py --sync`.
- **Keywords:** edit the tables in Part 2. Arabic = substring match, English = whole word. Prefer phrases over short roots (`ترجملي` not `ترجم`, which also catches `ترجمة فيديو`).
- **Tests:** add a row to [`tests.md`](tests.md) (message → specialist → model) whenever you change keywords or hit a misroute.
- **Add a specialist:** write a brief in Part 3 (`## name — Model` + a few lines) and add a row to the Specialists table in Part 2 at the right position (more specific rows go higher).
- **Logging:** make an Artifact with the `db` capability and paste its URL in step 6.

## Known limits / حدود معروفة

- Keyword matching is brittle: a missing synonym routes to the wrong specialist or `general`. Use `!opus` / `!sonnet` / `!haiku` to force.
- `done_check` only exists for deliverables with a command; writing and research rely on the subagent's STATUS.
- Logging needs an Artifact URL you create yourself; without it, delete the log step.
- Voice cloning: only your own voice or one whose owner gave permission. No voice sample is shipped (`*.wav` is git-ignored).
  استنساخ الصوت بإذن صاحبه بس.

## Files

```
skills/smart-router/SKILL.md    the full rules as a Claude skill (source of truth)
router-rules.md                 same rules, generated by check.py --sync
check.py                        sync check + keyword routing tests
tests.md                        routing test cases
skills/smart-router/voice/      clone.py + colab.ipynb (Chatterbox TTS)
LICENSE                         MIT
```

## License

[MIT](LICENSE) © 2026 Ahmed Ramadan Mahmoud
