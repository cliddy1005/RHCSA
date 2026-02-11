#!/usr/bin/env bash
set -euo pipefail

ACTION=${1:-status}
SUBNET4=${2:-192.168.50.0/24}

case "$ACTION" in
  apply)
    sudo iptables -C OUTPUT -d "$SUBNET4" -j ACCEPT 2>/dev/null || sudo iptables -I OUTPUT 1 -d "$SUBNET4" -j ACCEPT
    sudo iptables -C OUTPUT -j DROP 2>/dev/null || sudo iptables -A OUTPUT -j DROP
    echo "Applied egress block except $SUBNET4"
    ;;
  clear)
    sudo iptables -D OUTPUT -j DROP 2>/dev/null || true
    while sudo iptables -C OUTPUT -d "$SUBNET4" -j ACCEPT 2>/dev/null; do
      sudo iptables -D OUTPUT -d "$SUBNET4" -j ACCEPT || true
    done
    echo "Cleared egress block rules"
    ;;
  status)
    sudo iptables -S OUTPUT
    ;;
  *)
    echo "Usage: $0 {apply|clear|status} [subnet4]" >&2
    exit 1
    ;;
esac
