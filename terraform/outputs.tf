output "external_ip" {
  description = "Публичный IP-адрес виртуальной машины"
  value       = yandex_compute_instance.students_api_vm.network_interface[0].nat_ip_address
}

output "service_url" {
  description = "URL сервиса после развёртывания"
  value       = "http://${yandex_compute_instance.students_api_vm.network_interface[0].nat_ip_address}"
}
