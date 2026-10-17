"""Keep router-rules.md in sync with SKILL.md and test keyword routing against tests.md.

  python check.py          check only (CI)
  python check.py --sync   rewrite router-rules.md from SKILL.md, then check

SKILL.md is the source of truth. Routing here covers steps 1-3 only (tier, specialist,
model); Answer mode (step 0) is a judgment call, so test messages must ask for work.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
SKILL = ROOT / "skills/smart-router/SKILL.md"
RULES = ROOT / "router-rules.md"
TESTS = ROOT / "tests.md"
SKILL_LINE = "Exception: for `voice` tasks, use `voice/clone.py` and `voice/colab.ipynb` next to this file."
RULES_LINE = "Exception: for `voice` tasks, load the `smart-router` skill to get `voice/clone.py` and `voice/colab.ipynb`."
ARABIC = re.compile(r"[؀-ۿ]")


def rules_from_skill(skill):
    body = skill.split("---\n", 2)[2].lstrip("\n")  # drop frontmatter
    assert SKILL_LINE in body, "voice exception line changed; update check.py"
    return body.replace(SKILL_LINE, RULES_LINE)


def table(text, heading):
    """Rows of the first markdown table after `## heading`, as lists of cells."""
    lines = text.split(f"## {heading}\n", 1)[1].splitlines()
    start = next(i for i, l in enumerate(lines) if l.startswith("|"))
    out = []
    for l in lines[start:]:
        if not l.startswith("|"):
            break
        out.append([c.strip() for c in l.strip().strip("|").split("|")])
    return out[2:]  # skip header + separator


def keywords(cell):
    return [k.strip() for k in re.split(r"[،,]", cell) if k.strip()]


def hit(msg, kws):
    for k in kws:
        if ARABIC.search(k):
            if k in msg:
                return True
        elif re.search(rf"(?<!\w){re.escape(k)}(?!\w)", msg, re.I):
            return True
    return False


def route(msg, tiers, specialists):
    m = re.match(r"\s*!(opus|sonnet|haiku)\b", msg, re.I)
    tier = m.group(1).lower() if m else None
    if m:
        msg = msg[m.end():]
    tier = tier or ("opus" if hit(msg, tiers["Opus"]) else "haiku" if hit(msg, tiers["Haiku"]) else None)
    for _, name, default, kws in specialists:
        if hit(msg, keywords(kws)):
            return name, tier or default.lower()
    return "general", tier or "sonnet"


def main():
    skill = SKILL.read_text(encoding="utf-8")
    want = rules_from_skill(skill)
    if "--sync" in sys.argv:
        RULES.write_text(want, encoding="utf-8")
    errors = []
    if RULES.read_text(encoding="utf-8") != want:
        errors.append("router-rules.md is out of sync with SKILL.md: run `python check.py --sync`")

    tiers = {t: keywords(k) for t, k in table(skill, "Tiers")}
    specialists = table(skill, "Specialists")
    cases = table(TESTS.read_text(encoding="utf-8"), "Cases")
    for msg, spec, model in cases:
        got = route(msg, tiers, specialists)
        if got != (spec, model.lower()):
            errors.append(f"{msg!r}: expected {spec} · {model}, got {got[0]} · {got[1]}")

    print("\n".join(errors) or f"OK: rules in sync, {len(cases)} routing cases pass")
    sys.exit(bool(errors))


if __name__ == "__main__":
    main()
