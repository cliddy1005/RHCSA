# Lab Topology

## Nodes
- `infra.lab.example` (`192.168.50.10`, `fd00:50::10`): internal services (HTTP RPM repo, Flatpak repo, NFS, chrony).
- `node1.lab.example` (`192.168.50.11`, `fd00:50::11`): student target.
- `node2.lab.example` (`192.168.50.12`, `fd00:50::12`): student target.

## Network plan
- Isolated lab subnet: `192.168.50.0/24` and `fd00:50::/64`.
- Default behavior: outbound internet blocked using host/guest firewall controls via `scripts/netblock.sh` and hardening role.
- DNS can be set to infra or static entries in `/etc/hosts`.

## Storage plan
- Base disk per node from user-provided RHEL 10 image.
- Two extra virtual disks per student node for GPT/LVM tasks.

## Naming
- Domain defaults to `lab.example`, configurable in `config/lab.yml`.
