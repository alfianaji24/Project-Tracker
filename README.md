# Project & Contract Management System

Aplikasi Django + PostgreSQL untuk mengelola project, customer, vendor, kontrak, TOP, dan nilai pekerjaan — sesuai PRD MVP.

## Tech Stack

- **Backend:** Django 5.1
- **Database:** PostgreSQL 16
- **Runtime:** Docker & Docker Compose

## Quick Start

### 1. Salin environment file

```bash
cp .env.example .env
```

### 2. Jalankan dengan Docker

```bash
docker compose up --build
```

Aplikasi tersedia di:
- **App UI:** http://localhost:8000/
- **Admin:** http://localhost:8000/admin/

### 3. Login default (development)

| Field    | Value            |
|----------|------------------|
| Username | `admin`          |
| Password | `admin123`       |

> Ganti password di production melalui variabel `DJANGO_SUPERUSER_*` di `.env`.

## Struktur Database

| Tabel              | Deskripsi                    |
|--------------------|------------------------------|
| `customers`        | Master customer              |
| `vendors`          | Master vendor                |
| `contract_types`   | PKS / PO                     |
| `project_types`    | Cloud / ITaaS / Project      |
| `tops`             | Terms of Payment             |
| `project_statuses` | Draft, On Going, Completed…  |
| `projects`         | Data project utama           |

## Business Rules (PRD)

- Semua kode bisnis: **4 huruf kapital** (contoh: `AWBS`, `DMAS`)
- `work_value`: DECIMAL(18,2)
- `contract_end_date >= contract_start_date`
- Master yang sudah dipakai project **tidak bisa dihapus** — gunakan status Active/Inactive

## Perintah Berguna

```bash
# Seed master data manual
docker compose exec web python manage.py seed_masters

# Buat superuser manual
docker compose exec web python manage.py createsuperuser

# Migration
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate
```

## Development Lokal (tanpa Docker)

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt

# Pastikan PostgreSQL jalan, set POSTGRES_HOST=localhost di .env
python manage.py migrate
python manage.py seed_masters
python manage.py createsuperuser
python manage.py runserver
```

## Fitur Phase 2

| Fitur | URL |
|-------|-----|
| Login | `/login/` |
| Project List + Filter | `/` |
| Tambah Project | `/projects/create/` |
| Detail Project | `/projects/<id>/` |
| Edit Project | `/projects/<id>/edit/` |
| Nonaktifkan Project | `/projects/<id>/deactivate/` |

Filter project berdasarkan: code/nama, customer, vendor, contract type, project type, TOP, status, tanggal kontrak.

## Roadmap (PRD)

- [x] Phase 1 — Database, Auth, Master Data
- [x] Phase 2 — Project CRUD, Search & Filter UI
- [ ] Phase 3 — Dashboard
- [ ] Phase 4 — Contract Management
