#!/usr/bin/env python3
import os
import re
import sys
from pathlib import Path


def extract_links(text):
    """Extract markdown links from text"""
    # Pattern for markdown links [text](path)
    link_pattern = r"\[([^\]]*)\]\(([^)]+)\)"
    return re.findall(link_pattern, text)


REPO_ROOT = str(Path(__file__).resolve().parent.parent)


def check_file_exists(source_file, link_path):
    """Check if a linked file exists, resolving relative paths"""
    source_dir = os.path.dirname(source_file)

    # Handle different types of links
    if link_path.startswith("http"):
        return True, "External link (skipped)"

    if link_path.startswith("mailto:"):
        return True, "Email link (skipped)"

    if link_path.startswith("#"):
        return True, "Anchor link (assumed valid)"

    if link_path.startswith("/"):
        # Absolute path from project root
        full_path = os.path.join(REPO_ROOT, link_path.lstrip("/"))
    else:
        # Relative path from source file directory
        full_path = os.path.join(source_dir, link_path)

    # Clean up the path
    full_path = os.path.normpath(full_path)

    # Remove anchor fragments
    if "#" in full_path:
        full_path = full_path.split("#")[0]

    exists = os.path.exists(full_path)
    return exists, full_path


def main():
    docs_dir = os.path.join(REPO_ROOT, "docs")
    broken_links = []
    total_links = 0

    # Find all markdown files
    for root, dirs, files in os.walk(docs_dir):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)

                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()

                    # Extract links
                    links = extract_links(content)
                    total_links += len(links)

                    for link_text, link_path in links:
                        exists, resolved_path = check_file_exists(file_path, link_path)

                        if not exists and not link_path.startswith("http"):
                            broken_links.append(
                                {
                                    "source_file": file_path,
                                    "link_text": link_text,
                                    "link_path": link_path,
                                    "resolved_path": resolved_path,
                                }
                            )

                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

    # Report results
    print(f"Total internal links found: {total_links}")
    print(f"Broken links found: {len(broken_links)}")
    print("\n" + "=" * 80)
    print("BROKEN LINKS REPORT")
    print("=" * 80)

    # Group by source file
    by_file = {}
    for link in broken_links:
        source = link["source_file"]
        if source not in by_file:
            by_file[source] = []
        by_file[source].append(link)

    for source_file, links in by_file.items():
        relative_source = source_file.replace(REPO_ROOT + "/", "")
        print(f"\n📁 {relative_source} ({len(links)} broken links)")

        for link in links:
            print(f"   ❌ [{link['link_text']}]({link['link_path']})")
            print(f"      → Resolved to: {link['resolved_path']}")


if __name__ == "__main__":
    main()
