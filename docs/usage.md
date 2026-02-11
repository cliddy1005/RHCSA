# Usage

## 1) Prepare prerequisites
- Install dependency lists from `requirements/` first (see `requirements/README.md`).
- Linux host with KVM/libvirt, `terraform`, `ansible`, `python3`, and `jq`.
- No external Python YAML dependency required by shipped scripts.
- Optional fallback: VirtualBox + Vagrant.
- Provide your own licensed RHEL 10 image/ISO under `images/`.

## 2) Configure lab
1. Edit `config/lab.yml`.
2. Copy `config/secrets.sample.yml` to `config/secrets.yml` for local credentials (if needed).

## 3) Provision
- Preferred:
  - `./scripts/examctl provision`
- Optional fallback:
  - `vagrant up`

## 4) Start exam session
- `./scripts/examctl start`
- This restores baseline, generates `tasks/exams/current_exam.md`, starts a 180-minute timer, and prints access hints.

## 5) Grade
- `./scripts/examctl grade`
- Runs checks once, reboots nodes, runs persistence checks, aggregates weighted score, emits PASS/NO PASS.
- Reports are written to `artifacts/results.json` and `artifacts/results.md`.

## 6) Reset
- `./scripts/examctl reset`

## 7) Cleanup
- `./scripts/examctl stop`
