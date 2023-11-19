import glob
import os
import re
import subprocess
import sys
from itertools import zip_longest

import pytest


@pytest.mark.parametrize("path", glob.glob("tests/*.pyi"))
def test_pyi_file(path: str) -> None:
    flags = []
    expected_output = ""

    if match := re.search(r"_py3(\d+)\.pyi$", path):
        if sys.version_info < (3, int(match.group(1))):
            pytest.skip(f"Python {sys.version_info} is too old for {path}")

    with open(path, encoding="UTF-8") as file:
        file_contents = file.read()

    for lineno, line in enumerate(file_contents.splitlines(), start=1):
        if line.startswith("# flags: "):
            flags.extend(line.split()[2:])
            continue
        if line.startswith("#"):
            continue

        error_codes = list(re.finditer(r"# ([A-Z]\d\d\d )", line))

        for match, next_match in zip_longest(error_codes, error_codes[1:]):
            end_pos = len(line) if next_match is None else next_match.start()
            message = line[match.end() : end_pos].strip()
            code = match[1].replace("Y0", "PYI0").strip()
            if not code.startswith("PYI0"):
                continue
            # deliberately unimplemented by ruff:
            if code in {"PYI022", "PYI023", "PYI028", "PYI031", "PYI037", "PYI038", "PYI039", "PYI040"}:
                continue
            # new codes, not yet implemented by ruff:
            if code in {"PYI057", "PYI058", "PYI059", "PYI060", "PYI061", "PYI062", "PYI090"}:
                continue
            if code == "PYI033":
                message = "Don't use type comments in stub file"
            elif code == "PYI044":
                message = '"from __future__ import annotations" has no effect in stub files, since type checkers automatically treat stubs as having those semantics'
            expected_output += f"{path}:{lineno}: {code} {message}\n"

    expected_output = (
        expected_output
        .replace("PYI030 Multiple Literal", "PYI030 Multiple literal")
        .replace(
            "PYI026 Use typing_extensions.TypeAlias for type aliases, e.g. ",
            'PYI026 Use "typing_extensions.TypeAlias" for type alias, e.g., '
        )
        .replace(
            "PYI020 Quoted annotations should never be used in stubs",
            "PYI020 Quoted annotations should not be included in stubs"
        )
        .replace("use += instead", 'use "+=" instead')
        .replace("PYI046 Protocol", "PYI046 protocol")
        .replace("PYI047 Type alias", "PYI047 TypeAlias")
        .replace(
            "PYI006 Use only < and >= for version comparisons",
            'PYI006 Use "<" or ">=" for "sys.version_info" comparisons'
        )
        .replace(
            "PYI002 If test must be a simple comparison against sys.platform or sys.version_info",
            'PYI002 "if" test must be a simple comparison against "sys.platform" or "sys.version_info"'
        )
        .replace(
            "PYI003 Unrecognized sys.version_info",
            'PYI003 Unrecognized "sys.version_info"'
        )
        .replace(
            'PYI050 Use "typing_extensions.Never" instead of',
            'PYI050 Prefer "typing_extensions.Never" over'
        )
        .replace(
            "PYI007 Unrecognized sys.platform",
            'PYI007 Unrecognized "sys.platform"'
        )
        .replace(
            "PYI048 Function body should",
            "PYI048 Function body must"
        )
        .replace('with "builtins.set"', 'with the "set" builtin')
        .replace(".\n", "\n")
        .replace("bytes literals >50 characters long", "bytes literals longer than 50 characters")
    )
    expected_output = re.sub(
        r'PYI0(\d\d) (.+) ((`|").+?(`|")) is not used',
        r"PYI0\1 Private \2 \3 is never used",
        expected_output
    )
    expected_output = re.sub(
        "PYI001 Name of private (TypeVar|ParamSpec|TypeVarTuple) must start with _",
        r'PYI001 Name of private "\1" must start with "_"',
        expected_output
    )
    flags_ = [flag.replace("Y0", "PYI0") for flag in flags]
    flags = []
    for flag in flags_:
        if flag == "--no-pyi-aware-file-checker":
            continue
        if flag.split("=")[0] == "--extend-select":
            continue
        if flag.split("=")[0] != "--extend-ignore":
            flags.append(flag)
        if "PYI0" in flag and not any(code in flag for code in {"PYI022", "PYI023", "PYI028", "PYI031", "PYI037", "PYI038", "PYI039", "PYI040", "PYI061", "PYI062", "PYI090"}):
            flags.append(flag)

    # Silence DeprecationWarnings from our dependencies (pyflakes, flake8-bugbear, etc.)
    #
    # For DeprecationWarnings coming from flake8-pyi itself,
    # print the first occurence of each warning to stderr.
    # This will fail CI the same as `-Werror:::pyi`,
    # but the test failure report that pytest gives is much easier to read
    # if we use `-Wdefault:::pyi`
    flake8_invocation = ["ruff", "--select=PYI"]

    run_results = [
        # Passing a file on command line
        subprocess.run(
            [*flake8_invocation, *flags, path],
            env={**os.environ, "PYTHONPATH": "."},
            capture_output=True,
            text=True,
        ),
        # Passing "-" as the file, and reading from stdin instead
        subprocess.run(
            [*flake8_invocation, "--stdin-filename", path, *flags, "-"],
            env={**os.environ, "PYTHONPATH": "."},
            input=file_contents,
            capture_output=True,
            text=True,
        ),
    ]

    for run_result in run_results:
        output = re.sub(":[0-9]+: ", ": ", run_result.stdout)  # ignore column numbers
        if run_result.stderr:
            output += "\n" + run_result.stderr
        output = re.sub(r"\nFound \d+ errors", "", output)
        output = re.sub(r'\n\[\*\] \d+ fixable with the "\-\-fix" option\.', "", output)
        output = output.replace("`", '"').replace(" [*] ", " ").replace(".\n", "\n")
        assert output == expected_output
