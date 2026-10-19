# TkGate in a browser: Oracle VM + Kasm

Status: deployment preparation only. The Docker image has **not been built or
run** on Linux, and no public service exists yet. macOS verification does not
validate this container or browser integration. This serves the actual TkGate,
Verga and Gmac programs in separate graphical Linux sessions.

## Account and VM

Create an [Oracle Cloud Free Tier account](https://www.oracle.com/cloud/free/)
yourself, including its identity/payment verification and terms. In the home
region, create an **Always Free eligible** Ampere A1 Flex VM, Ubuntu 22.04 ARM64,
2 OCPUs, 12 GB RAM and an 80 GB boot volume. Check the console's estimate before
creating it; do not select paid resources or upgrade the account automatically.
Use a public subnet/public IP and your SSH public key. Keep the private key on
your computer; provide only the IP/SSH alias and username (`ubuntu`) to continue.

Oracle's current free allocation is 1,500 OCPU-hours and 9,000 GB-hours monthly
(2 OCPUs/12 GB continuously), with 200 GB total block storage across the tenancy.
Availability varies, and idle free VMs may be reclaimed. This is not guaranteed
permanent hosting. [Oracle limits](https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm)

Allow inbound TCP 443 for visitors and SSH 22 only from your administration IP
in both Oracle's network rules and the host firewall. No public VNC, Docker,
database or RDP ports are needed. Reserve a hostname pointing at the VM for
trusted HTTPS. Account creation, VM provisioning and hostname selection remain
outstanding.

## Prepare and transfer the source

On the Mac, from the repository root (Python 3.9+ and Git required):

```sh
python3 hosting/prepare-context.py hosting/build/context
tar -czf hosting/build/tkgate-context.tar.gz -C hosting/build/context .
```

The destination must be new. The exporter uses tracked working-tree files plus
an explicit list of new tests/hosting files; it excludes dotfiles and macOS
build products. Review `source/SOURCE-SHA256SUMS` before transferring the archive
to your VM with `scp`. The image includes the modified TkGate source and GPL
license under `/usr/share/doc/tkgate`. Build inputs and test fixtures are retained.

## Install the session service on the VM

Use a dedicated VM. Follow Kasm's [single-server installation](https://www.kasmweb.com/docs/latest/install/single_server_install.html)
for version 1.17.0. The official installer download is
`https://kasm-static-content.s3.amazonaws.com/kasm_release_1.17.0.7f020d.tar.gz`;
verify SHA-256
`22a293ea52b2adb7f3f72a2de8e9be799f443b9da040e066df403478da77f62d`
before extracting and running `sudo bash kasm_release/install.sh`. Review its
license interactively. Save the generated administrator password privately,
change it on first login, and remove or disable the default regular user.

Install a trusted certificate and renewal using the
[Kasm certificate guide](https://www.kasmweb.com/docs/latest/how_to/certificates.html)
before public launch. Test the hostname without bypassing certificate warnings.

Extract the transferred build context into a new directory and, inside it, run:

```sh
sudo docker build --pull -t tkgate-browser:1.17.0 .
```

The build runs the simulator/Gmac suite and allocator sanitizer regression;
failure stops the build. It uses the official ARM64-capable
[`core-ubuntu-jammy:1.17.0` image](https://www.kasmweb.com/docs/latest/guide/custom_images.html)
and [custom startup hook](https://www.kasmweb.com/docs/latest/how_to/building_images.html).
Record the resulting image digest. Refresh/retest the base periodically for
security updates; release tags alone do not make a reproducible image.

## Register and publish separate sessions

In Kasm administration, add a container Workspace with image
`tkgate-browser:1.17.0`, CPU allocation 1 and memory 2048 MB initially. Keep it
local to this single agent; disable automatic pruning of this locally built
image. Use a dedicated visitor group with access only to this workspace.
Start with **two concurrent sessions**, verify actual resource usage, and reserve
capacity for the control services. Kasm CE permits at most **five concurrent
sessions** for testing, non-profit and non-commercial use; commercial deployment
needs a suitable license. [Kasm licensing](https://www.kasmweb.com/docs/develop/license.html)

Create a [Casting configuration](https://www.kasmweb.com/docs/latest/guide/casting.html)
for this workspace, enabling anonymous users in the visitor group. Leave sharing
and dynamic Docker network selection off. Enable uploads/downloads and keep the
control panel visible. Rate-limit launches per IP (start at one per 60 seconds).
Configure session/resource quotas in the agent/group, not Casting's **Limit Total
Session**, which is a lifetime launch counter. Set an idle timeout of 30 minutes
and explain this to visitors. Do not enable persistent profiles for anonymous
sessions. Publish only the actual generated Casting URL after acceptance checks.

Visitors save circuits inside their own container and download before ending
the session. Print to PostScript/PDF and download; local physical printers and
local filesystem paths are not directly available in a browser session. This
deployment has no host mounts, privileged containers or Docker socket inside
visitor sessions. Keep those restrictions and user 1000 when configuring it.
Restrict visitor egress to prevent access to cloud metadata, host management and
other sessions; verify these rules against Docker networking before launch.

## Required acceptance checks before calling this live

- Image builds on the chosen ARM VM; all embedded command-line tests pass.
- Two fresh browsers receive separate desktops; files and session identifiers
  are inaccessible from the other session. A third launch respects capacity.
- Create, edit, save, download, upload and reopen a circuit; verify its contents.
- Run combinational and sequential simulations; exercise HDL modules, probes,
  breakpoints, memory initialization, Gmac, TTY and drink-machine peripherals.
- Export PostScript, convert with `ps2pdf`, and download/read the PDF.
- Exercise module/interface editing, libraries and options against
  `macos/FEATURE-CHECKLIST.md`; browser-specific results must be recorded separately.
- Verify HTTPS renewal, disconnect/resume behavior, idle termination, VM restart,
  quotas, disk usage and blocked metadata/host/cross-session access.

Unverified: all Linux image build/runtime checks above, public session isolation,
file transfer, browser feature parity and capacity. A free VM cannot serve an
unlimited number of simultaneous visitors.
