# TkGate in your browser

Run the **actual TkGate circuit editor, Verga simulator and Gmac compiler** in a temporary Linux desktop through your browser. This project adapts the existing application for easier educational access; it is not a JavaScript recreation of TkGate.

[![Launch Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/ritesh123malik/tkgate-binder/main?urlpath=desktop/)
[![Linux Binder build](https://github.com/ritesh123malik/tkgate-binder/actions/workflows/linux.yml/badge.svg)](https://github.com/ritesh123malik/tkgate-binder/actions/workflows/linux.yml)

**[Launch the latest version](https://mybinder.org/v2/gh/ritesh123malik/tkgate-binder/main?urlpath=desktop/)** · **[Launch the pinned, regression-tested code revision](https://mybinder.org/v2/gh/ritesh123malik/tkgate-binder/b5b0b2e9bef172ef61a29de4d10a6124f40ce5b9?urlpath=desktop/)** · [Student quick guide](.binder/USER-GUIDE.md)

> **Save locally before leaving:** Binder storage is temporary. TkGate's Save command writes to the remote session, not your laptop. Download your circuits before the session ends. Public Binder is a shared, best-effort service, not guaranteed classroom capacity or permanent hosting.

Documentation updated: **20 October 2026**. Test results below describe recorded runs, not a guarantee that every feature or future build works.

## Contents

- [Project purpose and status](#project-purpose-and-status)
- [Start using TkGate](#start-using-tkgate)
- [Save, download and reopen circuits](#save-download-and-reopen-circuits)
- [Sharing, privacy and classroom use](#sharing-privacy-and-classroom-use)
- [Application features and validation boundaries](#application-features-and-validation-boundaries)
- [Architecture and technologies](#architecture-and-technologies)
- [Repository layout](#repository-layout)
- [Build and startup lifecycle](#build-and-startup-lifecycle)
- [Source fixes and their reasoning](#source-fixes-and-their-reasoning)
- [Testing and recorded results](#testing-and-recorded-results)
- [Build and test on Linux](#build-and-test-on-linux)
- [macOS work and distribution status](#macos-work-and-distribution-status)
- [Alternative hosting: Kasm and Oracle](#alternative-hosting-kasm-and-oracle)
- [Troubleshooting](#troubleshooting)
- [Maintenance and contributions](#maintenance-and-contributions)
- [Project history](#project-history)
- [License, attribution and references](#license-attribution-and-references)

## Project purpose and status

TkGate is an established C/Tcl/Tk digital circuit editor and event-driven simulator. This project started with making it usable on MacBooks through XQuartz, then expanded to browser access for students who should not need to configure a local native toolchain.

The browser version runs the existing Linux application in a remote desktop. It retains the upstream circuit libraries, examples, HDL functionality and simulation tools. Work focused on compatibility fixes, memory correctness, build automation, packaging, deployment and regression testing.

| Area | Recorded status |
|---|---|
| Public source | Published in this repository |
| Linux native build | Ubuntu 24.04 completed `.binder/postBuild`, including 66/66 CLI checks and additional hash/allocator regressions |
| Binder desktop | A user-provided screenshot showed TkGate running and `second.v` visible in `~/Circuits` |
| Browser feature coverage | Full editing, simulation, peripherals, printing and transfer acceptance testing remains incomplete |
| Session isolation | Binder's separate-session design is relied upon; this project has not independently audited cross-session access |
| macOS | A local Apple Silicon/XQuartz bundle and selected integration tests were produced in the wider project; this checkout does not contain the full Mac packaging toolchain |
| Oracle/Kasm | Deployment files were prepared; no VM was provisioned and no Kasm image was built or deployed |

There is no claim that every TkGate feature has been verified. The screenshot establishes a working editor session, not exhaustive functional parity.

## Start using TkGate

1. Open a launch link above. The first launch of a revision may need to build an image; later launches can still queue or fail when shared capacity is unavailable.
2. Wait for the Linux desktop to appear. TkGate is configured to start automatically.
3. If you close TkGate, reopen it using the desktop launcher.
4. Open example circuits through **Desktop → Examples**, or create your own circuit.
5. Edit and simulate using TkGate's controls. Save your own work under **`/home/jovyan/Circuits`** (normally `~/Circuits`).
6. Download your saved files using the instructions below.

Browser access does not require installing XQuartz on your Mac. XQuartz applies only to the separate local macOS application route. The upstream [TkGate manual](https://bnoordhuis.github.io/tkgate/) explains circuit editing, modules, HDL, simulation, Gmac and components.

## Save, download and reopen circuits

### Save during a session

Use TkGate's Save/Save As command and choose `~/Circuits`, for example `~/Circuits/adder.v`. The `.v` file contains TkGate's circuit/netlist representation. Saving into the remote filesystem is only the first step toward keeping your work.

### Download to your computer

1. Save your latest changes in TkGate.
2. Duplicate the **current running session's browser tab**.
3. In the duplicated tab, preserve the existing server/session URL prefix and replace the trailing `/desktop/` route with `/lab/`.
4. In JupyterLab's file browser, open **Circuits**.
5. Right-click the `.v` file and choose **Download**.
6. Check that the download is on your computer before closing the session.

Do not open a fresh Binder launch to look for an old session's files: a new session has its own temporary environment. If your circuit depends on separate HDL, library or memory-initialization files, download those too and preserve the expected relative paths.

### Continue in a later session

Launch TkGate again, open that session's JupyterLab file browser, upload your saved files into **Circuits**, then open the circuit from TkGate. There is no automatic synchronization with your laptop, GitHub or cloud storage.

### Export a printable circuit

Print/export the schematic to a PostScript file. Ghostscript is included in the Binder package list; in the remote terminal you can convert it:

```sh
ps2pdf "circuit.ps" "circuit.pdf"
```

Download the PDF through JupyterLab. Your local physical printer and local filesystem are not directly connected to the remote application. Full browser printing/file-transfer acceptance testing remains outstanding.

## Sharing, privacy and classroom use

Share the generic **Binder launch link** or this repository URL. Do not share a running session URL, authentication token or browser session: those can grant access to the active environment.

Binder is designed to give visitors separate environments. Saving a circuit does **not** automatically commit it to this public GitHub repository. However, separate sessions are not a guarantee of absolute privacy, and this legacy application and deployment have not undergone a security audit. Avoid confidential data and credentials.

Suitable uses include digital logic practice, demonstrations, example exploration and short lab exercises. For group use:

- Ask students to download work regularly and before leaving.
- Try the exact class exercise in advance, including simulation and file transfer.
- Expect startup delays, inactivity termination, resource limits and possible service unavailability.
- Do not assume an entire class can launch simultaneously or that sessions survive until the next lab.
- Keep a local installation or institution-managed service as a fallback for graded or scheduled work.

The service does not reserve capacity, provide persistent student accounts or guarantee unlimited users. Consult [Binder's current usage guidelines](https://mybinder.readthedocs.io/en/latest/about/user-guidelines.html) for current quotas and session policies; they are not controlled by this repository.

## Application features and validation boundaries

The retained upstream application includes:

- Basic logic gates, tri-state devices, arithmetic components, registers, memories and MOS elements.
- Hierarchical circuits, user-defined modules and module-interface editing.
- Verilog-like netlists and HDL modules.
- Event-driven simulation, probes, breakpoints and memory initialization.
- Gmac microcode/assembly compilation.
- Peripheral/library components, including TTY and drink-machine examples.
- Schematic PostScript printing/export.

These describe the upstream feature set. Inclusion is not proof that each feature works in this browser environment. In particular, exhaustive VPD/peripheral tests, browser interaction tests, rendered print quality, cross-session isolation, resource limits and reconnect behavior remain to be validated.

## Architecture and technologies

```text
Browser
  → Binder launch / repo2docker image
  → Jupyter session and authenticated proxy
  → jupyter-remote-desktop-proxy
  → TigerVNC + X11 + XFCE desktop
  → native TkGate editor (C + Tcl/Tk)
      ├─ Verga simulation process
      ├─ Gmac compiler
      └─ circuit files in the temporary session filesystem
```

| Technology | Responsibility |
|---|---|
| C | Existing editor, simulator, compiler and low-level correctness fixes |
| Tcl/Tk 8.6 | Existing UI widgets and application orchestration |
| X11, XFCE, TigerVNC | Linux graphical desktop and remote display |
| Binder / repo2docker | Build the repository environment and launch temporary sessions |
| JupyterLab | Session file browser, upload/download and terminal access |
| `jupyter-remote-desktop-proxy==3.0.1` | Desktop integration through Jupyter |
| Bash | Build hooks and application startup |
| Python | Fixture comparison and source-context export |
| Autoconf, Automake, Libtool, Make | Regenerate, configure, compile and install upstream native code |
| Bison / Flex | Parser-generation tools used by the native build |
| GCC/Clang and ASan/UBSan | Compilation and focused memory/undefined-behavior checks |
| Ghostscript | PostScript-to-PDF conversion |
| GitHub Actions | Linux build/regression verification |

The wider macOS effort also used Objective-C/Cocoa for a small Finder launcher, XQuartz, private Tcl/Tk builds, Mach-O dependency relocation, `otool`, `install_name_tool`, `codesign` and `ditto`. TkGate's interface itself was not rewritten in Cocoa.

## Repository layout

| Path | Purpose |
|---|---|
| [`.binder/apt.txt`](.binder/apt.txt) | Native build, desktop, VNC, font and printing packages |
| [`.binder/requirements.txt`](.binder/requirements.txt) | Python desktop-proxy dependency |
| [`.binder/postBuild`](.binder/postBuild) | Compile/install, require tests to pass and create desktop launchers |
| [`.binder/start`](.binder/start) | Extend PATH and preserve Binder's startup command |
| [`.binder/USER-GUIDE.md`](.binder/USER-GUIDE.md) | Short student instructions, also copied to the desktop |
| [`.github/workflows/linux.yml`](.github/workflows/linux.yml) | Ubuntu CI build and failure diagnostics |
| [`src/common`](src/common) | Shared hash, allocator and other support code |
| [`src/tkgate`](src/tkgate) | Native circuit editor and application integration |
| [`src/verga`](src/verga) | Simulation engine, including multiword value operations |
| [`scripts`](scripts) | Tcl UI and simulator/peripheral orchestration |
| [`macos/test.py`](macos/test.py) | Cross-platform CLI regression runner; the directory name is historical |
| [`test/common`](test/common) | Pointer-hash and allocator regressions |
| [`test/verga`](test/verga) | Verga fixtures and expected output |
| [`hosting`](hosting) | Prepared Kasm Docker deployment and curated-source exporter |
| [`SOURCE-SHA256SUMS`](SOURCE-SHA256SUMS) | Checksums for the declared exported-source file list |
| [`COPYING`](COPYING) | Upstream GNU GPL license |

The checksum manifest is an inventory of its declared paths, not a checksum of every later-added configuration or documentation file. The publishing repository was created from a curated source export, so its initial commit includes inherited upstream code and does not preserve the original upstream Git ancestry.

## Build and startup lifecycle

1. Binder installs the system packages in `apt.txt` and Python requirements.
2. `postBuild` switches to the repository root and enables Bash failure handling with `set -euo pipefail`.
3. It creates a Tcl/Tk configuration shim under `~/.cache/tkgate-tcl-config`, linking the distribution's multiarch `tclConfig.sh` and `tkConfig.sh` into the layout expected by configure.
4. It runs `autogen.sh`, configures with `-O2 -std=gnu99 -fcommon`, compiles with `make -j2`, and installs into `~/.local/tkgate`.
5. It requires the simulator/Gmac suite, pointer-hash regression and allocator sanitizer regression to pass. A failing test fails the image build.
6. It creates `~/Circuits`, desktop shortcuts, an XFCE autostart entry and `~/.local/bin/tkgate-binder`.
7. The application wrapper sets `TKGATE_HOME`, changes to `~/Circuits` and executes the installed TkGate with the supplied arguments.
8. `.binder/start` extends PATH and calls `exec "$@"`, preserving Binder's Jupyter command and authentication/port arguments.
9. Opening the desktop starts the graphical session, whose autostart entry launches TkGate.

The launcher heredoc is quoted so `$HOME` and `$@` are expanded when the launcher runs. The desktop-entry heredoc expands HOME during setup to record its installed executable path. Tcl uses proper argument lists for paths with spaces; no separate public VNC endpoint is opened by these scripts.

Pinning a Git revision fixes source contents, but does not freeze all apt packages, transitive Python dependencies or Binder base images. The environment is not fully dependency-locked.

## Source fixes and their reasoning

The original source baseline for the wider project was [`bnoordhuis/tkgate` at `856c40542d3ee5ab0c23cb86a2a4ca0ba623619f`](https://github.com/bnoordhuis/tkgate/tree/856c40542d3ee5ab0c23cb86a2a4ca0ba623619f).

| Area / files | Problem and implemented logic |
|---|---|
| [`configure.ac`](configure.ac), `config.h.in` | Prefer Tcl/Tk 8.6 and accept a private Tcl/Tk prefix. The generated header template also contains Autoconf refresh churn. |
| [`hash.h`](src/common/hash.h), [`hash.c`](src/common/hash.c) | Integer casts truncated 64-bit pointer keys. Numeric key storage/APIs now use `uintptr_t`; bucket hashing folds high bits while comparisons retain the complete key. |
| Editor hash call sites | Circuit, edit state, module, print, selection and verification code now passes pointer-width keys instead of truncating pointers. |
| [`ycmalloc.c`](src/common/ycmalloc.c) | Pool poisoning wrote a platform-sized `long` at four-byte intervals. On LP64, an eight-byte write could cross bounds. Fixed-width `uint32_t` poisoning uses bounded `memcpy` writes. |
| [`verilog_in.c`](src/tkgate/verilog_in.c) | Array growth could copy using the expanded count, and pin growth referenced the wrong source array. Preserve old capacities and copy from the matching original arrays. |
| [`dip.c`](src/tkgate/dip.c) | Correct the property callback declaration to match its implementation and dispatch contract. |
| [`tkgatewin.c`](src/tkgate/tkgatewin.c) | Retain Tcl argument objects across evaluation and release them afterward, respecting object lifetime. |
| Tcl startup/simulation scripts | Use Tcl lists for sourced paths and process arguments so spaces remain within arguments. VPD substitution disables command and backslash evaluation where only variable substitution is intended. |
| [`module.c`](src/tkgate/module.c) | Replace a shell-interpolated HDL scanner invocation with pipe/fork/dup2/exec, explicit arguments and child-status handling. Bound digest formatting as well. |
| [`value.c`](src/verga/value.c) | Correct final partial-word masking, low-word extraction and decimal conversion behavior for multiword values. |
| [`channel1.out`](test/verga/channel1.out) | Correct stale `writting` expectations to `writing`, matching the existing fixture program. |

### Why the first Binder build failed

The initial build reached **65/66 passing CLI checks** and failed the wide-value regression. A short decimal literal such as `65'd0` took a fast conversion path that assigned the low word without clearing all upper words. Reinitializing storage did not guarantee those words were zero. The Mac run had passed, but the Linux allocation state exposed the defect.

The fix calls `Value_zero(S)` after `Value_reinit(...)` before assigning the parsed low word. The whole declared value is initialized, including high words. The test was retained; it was not skipped to make deployment succeed. See [the fix commit](https://github.com/ritesh123malik/tkgate-binder/commit/b5b0b2e9bef172ef61a29de4d10a6124f40ce5b9).

## Testing and recorded results

| Check | Result / meaning |
|---|---|
| 65 Verga fixtures + 1 Gmac memory-image comparison | 66/66 passed in the recorded corrected Linux build |
| Pointer-hash regression | Tests full-width keys sharing low bits, duplicate handling, lookup, iteration, replacement and removal |
| Allocator regression | Repeated pool allocation/free under AddressSanitizer and UndefinedBehaviorSanitizer |
| Wide-value fixture | Exercises 65-bit zero/high-bit values, decimal formatting, unknown/high-impedance handling and indexed bits |
| Local Mac GUI integration | Recorded six example save/reopen cycles, simulator start/step/stop, nonempty PostScript export and an AND-gate save |
| Browser screenshot | User evidence of a running editor and saved circuit listing; not a full automated browser test |

Historical Linux runs: [failure before the fix](https://github.com/ritesh123malik/tkgate-binder/actions/runs/39236834745) and [passing build after the fix](https://github.com/ritesh123malik/tkgate-binder/actions/runs/39237036554).

The fixture runner uses isolated working directories, process timeouts and expected-output comparisons. It narrowly normalizes contiguous same-time probe notifications in `probe1.v`, because pointer-hash iteration can reorder independent nets. It does not broadly ignore output ordering or whitespace. Gmac output is compared with the expected memory image.

**CI boundaries:** Ubuntu CI runs `.binder/postBuild` with native build dependencies. It does not install and exercise the entire VNC/XFCE/Jupyter browser stack. A green badge is evidence of native build/regression success, not complete browser validation. Mac GUI smoke tests likewise do not prove semantic equivalence of every saved circuit, waveform accuracy, rendered print quality or all peripheral behavior. Locale fallback and teardown warnings were observed in the historical GUI run.

## Build and test on Linux

Use a disposable Ubuntu environment or an account where creating `~/Circuits`, desktop files and autostart entries is appropriate. The commands below reproduce the native CI path; they do not create a public Binder service or install the whole browser desktop stack.

```sh
git clone https://github.com/ritesh123malik/tkgate-binder.git
cd tkgate-binder
sudo apt-get update
sudo apt-get install -y build-essential autoconf automake libtool libtool-bin \
  bison flex tcl8.6-dev tk8.6-dev libx11-dev
bash .binder/postBuild
```

A graphical X11 environment is required to open TkGate interactively. Rerun the CLI suite using the installed prefix:

```sh
python3 macos/test.py --prefix "$HOME/.local/tkgate"
```

Run focused regressions from the repository root:

```sh
cc -Isrc/common test/common/hash_pointer.c src/common/hash.c \
  -o /tmp/tkgate-hash-test
/tmp/tkgate-hash-test

cc -O0 -g -fsanitize=address,undefined -fno-sanitize-recover=all \
  -Isrc/common test/common/ycmalloc_pool.c src/common/ycmalloc.c \
  -o /tmp/tkgate-pool-test
/tmp/tkgate-pool-test

"$HOME/.local/tkgate/bin/verga" -q test/verga/widevalue.v
```

For the actual Binder environment, the `.binder` files are the build inputs; launch this repository through Binder. Do not interpret successful native commands as a completed public deployment or an isolation test.

## macOS work and distribution status

The wider project built Tcl/Tk **8.6.16** privately with X11 support and created an Apple Silicon app bundle using XQuartz. A small Cocoa launcher forwarded Finder/command-line file arguments to the existing application. Packaging relocated Mach-O dependencies, rewrote loader paths, retained XQuartz as an external prerequisite, generated an app ZIP/source archive and applied ad-hoc signatures.

Important distribution boundaries:

- This Binder checkout contains `macos/test.py`, but **not** the full Mac build, launcher, packaging or GUI-test files. Do not expect `macos/build.sh` or `macos/package.py` here.
- The local package recorded macOS 11 as its deployment target; that is not evidence of testing on macOS 11. Intel and clean-machine installation were not verified.
- Ad-hoc signing is not Developer ID signing or Apple notarization.
- The existing local Mac ZIP and paired source archive predate the final Linux decimal-parser fix. Rebuild, test and repackage before claiming a Mac release contains that fix.
- No downloadable Mac release is promised by this README. Browser use is the distribution path provided by this repository.

The REA skill was installed during the wider investigation, but this work primarily used the available source and normal build/debugging tools. No Hopper/Ghidra decompilation or native REA-engine evidence is claimed.

## Alternative hosting: Kasm and Oracle

The [`hosting`](hosting) directory preserves an earlier deployment design: build TkGate in an Ubuntu builder stage and serve it in a Kasm graphical runtime with separate visitor sessions. The source exporter creates a curated context and bundled source/license material.

**This route was not deployed.** Oracle account/VM setup was not completed, and the Kasm Docker image was not built or runtime-tested. Binder was chosen after the account/payment-verification requirement became unsuitable for the requested access route.

The [hosting README](hosting/README.md) is historical preparation material. Its statement that no public service existed refers to that earlier Kasm effort; the later Binder work is described here. Provider pricing, allocations, licensing and availability must be checked afresh before following that route. It would require its own image, HTTPS, capacity, isolation and functional acceptance checks.

## Troubleshooting

| Symptom | What to inspect or do |
|---|---|
| Binder image build fails | Expand build logs and locate the first failed command/test. Keep the actual error, revision and fixture name. |
| Old build reports 65/66 tests | Check whether the launch URL predates the wide-decimal initialization fix; use a link above. Do not remove the regression test. |
| Long launch or temporary unavailability | Shared Binder capacity or rebuilding may be involved; retry later and retain a fallback for scheduled labs. |
| Desktop opens without TkGate | Try its desktop launcher; check the native process, `TKGATE_HOME` and XFCE autostart entry. |
| A saved circuit is missing on your laptop | TkGate saved remotely. Download from the same running session's JupyterLab file browser. |
| A fresh session does not contain old work | Upload your downloaded copy. This repository provides no persistent session backup. |
| Simulation fails for a custom circuit | Include the circuit and any HDL, library or memory files needed to reproduce it; inspect simulator diagnostics. |
| Printing does not reach a local printer | Export PostScript, convert/download PDF and print locally. |
| A fix is absent from a pinned launch | The commit in the URL does not change automatically. Select a newer revision deliberately. |
| CI passes but desktop behavior fails | CI validates the native build path, not the full browser integration. Report the browser workflow separately. |

## Maintenance and contributions

Report reproducible problems through [GitHub Issues](https://github.com/ritesh123malik/tkgate-binder/issues). Include the source revision/launch link, browser and OS, exact steps, expected/actual result, relevant build or simulator output and a minimal non-sensitive circuit. Remove session URLs, tokens and private information from screenshots/logs.

For a source change:

1. Make the smallest relevant change and add a regression where it proves the defect.
2. Run the CLI suite and relevant focused tests; use a real desktop for UI changes.
3. Check the Linux workflow after pushing.
4. Verify the actual browser workflow separately when deployment/UI behavior changes.
5. Create a new pinned launch link if the shared version should change.
6. Refresh any checksum entries whose declared source files changed; do not present the manifest as covering paths it does not list.

Outstanding work includes full browser editing/simulation/peripheral validation, file-transfer round trips, print inspection, two-session isolation checks, disconnect/timeout behavior, classroom capacity testing and a current signed/notarized Mac release. These are acceptance tasks, not completed features.

## Project history

1. Started from the existing TkGate source and investigated macOS/XQuartz compatibility.
2. Fixed 64-bit pointer handling, allocator/parser correctness, Tcl lifetime/argument handling and simulator multiword values.
3. Built a local Apple Silicon package and added CLI/focused/GUI smoke tests.
4. Prepared an Oracle/Kasm route without deploying it.
5. Published a curated Binder source repository with desktop startup and student instructions.
6. Reproduced the initial Binder failure in Ubuntu CI and fixed wide decimal literal initialization.
7. Recorded the passing Linux build; a later user screenshot showed the running Binder editor.
8. Documented temporary storage, sharing/privacy boundaries and remaining validation work.

Publication milestones: [`dd24f38`](https://github.com/ritesh123malik/tkgate-binder/commit/dd24f38) (initial export/Binder), [`370aa20`](https://github.com/ritesh123malik/tkgate-binder/commit/370aa20) (Linux CI), [`b5b0b2e`](https://github.com/ritesh123malik/tkgate-binder/commit/b5b0b2e) (decimal fix), [`259c88d`](https://github.com/ritesh123malik/tkgate-binder/commit/259c88d) (passing results/source hashes). The initial export's full line count includes upstream source; it is not newly authored code.

## License, attribution and references

TkGate was created by **Jeffery P. Hansen**. This project is based on the [bnoordhuis/tkgate source repository](https://github.com/bnoordhuis/tkgate). TkGate is distributed under **GNU GPL version 2 or, at your option, any later version**; see [COPYING](COPYING) and retained source notices. Dependencies retain their own licenses. Preserve applicable notices and corresponding-source obligations when distributing modified binaries.

- [TkGate manual](https://bnoordhuis.github.io/tkgate/): editing, modules, HDL, simulation, Gmac and peripheral documentation.
- [Student guide](.binder/USER-GUIDE.md): concise session and file-transfer instructions.
- [Binder usage guidelines](https://mybinder.readthedocs.io/en/latest/about/user-guidelines.html): current service policies and limits.
- [repo2docker configuration reference](https://repo2docker.readthedocs.io/en/latest/configuration/): environment build inputs.
- [Jupyter remote desktop proxy](https://github.com/jupyterhub/jupyter-remote-desktop-proxy): browser desktop integration.
- [Linux CI workflow](.github/workflows/linux.yml): executable native-build validation.

This project makes an existing educational tool easier to access while retaining its native implementation. Keep local copies of your circuits and treat the documented validation boundaries as part of using and maintaining the service.
