"""Portable profiles. Never deserialize pickle or executable input."""

from __future__ import annotations

import re

from .models import Completion, StudentProfile


def parse_completions(text: str) -> list[Completion]:
    items = []
    for token in re.split(r"[,;\n]+", text):
        if not token.strip():
            continue
        code, sep, grade = token.strip().partition(":")
        items.append(Completion(course_code=code, grade=grade.strip() if sep else None))
    # Also enforces uniqueness through the canonical profile contract.
    StudentProfile(completed=items)
    return items


def export_profile(profile: StudentProfile) -> str:
    return profile.model_dump_json(indent=2)


def import_profile(raw: bytes) -> StudentProfile:
    if len(raw) > 100_000:
        raise ValueError("Profile file is too large")
    return StudentProfile.model_validate_json(raw)
