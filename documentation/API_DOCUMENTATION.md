# Dokumentasi API Expense Tracker

## Daftar Isi

- [Pengenalan](#pengenalan)
- [Konfigurasi](#konfigurasi)
- [Autentikasi](#autentikasi)
- [Endpoint API](#endpoint-api)
  - [Health Check](#health-check)
  - [Autentikasi](#autentikasi-endpoints)
  - [Kategori](#kategori)
  - [Pengeluaran](#pengeluaran)
  - [Anggaran](#anggaran)
  - [Akun](#akun)
  - [Tag](#tag)
  - [Pengeluaran Berulang](#pengeluaran-berulang)
  - [Statistik](#statistik)
- [Penanganan Error](#penanganan-error)
- [Rate Limiting](#rate-limiting)
- [Keamanan](#keamanan)

## Pengenalan

API Expense Tracker adalah RESTful API untuk mengelola keuangan pribadi. API ini menyediakan endpoint untuk mengelola pengeluaran, anggaran, kategori, dan fitur-fitur lainnya.

### Base URL

```
http://localhost:8000/api/v1
```

### Format Response

Semua response API menggunakan format JSON yang konsisten:

```json
{
  "status": "success" | "error",
  "data": <response_data>,
  "message": "Pesan opsional yang menjelaskan hasil"
}
```

### Status Code

- `200`: OK (untuk operasi GET, PUT, DELETE yang berhasil)
- `201`: Created (untuk operasi POST yang berhasil)
- `400`: Bad Request (untuk input yang tidak valid)
- `401`: Unauthorized (untuk autentikasi yang gagal)
- `404`: Not Found (untuk resource yang tidak ditemukan)
- `500`: Internal Server Error (untuk kesalahan server)

## Konfigurasi

### Header Umum

Semua request harus menyertakan:

```
Content-Type: application/json
Accept: application/json
```

Untuk endpoint yang memerlukan autentikasi, tambahkan:

```
Authorization: Bearer <token>
```

## Autentikasi

API menggunakan JWT (JSON Web Token) untuk autentikasi. Token harus disertakan dalam header Authorization untuk mengakses endpoint yang dilindungi.

### Format Token

```
Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Durasi Token

- Token berlaku selama 30 menit
- Setelah expired, login ulang diperlukan untuk mendapatkan token baru

## Endpoint API

### Health Check

#### GET /api/v1/health

Memeriksa status kesehatan API.

**Response:**

```json
{
  "status": "success",
  "data": {
    "status": "ok",
    "version": "1.0.0",
    "timestamp": "2024-03-14T10:00:00.000Z"
  },
  "message": null
}
```

### Autentikasi Endpoints

#### POST /api/v1/auth/register

Mendaftarkan pengguna baru.

**Request Body:**

```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "StrongPass123!"
}
```

**Response:**

```json
{
  "status": "success",
  "data": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "created_at": "2024-03-14T10:00:00"
  },
  "message": "Pengguna berhasil didaftarkan"
}
```

#### POST /api/v1/auth/token

Login untuk mendapatkan token akses.

**Request Body:**

```json
{
  "username": "johndoe",
  "password": "StrongPass123!"
}
```

**Response:**

```json
{
  "status": "success",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "expires_in": 1800
  },
  "message": "Login berhasil"
}
```

#### GET /api/v1/auth/me

Mendapatkan informasi pengguna yang sedang login.

**Headers:**

```
Authorization: Bearer <token>
```

**Response:**

```json
{
  "status": "success",
  "data": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "created_at": "2024-03-14T10:00:00"
  },
  "message": null
}
```

### Kategori

#### GET /api/v1/categories/

Mendapatkan semua kategori pengeluaran.

**Query Parameters:**

- `skip` (opsional): Jumlah record yang dilewati (default: 0)
- `limit` (opsional): Jumlah maksimum record yang dikembalikan (default: 100)

**Response:**

```json
{
  "status": "success",
  "data": {
    "items": [
      {
        "id": 1,
        "name": "Makanan",
        "description": "Belanja dan makan di luar",
        "created_at": "2024-03-14T10:00:00",
        "updated_at": "2024-03-14T10:00:00"
      }
    ],
    "total": 1,
    "page": 1,
    "size": 10,
    "pages": 1
  },
  "message": null
}
```

#### POST /api/v1/categories/

Membuat kategori baru.

**Request Body:**

```json
{
  "name": "Transportasi",
  "description": "Angkutan umum dan bahan bakar"
}
```

**Response:**

```json
{
  "status": "success",
  "data": {
    "id": 2,
    "name": "Transportasi",
    "description": "Angkutan umum dan bahan bakar",
    "created_at": "2024-03-14T10:15:00",
    "updated_at": "2024-03-14T10:15:00"
  },
  "message": "Kategori berhasil dibuat"
}
```

### Pengeluaran

#### GET /api/v1/expenses/

Mendapatkan semua pengeluaran dengan filter opsional.

**Query Parameters:**

- `skip` (opsional): Jumlah record yang dilewati (default: 0)
- `limit` (opsional): Jumlah maksimum record yang dikembalikan (default: 100)
- `category_id` (opsional): Filter berdasarkan kategori
- `account_id` (opsional): Filter berdasarkan akun
- `start_date` (opsional): Filter pengeluaran dari tanggal (YYYY-MM-DD)
- `end_date` (opsional): Filter pengeluaran sampai tanggal (YYYY-MM-DD)
- `tag_ids` (opsional): Filter berdasarkan tag

**Response:**

```json
{
  "status": "success",
  "data": {
    "items": [
      {
        "id": 1,
        "amount": "35.50",
        "date": "2024-03-14",
        "description": "Belanja bulanan",
        "category": {
          "id": 1,
          "name": "Makanan"
        },
        "account": {
          "id": 1,
          "name": "Rekening Bank"
        },
        "tags": [
          {
            "id": 1,
            "name": "Penting"
          }
        ],
        "created_at": "2024-03-14T10:30:00",
        "updated_at": "2024-03-14T10:30:00"
      }
    ],
    "total": 1,
    "page": 1,
    "size": 10,
    "pages": 1
  },
  "message": null
}
```

#### POST /api/v1/expenses/

Membuat pengeluaran baru.

**Request Body:**

```json
{
  "amount": 42.99,
  "date": "2024-03-14",
  "description": "Makan siang",
  "category_id": 1,
  "account_id": 1,
  "tag_ids": [1, 2]
}
```

**Response:**

```json
{
  "status": "success",
  "data": {
    "id": 2,
    "amount": "42.99",
    "date": "2024-03-14",
    "description": "Makan siang",
    "category": {
      "id": 1,
      "name": "Makanan"
    },
    "account": {
      "id": 1,
      "name": "Rekening Bank"
    },
    "tags": [
      {
        "id": 1,
        "name": "Penting"
      },
      {
        "id": 2,
        "name": "Makan Siang"
      }
    ],
    "created_at": "2024-03-14T10:45:00",
    "updated_at": "2024-03-14T10:45:00"
  },
  "message": "Pengeluaran berhasil dibuat"
}
```

### Anggaran

#### GET /api/v1/budgets/

Mendapatkan semua anggaran.

**Query Parameters:**

- `skip` (opsional): Jumlah record yang dilewati (default: 0)
- `limit` (opsional): Jumlah maksimum record yang dikembalikan (default: 100)

**Response:**

```json
{
  "status": "success",
  "data": {
    "items": [
      {
        "id": 1,
        "category_id": 1,
        "year": 2024,
        "month": 3,
        "amount": "500.00",
        "category": {
          "id": 1,
          "name": "Makanan"
        },
        "created_at": "2024-03-14T11:00:00",
        "updated_at": "2024-03-14T11:00:00"
      }
    ],
    "total": 1,
    "page": 1,
    "size": 10,
    "pages": 1
  },
  "message": null
}
```

#### POST /api/v1/budgets/

Membuat anggaran baru.

**Request Body:**

```json
{
  "category_id": 2,
  "year": 2024,
  "month": 3,
  "amount": 200.0
}
```

**Response:**

```json
{
  "status": "success",
  "data": {
    "id": 2,
    "category_id": 2,
    "year": 2024,
    "month": 3,
    "amount": "200.00",
    "category": {
      "id": 2,
      "name": "Transportasi"
    },
    "created_at": "2024-03-14T11:15:00",
    "updated_at": "2024-03-14T11:15:00"
  },
  "message": "Anggaran berhasil dibuat"
}
```

### Akun

#### GET /api/v1/accounts/

Mendapatkan semua akun.

**Query Parameters:**

- `skip` (opsional): Jumlah record yang dilewati (default: 0)
- `limit` (opsional): Jumlah maksimum record yang dikembalikan (default: 100)

**Response:**

```json
{
  "status": "success",
  "data": {
    "items": [
      {
        "id": 1,
        "name": "Rekening Bank",
        "initial_balance": "1000.00",
        "created_at": "2024-03-14T11:30:00",
        "updated_at": "2024-03-14T11:30:00"
      }
    ],
    "total": 1,
    "page": 1,
    "size": 10,
    "pages": 1
  },
  "message": null
}
```

#### POST /api/v1/accounts/

Membuat akun baru.

**Request Body:**

```json
{
  "name": "Dompet",
  "initial_balance": 500.0
}
```

**Response:**

```json
{
  "status": "success",
  "data": {
    "id": 2,
    "name": "Dompet",
    "initial_balance": "500.00",
    "created_at": "2024-03-14T11:45:00",
    "updated_at": "2024-03-14T11:45:00"
  },
  "message": "Akun berhasil dibuat"
}
```

### Tag

#### GET /api/v1/tags/

Mendapatkan semua tag.

**Query Parameters:**

- `skip` (opsional): Jumlah record yang dilewati (default: 0)
- `limit` (opsional): Jumlah maksimum record yang dikembalikan (default: 100)

**Response:**

```json
{
  "status": "success",
  "data": {
    "items": [
      {
        "id": 1,
        "name": "Penting",
        "created_at": "2024-03-14T12:00:00",
        "updated_at": "2024-03-14T12:00:00"
      }
    ],
    "total": 1,
    "page": 1,
    "size": 10,
    "pages": 1
  },
  "message": null
}
```

#### POST /api/v1/tags/

Membuat tag baru.

**Request Body:**

```json
{
  "name": "Makan Siang"
}
```

**Response:**

```json
{
  "status": "success",
  "data": {
    "id": 2,
    "name": "Makan Siang",
    "created_at": "2024-03-14T12:15:00",
    "updated_at": "2024-03-14T12:15:00"
  },
  "message": "Tag berhasil dibuat"
}
```

### Pengeluaran Berulang

#### GET /api/v1/recurring/

Mendapatkan semua pengeluaran berulang.

**Query Parameters:**

- `skip` (opsional): Jumlah record yang dilewati (default: 0)
- `limit` (opsional): Jumlah maksimum record yang dikembalikan (default: 100)

**Response:**

```json
{
  "status": "success",
  "data": {
    "items": [
      {
        "id": 1,
        "name": "Sewa Bulanan",
        "amount": "800.00",
        "category_id": 3,
        "interval": "monthly",
        "next_date": "2024-04-01",
        "end_date": null,
        "category": {
          "id": 3,
          "name": "Perumahan"
        },
        "created_at": "2024-03-14T12:30:00",
        "updated_at": "2024-03-14T12:30:00"
      }
    ],
    "total": 1,
    "page": 1,
    "size": 10,
    "pages": 1
  },
  "message": null
}
```

#### POST /api/v1/recurring/

Membuat pengeluaran berulang baru.

**Request Body:**

```json
{
  "name": "Internet Bulanan",
  "amount": 59.99,
  "category_id": 3,
  "interval": "monthly",
  "next_date": "2024-04-15",
  "end_date": null
}
```

**Response:**

```json
{
  "status": "success",
  "data": {
    "id": 2,
    "name": "Internet Bulanan",
    "amount": "59.99",
    "category_id": 3,
    "interval": "monthly",
    "next_date": "2024-04-15",
    "end_date": null,
    "category": {
      "id": 3,
      "name": "Perumahan"
    },
    "created_at": "2024-03-14T12:45:00",
    "updated_at": "2024-03-14T12:45:00"
  },
  "message": "Pengeluaran berulang berhasil dibuat"
}
```

### Statistik

#### GET /api/v1/statistics/monthly

Mendapatkan statistik pengeluaran bulanan.

**Query Parameters:**

- `year` (wajib): Tahun untuk statistik
- `month` (wajib): Bulan untuk statistik (1-12)

**Response:**

```json
{
  "status": "success",
  "data": {
    "total_expenses": "1250.75",
    "average_per_day": "89.34",
    "highest_day": {
      "date": "2024-03-10",
      "amount": "250.00"
    },
    "by_category": [
      {
        "category_name": "Makanan",
        "total": "450.25",
        "percent": 36.0
      }
    ],
    "by_tag": [
      {
        "tag_name": "Penting",
        "total": "800.50",
        "percent": 64.0
      }
    ],
    "daily_totals": [
      {
        "date": "2024-03-01",
        "amount": "125.00"
      }
    ]
  },
  "message": null
}
```

## Penanganan Error

Semua response error mengikuti format standar:

```json
{
  "status": "error",
  "data": null,
  "message": "Pesan error detail"
}
```

### Kode Status HTTP Umum

- **400 Bad Request**: Data input tidak valid
- **401 Unauthorized**: Autentikasi gagal
- **403 Forbidden**: Akses ditolak
- **404 Not Found**: Resource tidak ditemukan
- **409 Conflict**: Konflik resource
- **422 Unprocessable Entity**: Error validasi
- **429 Too Many Requests**: Rate limit terlampaui
- **500 Internal Server Error**: Error server

## Rate Limiting

API menerapkan rate limiting untuk memastikan penggunaan yang adil:

- Endpoint autentikasi: 5 request per menit
- Endpoint lainnya: 60 request per menit per pengguna

Header response rate limit:

```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 59
X-RateLimit-Reset: 1710417890
```

## Keamanan

### Persyaratan Password

- Minimal 8 karakter
- Minimal 1 huruf besar
- Minimal 1 huruf kecil
- Minimal 1 angka
- Minimal 1 karakter khusus

### Rate Limiting

Batas default per alamat IP:

- Endpoint autentikasi: 5 request per menit
- Endpoint lainnya: 60 request per menit
- Burst: 5 request
