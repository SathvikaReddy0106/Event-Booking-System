# Event Booking System

## Overview

The Event Booking System is a RESTful backend application built using Django REST Framework and MySQL. It allows users to temporarily hold seats, confirm reservations, cancel reservations, and view seat availability for a showtime.

The system is designed to maintain data integrity under concurrent access by preventing double booking while allowing independent seat reservations to proceed simultaneously.

---

# Technology Stack

- Python 3.14
- Django 5
- Django REST Framework
- MySQL

---

# Project Structure

```text
EventBookingSystem/
│
├── backend/
├── reservations/
├── seats/
├── showtimes/
├── venues/
├── scripts/
│   ├── concurrent_booking_test.py
│   └── simultaneous_booking_test.py
│
├── requirements.txt
├── README.md
├── DECISIONS.md
├── .env.example
└── manage.py
```

---

# Installation

## 1. Clone the repository

```bash
git clone <repository-url>
cd EventBookingSystem
```

---

## 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it

**Windows**

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

Copy `.env.example` to `.env` and update the database configuration.


## 5. Apply Database Migrations

```bash
python manage.py migrate
```

---

## 6. Run the Application

```bash
python manage.py runserver
```

The application will be available at

```
http://127.0.0.1:8000/
```

---

# API Documentation

## Hold Seat

Creates a temporary seat hold that remains valid for **2 minutes** unless it is confirmed or expires.

**Endpoint**

```
POST /api/seat/hold/
```

**Request**

```json
{
    "user_id": 1,
    "showtime_id": 1,
    "seat_id": 1
}
```

**Success Response (201 Created)**

```json
{
    "reservation_id": 1,
    "status": "HELD",
    "hold_expiry": "2026-07-05T11:47:45Z"
}
```

---

## Confirm Reservation

Confirms an active held reservation and converts it into a booked reservation.

**Endpoint**

```
POST /api/booking/confirm/
```

**Request**

```json
{
    "user_id": 1,
    "reservation_id": 1
}
```

**Success Response (200 OK)**

```json
{
    "reservation_id": 1,
    "status": "BOOKED"
}
```

---

## Cancel Reservation

Cancels an existing reservation and immediately releases the seat for future bookings.

**Endpoint**

```
DELETE /api/booking/cancel/
```

**Request**

```json
{
    "user_id": 1,
    "reservation_id": 1
}
```

**Success Response (200 OK)**

```json
{
    "reservation_id": 1,
    "status": "CANCELLED"
}
```

---

## Seat Availability

Returns the current status of every seat for a showtime.

**Endpoint**

```
GET /api/showtimes/{showtime_id}/seats/
```

---

## Booking Summary

Returns the booking statistics for a showtime.

**Endpoint**

```
GET /api/showtimes/{showtime_id}/summary/
```

---

# Concurrency Handling

The application prevents double booking using:

- `transaction.atomic()`
- `select_for_update()`
- Database-level unique constraint on `(seat, showtime)`

Each reservation request executes inside a database transaction. The requested seat is locked using row-level locking (`select_for_update()`), ensuring that only one transaction can reserve a particular seat at a time.

Requests for different seats proceed independently because only the requested seat row is locked, allowing high concurrency while maintaining data integrity.

---

# Hold Expiry Strategy

The system uses a **lazy expiry** strategy.

Whenever a reservation is accessed during seat holding, confirmation, or seat availability checks, the hold expiry is evaluated. Expired reservations are automatically released during normal request processing without requiring manual cleanup.

For larger deployments, this strategy can be replaced with a scheduled background cleanup using Celery and Redis.

---

# Idempotency

The **Confirm Reservation** endpoint is idempotent.

If a client retries a confirmation request due to a timeout or network interruption, the system returns the existing confirmed reservation instead of creating a duplicate booking.

---

# Error Handling

The API returns meaningful responses for common business failures.

| Scenario | Response |
|----------|----------|
| Seat already held or booked | 409 Conflict |
| Hold expired | 409 Conflict |
| Reservation belongs to another user | 409 Conflict |
| Reservation already cancelled | 409 Conflict |
| Reservation does not exist | 409 Conflict |

---

# Concurrency Validation

Two scripts are included to validate concurrent behaviour.

## 1. concurrent_booking_test.py

Simulates multiple users attempting to reserve the **same seat** simultaneously.

Expected outcome:

- Exactly one reservation succeeds.
- Remaining requests receive conflict responses.

This demonstrates that duplicate reservations cannot occur.

---

## 2. simultaneous_booking_test.py

Simulates multiple users reserving **different seats** simultaneously.

Expected outcome:

- All reservation requests succeed.

This demonstrates that row-level locking allows independent reservations to proceed concurrently without blocking one another.

---

# Testing

Business logic has been verified through service-level testing, while API behaviour has been validated using Postman.

Concurrency behaviour is demonstrated using the scripts available in the `scripts/` directory.

---

# AI Usage

ChatGPT was used as a learning and documentation aid to discuss architectural approaches, clarify Django concepts, review implementation decisions, and improve project documentation.

All implementation, integration, debugging, and validation were performed manually.

---

# Future Enhancements

- JWT-based authentication and authorization.
- Celery with Redis for scheduled cleanup of expired reservations.
- Docker and Docker Compose for deployment.
- OpenAPI (Swagger) documentation.
