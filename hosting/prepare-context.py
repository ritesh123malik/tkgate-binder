#!/usr/bin/env python3
"""Export tracked working-tree source plus explicit port files; never copy Git or builds."""
import argparse
import hashlib
from pathlib import Path
import shutil
import subprocess
import tarfile

ROOT = Path(__file__).resolve().parent.parent
EXTRAS = (
    'macos/test.py', 'test/common/hash_pointer.c', 'test/common/ycmalloc_pool.c',
    'test/verga/widevalue.v', 'test/verga/widevalue.out',
    'hosting/Dockerfile', 'hosting/custom_startup.sh', 'hosting/tkgate.desktop',
    'hosting/SESSION-README.txt', 'hosting/README.md', 'hosting/prepare-context.py',
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('destination', type=Path, help='new directory, must not exist')
    args = parser.parse_args()
    destination = args.destination.resolve()
    if destination.exists():
        parser.error('destination exists; choose a new directory')
    tracked = subprocess.check_output(['git', '-C', str(ROOT), 'ls-files', '-z'])
    paths = {Path(p.decode()) for p in tracked.split(b'\0') if p}
    paths.update(Path(p) for p in EXTRAS)
    selected = []
    for relative in sorted(paths):
        if relative.is_absolute() or '..' in relative.parts:
            raise ValueError(f'unsafe source path: {relative}')
        # Never transport dotfiles, host packaging outputs or user configuration.
        if any(p.startswith('.') for p in relative.parts):
            continue
        if relative.parts[0] in ('macos', 'hosting') and str(relative) not in EXTRAS:
            continue
        source = ROOT / relative
        if source.is_symlink() or not source.resolve().is_relative_to(ROOT):
            raise ValueError(f'symlink or external source refused: {relative}')
        if not source.is_file():
            raise ValueError(f'missing source: {relative}')
        selected.append(relative)
    destination.mkdir(parents=True)
    source_dir = destination / 'source'
    source_dir.mkdir()
    manifest = []
    for relative in selected:
        target = source_dir / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / relative, target)
        manifest.append(f'{hashlib.sha256(target.read_bytes()).hexdigest()}  {relative}\n')
    (source_dir / 'SOURCE-SHA256SUMS').write_text(''.join(manifest))
    with tarfile.open(destination / 'source.tar.gz', 'w:gz') as archive:
        archive.add(source_dir, arcname='tkgate')
    shutil.copy2(ROOT / 'hosting/Dockerfile', destination / 'Dockerfile')
    print(f'Prepared {len(selected)} source files in {destination}')
    print('No image built and no service deployed.')


if __name__ == '__main__':
    main()
