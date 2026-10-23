import re

KNOWN_HELPERS = (
    "analyze_data.py",
    "process_records.py",
    "validate_results.py",
    "check_config.py",
)

def canonicalize_tool_sequence(sequence: list[str]) -> list[str]:
    normalized = []

    for raw_step in sequence:
        step = raw_step.strip()
        matches = []

        for helper in KNOWN_HELPERS:
            pattern = rf"(?<![A-Za-z0-9_.-]){re.escape(helper)}(?![A-Za-z0-9_.-])"
            if re.search(pattern, step):
                matches.append(helper)

        if len(matches) > 1:
            raise ValueError("Ambiguous helper names")

        normalized.append(matches[0] if matches else step)

    return normalized


# Test your function
sequence = [
    " python3 scripts/analyze_data.py --input . ",
    "Run process_records.py",
    "unknown_helper.py",
]

print(canonicalize_tool_sequence(sequence))

print(canonicalize_tool_sequence(["fake_analyze_data.py"]))

print(canonicalize_tool_sequence([
    "analyze_data.py",
    "scripts/analyze_data.py",
    "process_records.py",
]))

try:
    canonicalize_tool_sequence([
        "Run process_records.py and validate_results.py"
    ])
except ValueError as e:
    print("ValueError:", e)
