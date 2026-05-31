variable "yc_token" {
  description = "OAuth token или IAM token для доступа к Yandex Cloud"
  type        = string
  sensitive   = true
}

variable "cloud_id" {
  description = "ID облака в Yandex Cloud"
  type        = string
}

variable "folder_id" {
  description = "ID каталога в Yandex Cloud"
  type        = string
}

variable "zone" {
  description = "Зона доступности Yandex Cloud"
  type        = string
  default     = "ru-central1-a"
}

variable "subnet_cidr" {
  description = "CIDR подсети для виртуальной машины"
  type        = string
  default     = "10.10.1.0/24"
}

variable "ssh_user" {
  description = "Пользователь для SSH-подключения к ВМ"
  type        = string
  default     = "ubuntu"
}

variable "ssh_public_key_path" {
  description = "Путь к публичному SSH-ключу"
  type        = string
  default     = "~/.ssh/id_rsa.pub"
}

variable "docker_image" {
  description = "Docker-образ приложения из Docker Hub"
  type        = string
  default     = "dockerhub_username/students-api:latest"
}
