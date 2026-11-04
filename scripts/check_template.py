"""Check tracked/candidate files for portability, schema, links, and obvious secrets.

This is a deterministic guard, not a guarantee that arbitrary company data is safe to publish.
"""

import ast
import json
from pathlib import Path
import re
import subprocess
import tomllib

import yaml

ROOT = Path(__file__).resolve().parents[1]
PATTERNS = {
    "private_key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "token": re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}|AKIA[A-Z0-9]{16})\b"),
    "jwt": re.compile(r"\beyJ[A-Za-z0-9_-]{15,}\.[A-Za-z0-9_-]{15,}\.[A-Za-z0-9_-]{15,}\b"),
    "home_path": re.compile(r"/(?:Users|home)/[A-Za-z0-9._-]+/"),
    "internal_link": re.compile(r"https?://(?:[^/\s]+\.atlassian\.net|app\.asana\.com|[^/\s]+\.sharepoint\.com)/"),
}
TEXT_SUFFIXES = {".md", ".py", ".json", ".toml", ".yaml", ".yml", ".html", ".txt", ".example"}


def candidate_files():
    data = subprocess.check_output(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"], cwd=ROOT
    )
    return sorted({ROOT / name for name in data.decode().split("\0") if name})


def main():
    errors = []
    files = candidate_files()
    for path in files:
        relative = path.relative_to(ROOT).as_posix()
        if path.is_symlink():
            errors.append(f"{relative}: symlinks are not portable template assets")
            continue
        if not path.is_file():
            continue
        if path.name.startswith(".env") and path.name != ".env.example":
            errors.append(f"{relative}: environment file cannot be exported")
        if ".local." in path.name or path.suffix in {".pem", ".key", ".p12", ".har"}:
            errors.append(f"{relative}: local/private file cannot be exported")
        if path.stat().st_size > 512_000:
            errors.append(f"{relative}: unexpectedly large file")
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeError:
            errors.append(f"{relative}: binary assets need separate review; none expected in this template")
            continue
        for kind, pattern in PATTERNS.items():
            if pattern.search(content):
                errors.append(f"{relative}: possible {kind} (value redacted)")
        try:
            if path.suffix == ".py":
                ast.parse(content, filename=relative)
            elif path.suffix == ".json":
                json.loads(content)
            elif path.suffix == ".toml":
                tomllib.loads(content)
            elif path.suffix in {".yaml", ".yml"}:
                yaml.safe_load(content)
        except (SyntaxError, ValueError, yaml.YAMLError) as error:
            errors.append(f"{relative}: invalid syntax ({type(error).__name__})")
        if path.suffix == ".md":
            for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", content):
                if "://" in target or target.startswith("#"):
                    continue
                target = target.split("#", 1)[0]
                if not (path.parent / target).exists():
                    errors.append(f"{relative}: broken link {target}")
    names = set()
    for path in (ROOT / ".agents/skills").glob("*/SKILL.md"):
        try:
            frontmatter = yaml.safe_load(path.read_text(encoding="utf-8").split("---", 2)[1])
            name = frontmatter["name"]
            if name != path.parent.name or name in names or not frontmatter.get("description"):
                raise ValueError("Skill name/description mismatch")
            names.add(name)
        except (IndexError, KeyError, TypeError, ValueError, yaml.YAMLError):
            errors.append(f"{path.relative_to(ROOT)}: invalid skill metadata")
    required_skills = {
        "qa-workflow", "generate-test-plan", "generate-testcases", "validate-testcases",
        "execute-testcases", "generate-test-report", "generate-api-tests",
        "generate-ui-automation", "organize-testcase-markdown", "write-bug",
    }
    if missing := required_skills - names:
        errors.append(f"Missing core skills: {', '.join(sorted(missing))}")
    for path in (ROOT / ".codex/agents").glob("*.toml"):
        agent = tomllib.loads(path.read_text())
        if not all(agent.get(key) for key in ("name", "description", "developer_instructions")):
            errors.append(f"{path.relative_to(ROOT)}: missing agent fields")
    for error in errors:
        print(error)
    print(f"Checked {len(files)} candidate files and {len(names)} skills; {len(errors)} issue(s).")
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
