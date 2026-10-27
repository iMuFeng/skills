#!/usr/bin/env python3
"""Calculate release identifiers without modifying files or Git."""
import argparse
import json
import re


def calculate(version, build, bump, node=False):
    if not isinstance(version, str) or not re.fullmatch(r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)(?:\.(?:0|[1-9][0-9]*))?", version):
        raise ValueError("version must have two or three numeric components")
    if type(build) is not int or build < 0:
        raise ValueError("buildVersion must be a nonnegative integer")
    if bump not in ("major", "minor", "patch", "build"):
        raise ValueError("unknown bump")
    parts = [int(part) for part in version.split(".")]
    if node and len(parts) == 2 and bump == "build":
        raise ValueError("Node requires three components; build cannot normalize the version without approval")
    if len(parts) == 2 and (node or bump == "patch"):
        parts.append(0)
    if bump != "build":
        index = {"major": 0, "minor": 1, "patch": 2}[bump]
        parts[index] += 1
        for offset in range(index + 1, len(parts)):
            parts[offset] = 0
    updated = ".".join(map(str, parts))
    tag = f"v{updated}-{build + 1}"
    return {"version": updated, "buildVersion": build + 1,
            "tag": tag, "commit": f"release: {tag}"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bump", choices=("major", "minor", "patch", "build"))
    parser.add_argument("--version", required=True)
    parser.add_argument("--build", type=int, required=True)
    parser.add_argument("--node", action="store_true")
    args = parser.parse_args()
    try:
        result = calculate(args.version, args.build, args.bump, args.node)
    except ValueError as error:
        parser.error(str(error))
    print(json.dumps(result))


if __name__ == "__main__":
    main()
