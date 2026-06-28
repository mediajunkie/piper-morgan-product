"""Parse and write draft markdown files.

Supports two metadata formats per publish-to-blog SKILL.md v0.8:
    1. YAML frontmatter (file opens with a `---` fence on line 1)
    2. Legacy HTML comments in the body (e.g. `<!-- image: foo.png -->`)
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Optional

PIPER_ROOT = Path(__file__).resolve().parent.parent.parent
DRAFTS_DIR = PIPER_ROOT / "docs" / "public" / "comms" / "drafts"

_FRONTMATTER_KEYS = ("image", "alt", "caption")


def _empty_frontmatter() -> dict:
    return {k: "" for k in _FRONTMATTER_KEYS}


def _parse_yaml_frontmatter(text: str) -> tuple[Optional[dict], str]:
    """If text opens with a `---` fence, return (frontmatter_dict, body).
    Otherwise return (None, text) unchanged.

    Minimal YAML parser for simple key: value lines; avoids pulling in PyYAML.
    """
    if not text.startswith("---"):
        return None, text
    # Find the closing fence
    lines = text.splitlines(keepends=False)
    if not lines or lines[0].strip() != "---":
        return None, text
    close_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            close_idx = i
            break
    if close_idx is None:
        return None, text

    fm = _empty_frontmatter()
    for raw in lines[1:close_idx]:
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip().lower()
        value = value.strip()
        # Unescape YAML quoted scalars — single-quote ('' → ') and double-quote (\" → ")
        if value.startswith("'") and value.endswith("'") and len(value) >= 2:
            value = value[1:-1].replace("''", "'")
        elif value.startswith('"') and value.endswith('"') and len(value) >= 2:
            value = value[1:-1].replace('\\"', '"').replace("\\\\", "\\")
        if key in _FRONTMATTER_KEYS:
            fm[key] = value

    # Body is everything after the closing fence; preserve original newline shape
    body_lines = lines[close_idx + 1 :]
    # Trim a single leading blank line for neatness
    if body_lines and body_lines[0].strip() == "":
        body_lines = body_lines[1:]
    body = "\n".join(body_lines)
    return fm, body


_HTML_COMMENT_PATTERNS = {
    "image": re.compile(r"<!--\s*image:\s*(.+?)\s*-->", re.IGNORECASE),
    "alt": re.compile(r"<!--\s*alt:\s*(.+?)\s*-->", re.IGNORECASE),
    "caption": re.compile(r"<!--\s*caption:\s*(.+?)\s*-->", re.IGNORECASE),
}


def _parse_legacy_comments(text: str) -> dict:
    fm = _empty_frontmatter()
    for key, pat in _HTML_COMMENT_PATTERNS.items():
        m = pat.search(text)
        if m:
            v = m.group(1).strip()
            # Strip quotes if present
            if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
                v = v[1:-1]
            fm[key] = v
    return fm


def parse_draft(path: Path) -> tuple[dict, str]:
    """Return (frontmatter_dict, body_string). Missing keys are empty string."""
    text = path.read_text(encoding="utf-8")
    fm, body = _parse_yaml_frontmatter(text)
    if fm is not None:
        return fm, body
    # No YAML frontmatter: scan for legacy HTML comments; body is the full text
    fm = _parse_legacy_comments(text)
    return fm, text


def resolve_draft_path(slug: str, drafts_dir: Path = DRAFTS_DIR) -> Optional[Path]:
    """Try slug resolution in the order specified by the brief."""
    candidates = [
        drafts_dir / f"{slug}.md",
        drafts_dir / f"draft-{slug}-v1.md",
        drafts_dir / f"draft-{slug}.md",
    ]
    for c in candidates:
        if c.exists():
            return c
    return None


def _yaml_single_quote(value: str) -> str:
    """Encode a string as a YAML single-quoted scalar (doubling internal apostrophes)."""
    return "'" + value.replace("'", "''") + "'"


def write_draft(path: Path, frontmatter: dict, body: str) -> None:
    """Overwrite a draft file with YAML frontmatter + body.

    Existing files are replaced atomically via a temp-file rename to avoid
    partial writes on autosave.
    """
    lines = ["---"]
    for key in _FRONTMATTER_KEYS:
        value = frontmatter.get(key, "")
        lines.append(f"{key}: {_yaml_single_quote(value)}")
    lines.append("---")
    lines.append("")
    content = "\n".join(lines) + body
    if not content.endswith("\n"):
        content += "\n"
    # Atomic write: write to .tmp sibling, then rename
    tmp = path.with_suffix(".md.tmp")
    try:
        tmp.write_text(content, encoding="utf-8")
        tmp.replace(path)
    except Exception:
        tmp.unlink(missing_ok=True)
        raise
