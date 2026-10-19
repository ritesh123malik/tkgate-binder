# TkGate in your browser

[Launch TkGate](https://mybinder.org/v2/gh/ritesh123malik/tkgate-binder/main?urlpath=desktop/)

This repository builds the real TkGate circuit editor, Verga simulator and Gmac
compiler in a temporary, separate Linux desktop for each Binder visitor.
TkGate starts when the desktop opens. Save circuits in ~/Circuits and download
before leaving. See [.binder/USER-GUIDE.md](.binder/USER-GUIDE.md).

Status: Ubuntu 24.04 completed the full Binder postBuild script on 2026-10-19,
including 66/66 simulator/Gmac checks and hash/allocator regressions.
[Passing Linux build](https://github.com/ritesh123malik/tkgate-binder/actions/runs/39237036554).
The first Binder build failure was fixed by clearing upper words of wide decimal
constants. A live browser desktop and full browser feature parity remain unverified.

Based on https://github.com/bnoordhuis/tkgate with 64-bit allocator, pointer hash,
wide-value simulation, parser and path-with-spaces fixes. TkGate is GPL-2.0-or-later;
see COPYING. This repository contains the modified source and build instructions.

Binder installs .binder/apt.txt and requirements.txt, then runs .binder/postBuild.
The build must pass 65 Verga fixtures, the Gmac comparison, and hash/allocator
checks. No cloud credentials or private files are needed.

Binder is a community service for short educational and research sessions, not
guaranteed production hosting. Files disappear when the session ends. See
https://mybinder.readthedocs.io/en/latest/user-guidelines.html.
