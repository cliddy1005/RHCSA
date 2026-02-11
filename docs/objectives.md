# RHCSA EX200 Objective Domains (RHEL 10-aligned headings)

> This simulator maps to public objective headings only. No Red Hat copyrighted lab prose or NDA content is included.

## Understand and use essential tools
- Access systems and use help.
- Operate with files, text, archiving, links, and permissions.
- Manage input/output redirection and regular expressions.

## Operate running systems
- Boot/reboot/shutdown and switch targets.
- Manage processes, services, logs, timers, and software updates.
- Configure time synchronization.

## Configure local storage
- Partition with GPT.
- Create/manage LVM and filesystems.
- Configure mount persistence and swap.

## Create and configure file systems
- Create and mount filesystems.
- Configure auto-mounting and permissions/ACLs.
- Manage NFS client mounts.

## Deploy, configure, and maintain systems
- Configure networking and hostname resolution.
- Manage software repositories.
- Configure firewall and SELinux contexts/booleans.

## Manage users and groups
- Create/modify/delete users and groups.
- Configure password aging and sudo policy.

## Manage security
- Configure SSH keys and access.
- Apply SELinux and basic hardening practices.

## Mapping notes
- `tasks/taskbank.yml` includes objective_domain for each task.
- `grader/ansible/checks/*.yml` provide objective-aligned checks.
- Persistence checks are run after reboot in `grader/ansible/grade.yml`.
