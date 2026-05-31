provider "yandex" {
  token     = var.yc_token
  cloud_id  = var.cloud_id
  folder_id = var.folder_id
  zone      = var.zone
}

data "yandex_compute_image" "ubuntu" {
  family    = "ubuntu-2204-lts"
  folder_id = "standard-images"
}

resource "yandex_vpc_network" "students_network" {
  name = "students-api-network"
}

resource "yandex_vpc_subnet" "students_subnet" {
  name           = "students-api-subnet"
  zone           = var.zone
  network_id     = yandex_vpc_network.students_network.id
  v4_cidr_blocks = [var.subnet_cidr]
}

resource "yandex_compute_instance" "students_api_vm" {
  name        = "students-api-vm"
  platform_id = "standard-v3"
  zone        = var.zone

  resources {
    cores         = 2
    memory        = 2
    core_fraction = 20
  }

  boot_disk {
    initialize_params {
      image_id = data.yandex_compute_image.ubuntu.id
      size     = 20
      type     = "network-hdd"
    }
  }

  network_interface {
    subnet_id = yandex_vpc_subnet.students_subnet.id
    nat       = true
  }

  metadata = {
    ssh-keys = "${var.ssh_user}:${file(var.ssh_public_key_path)}"
    user-data = <<-EOF
      #cloud-config
      package_update: true
      packages:
        - docker.io
      runcmd:
        - systemctl enable docker
        - systemctl start docker
        - docker pull ${var.docker_image}
        - docker rm -f students-api || true
        - docker run -d --restart always --name students-api -p 80:8000 ${var.docker_image}
    EOF
  }
}
