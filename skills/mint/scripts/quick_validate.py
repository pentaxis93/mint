#!/usr/bin/env python3
"""Quick validation script for mint definitions."""

import re
import sys
from pathlib import Path

import yaml

PROTOCOL_INTERFACE_FIELDS = {
    "requires",
    "accepts",
    "produces",
    "may_produce",
}
SKILL_PROPERTIES = {
    "name",
    "description",
    "license",
    "allowed-tools",
    "metadata",
    "compatibility",
}
PROTOCOL_PROPERTIES = SKILL_PROPERTIES | PROTOCOL_INTERFACE_FIELDS | {"trigger"}


def validate_name(name):
    """Validate the frontmatter name field."""
    if not isinstance(name, str):
        return False, f"Name must be a string, got {type(name).__name__}"
    name = name.strip()
    if name:
        if not re.match(r"^[a-z0-9-]+$", name):
            return False, f"Name '{name}' should be kebab-case (lowercase letters, digits, and hyphens only)"
        if name.startswith("-") or name.endswith("-") or "--" in name:
            return False, f"Name '{name}' cannot start/end with hyphen or contain consecutive hyphens"
        if len(name) > 64:
            return False, f"Name is too long ({len(name)} characters). Maximum is 64 characters."
    return True, ""


def validate_description(description):
    """Validate the frontmatter description field."""
    if not isinstance(description, str):
        return False, f"Description must be a string, got {type(description).__name__}"
    description = description.strip()
    if description:
        if "<" in description or ">" in description:
            return False, "Description cannot contain angle brackets (< or >)"
        if len(description) > 1024:
            return False, f"Description is too long ({len(description)} characters). Maximum is 1024 characters."
    return True, ""


def validate_compatibility(compatibility):
    """Validate the optional compatibility field."""
    if compatibility:
        if not isinstance(compatibility, str):
            return False, f"Compatibility must be a string, got {type(compatibility).__name__}"
        if len(compatibility) > 500:
            return False, f"Compatibility is too long ({len(compatibility)} characters). Maximum is 500 characters."
    return True, ""


def validate_skill(skill_path):
    """Validate a skill or protocol directory."""
    skill_path = Path(skill_path)
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return False, "SKILL.md not found"

    content = skill_md.read_text()
    if not content.startswith("---"):
        return False, "No YAML frontmatter found"

    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format"

    frontmatter_text = match.group(1)

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
        if not isinstance(frontmatter, dict):
            return False, "Frontmatter must be a YAML dictionary"
    except yaml.YAMLError as exc:
        return False, f"Invalid YAML in frontmatter: {exc}"

    interface_fields_present = PROTOCOL_INTERFACE_FIELDS & set(frontmatter.keys())
    is_protocol = bool(interface_fields_present or "trigger" in frontmatter)
    allowed_properties = PROTOCOL_PROPERTIES if is_protocol else SKILL_PROPERTIES

    unexpected_keys = set(frontmatter.keys()) - allowed_properties
    if unexpected_keys:
        return False, (
            f"Unexpected key(s) in SKILL.md frontmatter: {', '.join(sorted(unexpected_keys))}. "
            f"Allowed properties are: {', '.join(sorted(allowed_properties))}"
        )

    if "name" not in frontmatter:
        return False, "Missing 'name' in frontmatter"
    if "description" not in frontmatter:
        return False, "Missing 'description' in frontmatter"

    if is_protocol:
        missing_protocol_fields = [
            field for field in (*sorted(PROTOCOL_INTERFACE_FIELDS), "trigger")
            if field not in frontmatter
        ]
        if missing_protocol_fields:
            return False, (
                "Missing required protocol field(s): "
                + ", ".join(missing_protocol_fields)
            )

    valid, message = validate_name(frontmatter.get("name", ""))
    if not valid:
        return False, message

    valid, message = validate_description(frontmatter.get("description", ""))
    if not valid:
        return False, message

    valid, message = validate_compatibility(frontmatter.get("compatibility", ""))
    if not valid:
        return False, message

    if is_protocol:
        for field in sorted(PROTOCOL_INTERFACE_FIELDS):
            if not isinstance(frontmatter[field], list):
                return False, f"Protocol field '{field}' must be a list"
        if not isinstance(frontmatter["trigger"], dict):
            return False, "Protocol field 'trigger' must be a mapping"

    kind = "Protocol" if is_protocol else "Skill"
    return True, f"{kind} is valid!"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python quick_validate.py <skill_directory>")
        sys.exit(1)

    valid, message = validate_skill(sys.argv[1])
    print(message)
    sys.exit(0 if valid else 1)
