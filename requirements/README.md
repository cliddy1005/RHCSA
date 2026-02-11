# Requirements

This folder centralizes dependencies needed by `rhcsa-ex200-simulator`.

## Files
- `python.txt`: Python packages for local tooling/checks.
- `system-packages.txt`: host packages to install using your Linux package manager.

## Install commands

### Python dependencies
```bash
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements/python.txt
```

### RHEL/Fedora host packages
```bash
sudo dnf install -y terraform libvirt qemu-kvm virt-install ansible-core jq
# Optional fallback provider
sudo dnf install -y vagrant VirtualBox
```

### Debian/Ubuntu host packages
```bash
sudo apt-get update
sudo apt-get install -y libvirt-daemon-system qemu-kvm virtinst ansible jq vagrant virtualbox
# Terraform package availability varies by distro release; install via HashiCorp apt repo if missing.
```

## Verify
```bash
terraform version
ansible --version
virsh --version
python3 -m pip show ansible-core
```
