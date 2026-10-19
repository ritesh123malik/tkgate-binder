#!/usr/bin/env python3
"""Run installed TkGate command-line regressions without modifying fixtures."""
import argparse
import difflib
import os
import itertools
import re
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent.parent


def probe_order(data):
    """Only independent probe messages within one timestamp may commute.

    new_TaskContext enumerates a pointer hash, so ASLR changes net ordering.
    Keep timestamp/operation order and repeated events for each signal intact.
    """
    lines = data.splitlines(keepends=True)
    pattern = re.compile(rb'^(valueof|tell bob) (\S+) (\S+) @ (\d+)\n$')
    def group_key(line):
        match = pattern.fullmatch(line)
        return (match[1], match[4]) if match else (line, None)
    result = []
    for _, group in itertools.groupby(lines, group_key):
        group = list(group)
        if all(pattern.fullmatch(line) for line in group):
            # Stable sort changes only ordering between distinct nets.
            group.sort(key=lambda line: pattern.fullmatch(line)[2])
        result.extend(group)
    return b''.join(result)


def compare(expected, actual):
    if expected == actual:
        return True
    print(''.join(difflib.unified_diff(
        expected.decode('utf-8', errors='replace').splitlines(keepends=True),
        actual.decode('utf-8', errors='replace').splitlines(keepends=True),
        fromfile='expected', tofile='actual')), end='')
    return False


def run(command, cwd, timeout):
    try:
        result = subprocess.run(command, cwd=cwd, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, timeout=timeout)
    except (subprocess.TimeoutExpired, OSError) as exc:
        print(f'FAIL: {exc}')
        return None
    if result.stderr:
        print(result.stderr.decode('utf-8', errors='replace'), end='')
    if result.returncode:
        print(f'FAIL: exit status {result.returncode}')
        return None
    return result.stdout


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prefix', type=Path, default=ROOT / 'macos/build/prefix',
                        help='installed TkGate prefix containing bin/verga and bin/gmac')
    parser.add_argument('--timeout', type=float, default=30,
                        help='maximum seconds per test (default: 30)')
    args = parser.parse_args()
    if args.timeout <= 0:
        parser.error('--timeout must be positive')
    prefix = args.prefix.resolve()
    binaries = {name: prefix / 'bin' / name for name in ('verga', 'gmac')}
    for binary in binaries.values():
        if not binary.is_file() or not os.access(binary, os.X_OK):
            parser.error(f'missing executable: {binary}; build and install first')
    fixtures = ROOT / 'test/verga'
    cases = sorted(fixtures.glob('*.v'))
    if not cases:
        parser.error(f'no Verga fixtures found in {fixtures}')
    passed = 0
    total = len(cases) + 1
    with tempfile.TemporaryDirectory(prefix='tkgate-tests-') as temporary:
        scratch = Path(temporary)
        for case in cases:
            print(f'Verga {case.name}:', flush=True)
            expected = case.with_suffix('.out')
            if not expected.is_file():
                print(f'FAIL: missing expected output {expected}')
                continue
            # Preserve test/verga working-directory semantics (test.mem etc.),
            # with a separate copy for every case, including $fopen outputs.
            work = scratch / case.stem / 'test/verga'
            shutil.copytree(fixtures, work)
            actual = run([str(binaries['verga']), '-q', case.name], work, args.timeout)
            wanted = expected.read_bytes()
            if actual is not None and case.name == 'probe1.v':
                wanted, actual = probe_order(wanted), probe_order(actual)
            if actual is not None and compare(wanted, actual):
                passed += 1
                print('PASS')
            else:
                print('FAIL')
        print('Gmac menagerie memory image:', flush=True)
        example = ROOT / 'locale/en/examples/ex5'
        work = scratch / 'gmac'
        shutil.copytree(example, work)
        actual = run([str(binaries['gmac']), '-o', 'actual.mem', 'menagerie.gm'],
                     work, args.timeout)
        output = work / 'actual.mem'
        if actual is not None and output.is_file() and compare(
                (example / 'menagerie.mem').read_bytes(), output.read_bytes()):
            passed += 1
            print('PASS')
        else:
            print('FAIL')
    print(f'{passed}/{total} passed; {total - passed} failed.')
    print('GUI, XQuartz, printing, and peripheral integration require separate checks.')
    return int(passed != total)


if __name__ == '__main__':
    sys.exit(main())
