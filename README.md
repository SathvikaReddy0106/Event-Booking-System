# Event Booking System

## Overview

The Event Booking System is a RESTful backend application built using Django REST Framework and MySQL. It allows users to temporarily hold seats, confirm reservations, cancel reservations, and view seat availability for a showtime.

The primary objective of this project is to demonstrate safe concurrent seat reservation while preventing double booking using database transactions and row-level locking.

---

# Technology Stack

- Python 3.14
- Django 5
- Django REST Framework
- MySQL
- VS Code

---

# Project Structure

```
EventBookingSystem/
│
├── backend/
├── reservations/
├── seats/
├── showtimes/
├── venues/
├── users/
├── scripts/
│   └── concurrent_booking_test.py
│
├── requirements.txt
├── README.md
├── DECISIONS.md
├── .env.example
├── manage.py
└── venv/
```

---

# Installation

## 1. Clone the repository

```bash
git clone <repository-url>
```

---

## 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it

Windows

```bash
venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create a `.env` file using `.env.example`.


## 5. Apply Migrations

```bash
python manage.py migrate
```

---

## 6. Run the Server

```bash
python manage.py runserver
```

The application will be available at

```
http://127.0.0.1:8000/
```

---

# API Documentation

## 1. Hold Seat

Creates a temporary reservation valid for **2 minutes**.

### Endpoint

```
POST /api/hold/
```

### Request

```json
{
    "user_id": 1,
    "showtime_id": 1,
    "seat_id": 1
}
```

### Success Response

**201 Created**

```json
{
    "reservation_id": 1,
    "status": "HELD",
    "hold_expiry": "2026-07-05T11:47:45Z"
}
```

### Possible Errors

| Status | Reason |
|---------|--------|
| 409 Conflict | Seat already held or booked |
| 409 Conflict | Hold has expired |
| 500 Internal Server Error | Unexpected server error |

---

## 2. Confirm Reservation

Confirms an existing held reservation.

### Endpoint

```
POST /api/confirm/
```

### Request

```json
{
    "user_id": 1,
    "reservation_id": 1
}
```

### Success Response

**200 OK**

```json
{
    "reservation_id": 1,
    "status": "BOOKED"
}
```

### Possible Errors

| Status | Reason |
|---------|--------|
| 409 Conflict | Hold expired |
| 409 Conflict | Reservation belongs to another user |
| 409 Conflict | Reservation already cancelled |

---

## 3. Cancel Reservation

Cancels an existing reservation.

### Endpoint

```
DELETE /api/cancel/
```

### Request

```json
{
    "user_id": 1,
    "reservation_id": 1
}
```

### Success Response

**200 OK**

```json
{
    "reservation_id": 1,
    "status": "CANCELLED"
}
```

---

## 4. Seat Availability

Returns the current status of every seat for a showtime.

### Endpoint

```
GET /api/showtimes/{showtime_id}/seats/
```

### Success Response

```json
[
    {
        "seat_id": 1,
        "row": "A",
        "seat_number": 1,
        "status": "AVAILABLE"
    }
]
```

---

## 5. Booking Summary

Returns the booking statistics for a showtime.

### Endpoint

```
GET /api/showtimes/{showtime_id}/summary/
```

### Success Response

```json
{
    "total_seats": 100,
    "booked": 45,
    "held": 10,
    "available": 45
}
```

---

# Concurrency Handling

The application prevents double booking by using:

- `transaction.atomic()`
- `select_for_update()`

When multiple users attempt to reserve the same seat simultaneously, the requested seat row is locked within a database transaction. Only one transaction can successfully create a reservation, while competing transactions receive a conflict response.

---

# Hold Expiry Strategy

A **lazy expiry** strategy is used.

Every hold, confirmation, and seat listing checks whether the hold has expired. If the hold has expired, it is released automatically without requiring manual cleanup.

This approach satisfies the assignment requirements while keeping the implementation simple. In a production environment, a background scheduler such as Celery could be used for periodic cleanup.

---

# Idempotency

The Confirm Reservation API is designed to be idempotent.

If a client retries the same confirmation request after a timeout, the system does not create duplicate bookings. If the reservation has already been confirmed, the existing reservation is returned.

---

# Error Handling

The application returns meaningful responses for common failure scenarios, including:

- Seat already held or booked
- Hold expired
- Reservation belongs to another user
- Reservation already cancelled
- Reservation does not exist

---

# Concurrency Test

The project includes:

```
scripts/concurrent_booking_test.py
```

The script sends **10 concurrent hold requests** for the same seat.

Expected Result:

- Exactly **one** request succeeds.
- Remaining requests receive a conflict response.

This demonstrates that the application correctly prevents double booking under concurrent access.

---

# AI Usage

ChatGPT was used to discuss the project architecture, understand Django concepts, review the implementation, and improve the project documentation.


---

# Future Improvements

- JWT-based authentication and authorization.
- Celery with Redis for scheduled cleanup of expired reservations.
- Docker support for simplified deployment.
- OpenAPI (Swagger) documentation.
- Comprehensive automated testing.
