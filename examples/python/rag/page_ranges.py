#!/usr/bin/env python3
"""
Helpers for turning page selections into compact convert() arguments.

The benchmark conclusion in docs/hybrid/experiments/chunking_strategy/conclusion.json
showed that merging consecutive pages into ranges is the best strategy before
calling convert().
"""

from __future__ import annotations

from typing import Iterable


def merge_consecutive_pages(pages: Iterable[int]) -> list[tuple[int, int]]:
    """Collapse a page list like [1, 2, 11] into [(1, 2), (11, 11)]."""
    unique_pages = sorted({int(page) for page in pages if int(page) > 0})
    if not unique_pages:
        return []

    ranges: list[tuple[int, int]] = []
    start = unique_pages[0]
    end = unique_pages[0]

    for page in unique_pages[1:]:
        if page == end + 1:
            end = page
            continue
        ranges.append((start, end))
        start = end = page

    ranges.append((start, end))
    return ranges


def format_pages_argument(pages: Iterable[int]) -> str | None:
    """Format pages for opendataloader-pdf's pages option."""
    ranges = merge_consecutive_pages(pages)
    if not ranges:
        return None

    return ",".join(
        f"{start}-{end}" if start != end else str(start)
        for start, end in ranges
    )
