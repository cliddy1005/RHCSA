# Requirements

This folder centralizes dependencies needed by `rhcsa-ex200-simulator`.

## Files
- `python.txt`: Python packages for local tooling/checks.
- `system-packages.txt`: host packages grouped by platform notes.

## Install commands

### Python dependencies
```bash
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements/python.txt
```

### macOS (Homebrew) - recommended for this repo on Mac
```bash
brew update
brew install terraform ansible jq vagrant
brew install --cask virtualbox
```

> macOS should use the VirtualBox fallback provider. KVM/libvirt instructions are Linux-only.

### Linux RHEL/Fedora host packages
```bash
sudo dnf install -y terraform libvirt qemu-kvm virt-install ansible-core jq
# Optional fallback provider
sudo dnf install -y vagrant VirtualBox
```

### Linux Debian/Ubuntu host packages
```bash
sudo apt-get update
sudo apt-get install -y libvirt-daemon-system qemu-kvm virtinst ansible jq vagrant virtualbox
# Terraform package availability varies by distro release; install via HashiCorp apt repo if missing.
```

## Verify
```bash
terraform version
ansible --version
vagrant --version
VBoxManage --version
python3 -m pip show ansible-core
```
