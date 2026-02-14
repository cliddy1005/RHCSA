# rhcsa-ex200-simulator

A local, exam-like RHCSA EX200 practice environment generator for RHEL 10-style objectives.

## Disclaimer
- This is **not** an official Red Hat product.
- Contains **no** NDA or copyrighted Red Hat lab content.
- Tasks are original and mapped to public objective domains.

## Features
- Deterministic 3-VM lab (`infra`, `node1`, `node2`) via libvirt/KVM (preferred) with Vagrant/VirtualBox fallback.
- Default isolated networking with outbound internet blocked.
- Internal infra services: HTTP RPM repo, Flatpak repo, NFS exports, chrony/NTP.
- Exam workflow: generate brief, run 180-minute timer, grade (including reboot persistence), reset baseline.
- Weighted scoring to 300 points with configurable pass threshold (default 210).

## Prerequisites
- Host: RHEL/Fedora/other Linux with KVM/libvirt.
- Tools: `terraform`, `ansible-core`, `python3`, `jq`, `virsh`.
- Optional fallback: `vagrant`, `virtualbox`.
- User-provided RHEL 10 assets (licensed): cloud-init qcow2 image preferred, or installer ISO.

## Quick dependency install
- Python deps: `python3 -m pip install -r requirements/python.txt`
- Host deps: see `requirements/system-packages.txt` and distro examples in `requirements/README.md`.

## macOS quick start
1. Install dependencies from `requirements/README.md` (Homebrew section).
2. Set `provider: virtualbox` in `config/lab.yml`.
3. Run `./scripts/examctl provision`.

## Configure lab
1. Edit `config/lab.yml` (CPU/RAM/disk/IPs/domain/image paths).
2. Copy `config/secrets.sample.yml` -> `config/secrets.yml` (gitignored) for local secrets if needed.

## Provision
```bash
./scripts/examctl provision
```

## Start an exam
```bash
./scripts/examctl start
```
- Restores baseline snapshot.
- Generates `tasks/exams/current_exam.md` from taskbank.
- Starts a local 180-minute timer.
- Prints SSH access instructions.

## Grade (state + persistence)
```bash
./scripts/examctl grade
```
- Runs primary checks.
- Reboots `node1`/`node2`.
- Re-runs persistence checks.
- Produces `artifacts/results.json` and `artifacts/results.md`.
- Prints final score and PASS/NO PASS.

## Reset
```bash
./scripts/examctl reset
```

## Repo map
- `docs/`: objective mapping, topology, usage.
- `terraform-libvirt/`: preferred provisioning path.
- `vagrant/`: optional fallback.
- `ansible/`: provisioning and baseline management.
- `tasks/`: task bank and exam template.
- `grader/`: assertion checks + optional testinfra.
- `scripts/examctl`: CLI orchestration.
