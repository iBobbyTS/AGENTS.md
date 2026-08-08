#!/bin/sh
set -eu

repo_root=$(git rev-parse --show-toplevel 2>/dev/null) || {
  printf '%s\n' 'error: run this script from inside a Git repository.' >&2
  exit 1
}

hooks_dir="$repo_root/.githooks"
if [ ! -d "$hooks_dir" ]; then
  printf 'error: missing hook directory: %s\n' "$hooks_dir" >&2
  exit 1
fi

git -C "$repo_root" config --local core.hooksPath .githooks
printf 'Configured repository-local core.hooksPath: .githooks\n'
