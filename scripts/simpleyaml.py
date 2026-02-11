#!/usr/bin/env python3
"""Tiny YAML subset parser for this repository.
Supports:
- mappings with 2-space indentation
- sequences with '- '
- block scalars with '|'
- inline scalar lists like [1, 2]
"""
from __future__ import annotations

from pathlib import Path
from typing import Any


def _parse_scalar(value: str) -> Any:
    v = value.strip()
    if v == "":
        return ""
    if v.lower() in {"true", "false"}:
        return v.lower() == "true"
    if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
        return v[1:-1]
    if v.startswith("[") and v.endswith("]"):
        inner = v[1:-1].strip()
        if not inner:
            return []
        return [_parse_scalar(x.strip()) for x in inner.split(",")]
    try:
        return int(v)
    except ValueError:
        return v


def load(path: str | Path) -> Any:
    lines = Path(path).read_text().splitlines()
    root: Any = None
    stack: list[tuple[int, Any]] = []
    i = 0

    def current_parent(indent: int):
        while stack and stack[-1][0] >= indent:
            stack.pop()
        return stack[-1][1] if stack else None

    while i < len(lines):
        raw = lines[i]
        if not raw.strip() or raw.lstrip().startswith("#"):
            i += 1
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        stripped = raw.strip()

        if stripped.startswith("- "):
            item = stripped[2:]
            parent = current_parent(indent)
            if parent is None:
                if root is None:
                    root = []
                parent = root
                stack.append((indent, parent))
            if not isinstance(parent, list):
                raise ValueError(f"Expected list parent at line {i+1}: {raw}")

            if ":" in item:
                key, value = item.split(":", 1)
                obj = {key.strip(): _parse_scalar(value)}
                parent.append(obj)
                stack.append((indent + 1, obj))
            else:
                parent.append(_parse_scalar(item))
            i += 1
            continue

        if ":" in stripped:
            key, value = stripped.split(":", 1)
            key = key.strip()
            value = value.strip()

            parent = current_parent(indent)
            if parent is None:
                if root is None:
                    root = {}
                parent = root
                stack.append((indent, parent))

            if not isinstance(parent, dict):
                raise ValueError(f"Expected mapping parent at line {i+1}: {raw}")

            if value == "|":
                block: list[str] = []
                i += 1
                while i < len(lines):
                    nxt = lines[i]
                    nindent = len(nxt) - len(nxt.lstrip(" "))
                    if nxt.strip() == "":
                        block.append("")
                        i += 1
                        continue
                    if nindent <= indent:
                        break
                    block.append(nxt[indent + 2 :])
                    i += 1
                parent[key] = "\n".join(block).rstrip("\n")
                continue

            if value == "":
                # Decide container type by peeking next non-empty line.
                j = i + 1
                next_nonempty = ""
                next_indent = -1
                while j < len(lines):
                    if lines[j].strip() and not lines[j].lstrip().startswith("#"):
                        next_nonempty = lines[j].strip()
                        next_indent = len(lines[j]) - len(lines[j].lstrip(" "))
                        break
                    j += 1
                if next_nonempty.startswith("- ") and next_indent > indent:
                    container: Any = []
                else:
                    container = {}
                parent[key] = container
                stack.append((indent + 1, container))
            else:
                parent[key] = _parse_scalar(value)
            i += 1
            continue

        i += 1

    return root
