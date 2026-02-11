terraform {
  required_providers {
    libvirt = {
      source  = "dmacvicar/libvirt"
      version = ">= 0.7.0"
    }
  }
}

provider "libvirt" {
  uri = "qemu:///system"
}

resource "libvirt_network" "lab" {
  name      = var.network_name
  mode      = "nat"
  domain    = var.domain
  addresses = ["192.168.50.0/24", "fd00:50::/64"]
  dns { enabled = true }
}

locals {
  nodes = {
    infra = { ip4 = "192.168.50.10", vcpu = 2, memory = 4096 }
    node1 = { ip4 = "192.168.50.11", vcpu = 2, memory = 4096 }
    node2 = { ip4 = "192.168.50.12", vcpu = 2, memory = 4096 }
  }

  extra_disks = {
    node1 = ["node1-extra1.qcow2", "node1-extra2.qcow2"]
    node2 = ["node2-extra1.qcow2", "node2-extra2.qcow2"]
  }
}

resource "libvirt_volume" "base" {
  name   = "rhel10-base.qcow2"
  pool   = var.pool
  source = var.base_image
}

resource "libvirt_volume" "node_disk" {
  for_each       = local.nodes
  name           = "${each.key}.qcow2"
  pool           = var.pool
  base_volume_id = libvirt_volume.base.id
}

resource "libvirt_volume" "extra" {
  for_each = merge(
    { for idx, name in local.extra_disks.node1 : "node1-${idx}" => { vm = "node1", name = name } },
    { for idx, name in local.extra_disks.node2 : "node2-${idx}" => { vm = "node2", name = name } }
  )

  name   = each.value.name
  pool   = var.pool
  size   = 8 * 1024 * 1024 * 1024
  format = "qcow2"
}

resource "libvirt_cloudinit_disk" "common" {
  name      = "commoninit.iso"
  user_data = file("${path.module}/user-data.yaml")
}

resource "libvirt_domain" "vm" {
  for_each = local.nodes
  name     = each.key
  memory   = each.value.memory
  vcpu     = each.value.vcpu

  network_interface {
    network_id     = libvirt_network.lab.id
    addresses      = [each.value.ip4]
    wait_for_lease = true
  }

  disk { volume_id = libvirt_volume.node_disk[each.key].id }

  dynamic "disk" {
    for_each = each.key == "infra" ? [] : [for k, v in libvirt_volume.extra : v if startswith(k, each.key)]
    content {
      volume_id = disk.value.id
    }
  }

  cloudinit  = libvirt_cloudinit_disk.common.id
  qemu_agent = true
}
