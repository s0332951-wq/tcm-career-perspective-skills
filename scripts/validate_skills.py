from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
THREAD_ID_RE = re.compile(r"\b019f[0-9a-f-]{20,}\b", re.IGNORECASE)
PRIVATE_PATTERNS = {
    "Windows user path": re.compile(r"\b[A-Z]:\\Users\\[^\\\s`]+", re.IGNORECASE),
    "Unix user path": re.compile(r"(?:^|[\s`])/(?:Users|home)/[^/\s`]+", re.IGNORECASE),
    "email address": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE),
    "mainland China mobile number": re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)"),
    "UUID-like identifier": re.compile(
        r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b",
        re.IGNORECASE,
    ),
    "raw CV filename": re.compile(r"\bCV[-_ ][^\r\n`]{0,80}\.(?:docx?|pdf)\b", re.IGNORECASE),
    "private archive filename": re.compile(
        r"\b(?:career_decision_background_card|career_consultation_synthesis|thread-register|advisor-continuation-briefs)\.md\b",
        re.IGNORECASE,
    ),
}


def frontmatter(text: str) -> tuple[dict[str, str], list[str]]:
    errors: list[str] = []
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, ["missing opening frontmatter delimiter"]
    try:
        end = next(i for i, line in enumerate(lines[1:], start=1) if line.strip() == "---")
    except StopIteration:
        return {}, ["missing closing frontmatter delimiter"]

    fields: dict[str, str] = {}
    for line in lines[1:end]:
        if not line or line[0].isspace() or ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip("'\"")

    unexpected = sorted(set(fields) - {"name", "description"})
    if unexpected:
        errors.append(f"unexpected frontmatter fields: {', '.join(unexpected)}")
    if "name" not in fields:
        errors.append("missing frontmatter name")
    if "description" not in fields:
        errors.append("missing frontmatter description")
    return fields, errors


def validate_links(skill_file: Path, text: str) -> list[str]:
    errors: list[str] = []
    for raw_target in MARKDOWN_LINK_RE.findall(text):
        target = raw_target.strip().split("#", 1)[0]
        if not target or re.match(r"^(?:https?://|mailto:)", target, re.IGNORECASE):
            continue
        target = target.replace("%20", " ")
        if not (skill_file.parent / target).resolve().exists():
            errors.append(f"broken relative link: {raw_target}")
    return errors


def validate_agent_file(agent_file: Path, skill_name: str) -> list[str]:
    errors: list[str] = []
    text = agent_file.read_text(encoding="utf-8")
    for field in ("interface:", "display_name:", "short_description:", "default_prompt:"):
        if field not in text:
            errors.append(f"missing agent metadata field: {field}")
    if f"${skill_name}" not in text:
        errors.append("default_prompt does not reference the skill name")
    return errors


def validate_all_markdown_links() -> list[str]:
    errors: list[str] = []
    for path in ROOT.rglob("*.md"):
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        for error in validate_links(path, text):
            errors.append(f"{path.relative_to(ROOT)}: {error}")
    return errors


def scan_private_material() -> list[str]:
    errors: list[str] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.resolve() == Path(__file__).resolve():
            continue
        if path.suffix.lower() not in {
            ".md",
            ".yaml",
            ".yml",
            ".py",
            ".txt",
            ".json",
            ".toml",
            ".ini",
            ".csv",
            ".tsv",
        } and path.name != "LICENSE":
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for label, pattern in PRIVATE_PATTERNS.items():
            if pattern.search(text):
                errors.append(f"{path.relative_to(ROOT)}: {label} found")
        if THREAD_ID_RE.search(text):
            errors.append(f"{path.relative_to(ROOT)}: Codex thread id found")
    return errors


def main() -> int:
    errors: list[str] = []
    if not SKILLS_DIR.is_dir():
        errors.append("skills directory is missing")
    else:
        skill_dirs = sorted(path for path in SKILLS_DIR.iterdir() if path.is_dir())
        if not skill_dirs:
            errors.append("no skills found")
        for skill_dir in skill_dirs:
            prefix = skill_dir.relative_to(ROOT)
            skill_file = skill_dir / "SKILL.md"
            agent_file = skill_dir / "agents" / "openai.yaml"
            if not skill_file.is_file():
                errors.append(f"{prefix}: missing SKILL.md")
                continue
            if not agent_file.is_file():
                errors.append(f"{prefix}: missing agents/openai.yaml")

            text = skill_file.read_text(encoding="utf-8")
            fields, fm_errors = frontmatter(text)
            errors.extend(f"{prefix}: {item}" for item in fm_errors)
            name = fields.get("name", "")
            if name and not NAME_RE.fullmatch(name):
                errors.append(f"{prefix}: invalid skill name: {name}")
            if name and name != skill_dir.name:
                errors.append(f"{prefix}: directory does not match frontmatter name {name}")
            if len(text.splitlines()) > 500:
                errors.append(f"{prefix}: SKILL.md exceeds 500 lines")
            if (skill_dir / "references" / "tests").exists():
                errors.append(f"{prefix}: private test transcript directory must not be published")
            if agent_file.is_file() and name:
                errors.extend(
                    f"{prefix}: {item}" for item in validate_agent_file(agent_file, name)
                )

    errors.extend(validate_all_markdown_links())
    errors.extend(scan_private_material())
    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    count = len([path for path in SKILLS_DIR.iterdir() if path.is_dir()])
    print(f"Validation passed for {count} skills.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
