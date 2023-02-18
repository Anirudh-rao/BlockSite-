#!/bin/bash

set -euo pipefail
current_path="$(realpath $0)"
current_dir="$(dirname $current_path)"

function enable() {
	"$current_dir/venv/bin/python" "$current_dir/main.py" /etc/hosts ./sites.txt
}

function disable() {
	"$current_dir/venv/bin/python" "$current_dir/main.py" /etc/hosts ./sites.txt --disable
}

function help() {
	echo "Usage: $(basename "$0") [OPTIONS]

Commands:
  enable   Enable block
  disable  Disable block
  help     Show help
"
}

if [[ $1 =~ ^(enable|disable|help)$ ]]; then
	"$@"
else
	help
	exit 1
fi