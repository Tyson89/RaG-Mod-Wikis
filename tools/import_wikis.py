"""Import the RaG GitHub wikis into the central MkDocs site.

Run without arguments to fetch fresh copies from GitHub:

    python tools/import_wikis.py

For an existing directory of wiki checkouts:

    python tools/import_wikis.py --source-root .wiki-imports
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]
DOCS_ROOT = ROOT / "docs" / "mods"


@dataclass(frozen=True)
class Wiki:
    slug: str
    repository: str

    @property
    def clone_url(self) -> str:
        return f"https://github.com/Tyson89/{self.repository}.wiki.git"

    @property
    def web_prefix(self) -> str:
        return f"https://github.com/Tyson89/{self.repository}/wiki"


# Add future wikis here, then add their curated navigation to mkdocs.yml.
WIKIS = (
    Wiki("core", "RaG_Core_Wiki"),
    Wiki("basebuilding", "RaG_BaseBuilding_Wiki"),
    Wiki("baseitems", "RaG-Baseitems-Wiki"),
    Wiki("immersive-vehicles", "RaG-Immersive-Vehicles-Wiki"),
)

LINK_RE = re.compile(r"(\[[^\]]+\]\()([^)]+)(\))")


def page_name(value: str) -> str:
    """Convert a GitHub Wiki page name to a predictable MkDocs filename."""
    if value.casefold() == "home":
        return "index.md"
    value = value.removesuffix(".md")
    value = re.sub(r"[\s_]+", "-", value)
    value = re.sub(r"-+", "-", value)
    return f"{value.strip('-').lower()}.md"


def split_anchor(target: str) -> tuple[str, str]:
    page, marker, anchor = target.partition("#")
    return page, f"{marker}{anchor}" if marker else ""


def rewrite_target(target: str, current: Wiki) -> str:
    """Rewrite local and RaG cross-wiki links while preserving anchors."""
    target = target.strip()
    parts = urlsplit(target)
    if parts.scheme or target.startswith(("/", "mailto:")):
        for wiki in WIKIS:
            if target == wiki.web_prefix or target == f"{wiki.web_prefix}/":
                return f"../{wiki.slug}/index.md"
            prefix = f"{wiki.web_prefix}/"
            if target.startswith(prefix):
                page, anchor = split_anchor(target[len(prefix) :])
                return f"../{wiki.slug}/{page_name(page)}{anchor}"
        return target

    page, anchor = split_anchor(target)
    if not page:
        return target
    if "/" in page or page.startswith("."):
        return target
    return f"{page_name(page)}{anchor}"


def rewrite_document(text: str, current: Wiki) -> str:
    def replace(match: re.Match[str]) -> str:
        return (
            f"{match.group(1)}"
            f"{rewrite_target(match.group(2), current)}"
            f"{match.group(3)}"
        )

    text = LINK_RE.sub(replace, text)
    return text.replace("Â°C", "°C").replace("\r\n", "\n").rstrip() + "\n"


def clone_wikis(destination: Path) -> None:
    for wiki in WIKIS:
        subprocess.run(
            [
                "git",
                "-c",
                "http.sslBackend=openssl",
                "clone",
                "--quiet",
                wiki.clone_url,
                str(destination / wiki.slug),
            ],
            check=True,
        )


def import_wikis(source_root: Path) -> None:
    DOCS_ROOT.mkdir(parents=True, exist_ok=True)

    for wiki in WIKIS:
        source = source_root / wiki.slug
        if not source.is_dir():
            raise FileNotFoundError(f"Missing wiki source: {source}")

        destination = DOCS_ROOT / wiki.slug
        if destination.exists():
            shutil.rmtree(destination)
        destination.mkdir(parents=True)

        imported = 0
        for source_file in sorted(source.glob("*.md")):
            if source_file.name in {"_Sidebar.md", "_Footer.md"}:
                continue
            target_file = destination / page_name(source_file.stem)
            text = source_file.read_text(encoding="utf-8")
            target_file.write_text(
                rewrite_document(text, wiki),
                encoding="utf-8",
                newline="\n",
            )
            imported += 1

        print(f"{wiki.slug}: imported {imported} pages")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source-root",
        type=Path,
        help="Directory containing checkouts named by their destination slug.",
    )
    args = parser.parse_args()

    if args.source_root:
        import_wikis(args.source_root.resolve())
        return

    cache_root = ROOT / ".cache"
    cache_root.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="rag-wikis-", dir=cache_root) as temporary:
        source_root = Path(temporary)
        clone_wikis(source_root)
        import_wikis(source_root)


if __name__ == "__main__":
    main()
