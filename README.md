# students-api

Учебный проект для КубГТУ, 5 курс.

`students-api` — это небольшой сервис учёта студентов. Он позволяет получить список студентов, найти студента по ID, добавить нового студента и вывести студентов конкретной группы.

В задании среди идей был указан Flask, но в стеке указан FastAPI, поэтому проект выполнен на **FastAPI**.

---

## 1. Стек проекта

- Python 3.11
- FastAPI
- JSON-файл для хранения данных
- Docker
- Docker Hub
- Terraform
- Yandex Cloud
- Kubernetes
- Minikube

---

## 2. Структура проекта

```text
students-api/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── schemas.py
│   └── students.json
│
├── Dockerfile
├── requirements.txt
├── README.md
│
├── terraform/
│   ├── versions.tf
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
│
└── k8s/
    ├── namespace.yaml
    ├── deployment.yaml
    └── service.yaml
```

---

## 3. Эндпоинты

| Метод | URL | Назначение |
|---|---|---|
| GET | `/` | Проверка работы сервиса |
| GET | `/students` | Получить всех студентов |
| GET | `/students/{student_id}` | Найти студента по ID |
| GET | `/students/group/{group_name}` | Получить студентов конкретной группы |
| POST | `/students` | Добавить нового студента |

После запуска сервиса автоматическая документация доступна по адресу:

```text
http://127.0.0.1:8000/docs
```

---

## 4. Пример данных

Файл с данными находится здесь:

```text
app/students.json
```

Пример записи:

```json
{
  "id": 1,
  "full_name": "Иванов Иван Иванович",
  "group": "ИБ-21",
  "course": 3,
  "average_grade": 4.6
}
```

---

## 5. Локальный запуск без Docker

Перейдите в папку проекта:

```bash
cd students-api
```

Создайте виртуальное окружение:

```bash
python -m venv .venv
```

Активируйте виртуальное окружение.

Для Windows PowerShell:

```bash
.venv\Scripts\Activate.ps1
```

Для Linux или macOS:

```bash
source .venv/bin/activate
```

Установите зависимости:

```bash
pip install -r requirements.txt
```

Запустите приложение:

```bash
uvicorn app.main:app --reload
```

Проверьте работу:

```bash
curl http://127.0.0.1:8000/
curl http://127.0.0.1:8000/students
```

---

## 6. Примеры запросов

### Получить всех студентов

```bash
curl http://127.0.0.1:8000/students
```

### Найти студента по ID

```bash
curl http://127.0.0.1:8000/students/1
```

### Найти студентов группы

```bash
curl http://127.0.0.1:8000/students/group/ИБ-21
```

### Добавить студента

```bash
curl -X POST http://127.0.0.1:8000/students \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Кузнецова Мария Андреевна",
    "group": "ИБ-23",
    "course": 1,
    "average_grade": 4.7
  }'
```

---

## 7. Упаковка сервиса в Docker

Соберите Docker-образ:

```bash
docker build -t students-api .
```

Запустите контейнер:

```bash
docker run -d --name students-api -p 8000:8000 students-api
```

Проверьте работу:

```bash
curl http://127.0.0.1:8000/students
```

Остановить и удалить контейнер:

```bash
docker rm -f students-api
```

---

## 8. Загрузка образа в Docker Hub

Войдите в Docker Hub:

```bash
docker login
```

Замените `dockerhub_username` на свой логин Docker Hub:

```bash
docker tag students-api dockerhub_username/students-api:latest
docker push dockerhub_username/students-api:latest
```

После загрузки образ будет доступен в Docker Hub.

---

## 9. Развёртывание в Yandex Cloud через Terraform

Terraform-файлы находятся в папке:

```text
terraform/
```

Перед запуском нужно подготовить:

- аккаунт Yandex Cloud;
- `cloud_id`;
- `folder_id`;
- токен `yc_token`;
- SSH-ключ;
- загруженный Docker-образ в Docker Hub.

Перейдите в папку Terraform:

```bash
cd terraform
```

Инициализируйте Terraform:

```bash
terraform init
```

Посмотрите план создания инфраструктуры:

```bash
terraform plan \
  -var="yc_token=ВАШ_ТОКЕН" \
  -var="cloud_id=ВАШ_CLOUD_ID" \
  -var="folder_id=ВАШ_FOLDER_ID" \
  -var="docker_image=dockerhub_username/students-api:latest"
```

Создайте инфраструктуру:

```bash
terraform apply \
  -var="yc_token=ВАШ_ТОКЕН" \
  -var="cloud_id=ВАШ_CLOUD_ID" \
  -var="folder_id=ВАШ_FOLDER_ID" \
  -var="docker_image=dockerhub_username/students-api:latest"
```

После выполнения Terraform выведет публичный IP-адрес виртуальной машины и URL сервиса.

Удалить созданную инфраструктуру можно командой:

```bash
terraform destroy \
  -var="yc_token=ВАШ_ТОКЕН" \
  -var="cloud_id=ВАШ_CLOUD_ID" \
  -var="folder_id=ВАШ_FOLDER_ID" \
  -var="docker_image=dockerhub_username/students-api:latest"
```

---

## 10. Развёртывание в Minikube через Kubernetes

Kubernetes-манифесты находятся в папке:

```text
k8s/
```

Перед запуском замените в файле `k8s/deployment.yaml` строку:

```text
image: dockerhub_username/students-api:latest
```

на имя вашего Docker-образа.

Запустите Minikube:

```bash
minikube start
```

Примените манифесты:

```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

Проверьте поды и сервис:

```bash
kubectl get pods -n students-api
kubectl get svc -n students-api
```

Откройте сервис:

```bash
minikube service students-api-service -n students-api
```

Или получите адрес Minikube:

```bash
minikube ip
```

Тогда сервис будет доступен по адресу:

```text
http://MINIKUBE_IP:30080
```

Удалить ресурсы Kubernetes:

```bash
kubectl delete namespace students-api
```

---

## 11. Загрузка проекта в GitHub

В корне проекта выполните команды:

```bash
git init
git add .
git commit -m "Initial commit: students-api"
git branch -M main
git remote add origin https://github.com/username/students-api.git
git push -u origin main
```

`username` нужно заменить на свой логин GitHub.

---

## 12. Что реализовано по заданию

1. Создан проект `students-api`.
2. Реализован сервис на FastAPI для работы со списком студентов.
3. Данные хранятся в JSON-файле.
4. Реализованы эндпоинты `GET /`, `GET /students`, `GET /students/{student_id}`, `GET /students/group/{group_name}`, `POST /students`.
5. Добавлен `Dockerfile` для упаковки сервиса в Docker.
6. Подготовлены инструкции для публикации образа в Docker Hub.
7. Добавлены Terraform-файлы для развёртывания в Yandex Cloud.
8. Добавлены Kubernetes-манифесты для развёртывания в Minikube.
9. Подготовлен README-файл с описанием проекта, запуском и командами.

---

## 13. Автор проекта

Проект подготовлен для учебного задания КубГТУ.
