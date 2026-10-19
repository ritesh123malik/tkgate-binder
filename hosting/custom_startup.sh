#!/usr/bin/env bash
set -euo pipefail
# Kasm invokes this hook as the individual session's unprivileged user.
/usr/bin/desktop_ready
mkdir -p "$HOME/Documents" "$HOME/Desktop"
cd "$HOME/Documents"
/opt/tkgate/bin/tkgate > "$HOME/tkgate-session.log" 2>&1 &
