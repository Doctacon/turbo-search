#!/usr/bin/env python3
"""Validate Buoy release tags and distribution filenames without side effects."""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys
import tomllib

ROOT = Path(__file__).resolve().parents[1]


def generated_version() -> str:
    path = ROOT / "src" / "buoy_search" / "_version.py"
    try:
        text = path.read_text()
    except FileNotFoundError as exc:
        raise ValueError("generated package version is unavailable; install or build Buoy first") from exc
    match = re.search(
        r'^__version__\s*=\s*version\s*=\s*["\']([^"\']+)["\']',
        text,
        re.MULTILINE,
    )
    if match is None:
        raise ValueError("generated package version is malformed")
    return match.group(1)


def project_version() -> str:
    with (ROOT / "pyproject.toml").open("rb") as handle:
        project = tomllib.load(handle)["project"]
    return str(project["version"]) if "version" in project else generated_version()


def module_version() -> str:
    text = (ROOT / "src" / "buoy_search" / "__init__.py").read_text()
    match = re.search(r'^__version__\s*=\s*["\']([^"\']+)["\']', text, re.MULTILINE)
    if match is not None:
        return match.group(1)
    if "from ._version import __version__" in text:
        return generated_version()
    raise ValueError("src/buoy_search/__init__.py does not expose __version__")


def verify_tag(tag: str) -> None:
    project = project_version()
    module = module_version()
    if module != project:
        raise ValueError(f"package version mismatch: pyproject={project!r}, module={module!r}")
    expected = f"v{project}"
    if tag != expected:
        raise ValueError(f"release tag mismatch: expected {expected!r}, received {tag!r}")


def verify_remote_annotated_tag(tag: str, object_type: str) -> None:
    """Verify authoritative GitHub tag-ref metadata reports an annotated tag."""

    verify_tag(tag)
    if object_type != "tag":
        raise ValueError(
            f"release tag {tag!r} must be annotated; remote object type is {object_type!r}"
        )


def verify_assets(dist: Path) -> list[str]:
    version = project_version()
    expected = {
        f"buoy_search-{version}-py3-none-any.whl",
        f"buoy_search-{version}.tar.gz",
    }
    actual = (
        {path.name for path in dist.iterdir() if path.is_file() and not path.name.startswith(".")}
        if dist.is_dir()
        else set()
    )
    if actual != expected:
        raise ValueError(
            "release assets mismatch: "
            f"expected {sorted(expected)!r}, received {sorted(actual)!r}"
        )
    return sorted(actual)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    tag_parser = subparsers.add_parser("tag")
    tag_parser.add_argument("--tag", required=True)
    tag_object_parser = subparsers.add_parser("remote-tag-object")
    tag_object_parser.add_argument("--tag", required=True)
    tag_object_parser.add_argument("--object-type", required=True)
    assets_parser = subparsers.add_parser("assets")
    assets_parser.add_argument("--dist", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "tag":
            verify_tag(args.tag)
        elif args.command == "remote-tag-object":
            verify_remote_annotated_tag(args.tag, args.object_type)
        else:
            verify_assets(args.dist)
    except (OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
