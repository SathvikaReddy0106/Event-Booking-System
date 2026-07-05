# Architecture & Design Decisions

This document summarizes the key architectural and implementation decisions made during the development of the Event Booking System.

---

# 1. Multiple Seat Reservations

## Decision

A user may hold and confirm multiple seats for the same showtime, provided each seat is available.

## Reasoning

Allowing multiple seat reservations reflects common booking scenarios where users reserve seats for family or friends. Since reservation conflicts are handled at the seat level, multiple reservations by the same user do not affect system consistency.

## Alternatives Considered

- Restrict one active reservation per user per showtime.
- Limit the maximum number of seats per booking.

These rules can be introduced later as business requirements without changing the overall architecture.

---

# 2. Booking Close to Showtime

## Decision

Seat holds are allowed regardless of how close the showtime is.

## Reasoning

The reservation system enforces a fixed two-minute hold duration while keeping the booking process independent of the event start time. This keeps the implementation simple and predictable.

## Alternatives Considered

Introduce a configurable booking cutoff (for example, five to fifteen minutes before the event starts) to prevent late reservations.

---

# 3. Cancellation Behaviour

## Decision

Cancelling a reservation immediately releases the seat, making it available for new reservations.

## Reasoning

Immediate availability improves seat utilization and allows other users to reserve the seat without unnecessary delays.

## Alternatives Considered

Introduce a cooldown period before making the seat available again. This could reduce abuse but would increase implementation complexity.

---

# 4. Hold Expiry During Confirmation

## Decision

If a hold expires before the confirmation request is processed, the request is rejected.

The API returns **409 Conflict** with an appropriate error message.

## Reasoning

Although the client originally viewed a valid hold, the reservation state changed before confirmation was completed. Returning a conflict accurately communicates that the request can no longer be completed because the resource state has changed.

If the seat is still available, the client can create a new reservation.

---

# 5. Concurrency Control

## Decision

Concurrency is managed using database transactions together with row-level locking.

Implementation uses:

- `transaction.atomic()`
- `select_for_update()`

## Reasoning

Seat reservation is a critical operation where multiple users may attempt to reserve the same seat simultaneously.

Row-level locking ensures that only one transaction can reserve a seat while competing transactions wait until the lock is released. This prevents race conditions and guarantees that duplicate reservations cannot occur.

---

# 6. Hold Expiry Strategy

## Decision

The system uses a lazy expiry strategy.

Whenever a reservation is accessed during seat holding, confirmation, or seat availability checks, the hold expiry is evaluated. Expired holds are automatically released during normal request processing.

## Reasoning

This approach keeps the implementation simple while ensuring expired reservations do not permanently block seats. It also avoids introducing additional background infrastructure.

## Alternatives Considered

- Scheduled cleanup jobs
- Celery workers
- Database TTL mechanisms

These approaches are more suitable for larger distributed deployments.

---

# 7. Idempotent Confirmation

## Decision

The Confirm Reservation endpoint is idempotent.

If a reservation has already been confirmed, repeated confirmation requests return the existing reservation instead of creating duplicate bookings.

## Reasoning

Clients may retry requests after temporary network failures or timeouts. Returning the existing reservation guarantees a consistent result regardless of how many times the confirmation request is submitted.

---

# 8. Error Handling

## Decision

The API returns clear and meaningful responses for common business failures.

Examples include:

- Seat already held or booked
- Hold expired
- Reservation belongs to another user
- Reservation already cancelled
- Reservation does not exist

## Reasoning

Meaningful error responses make the API easier to consume and allow client applications to handle different failure scenarios appropriately.

---

# 9. Data Integrity Under Concurrent Load

## Decision

A concurrency test script is included to simulate ten simultaneous reservation requests for the same seat.

## Expected Outcome

- Exactly one reservation succeeds.
- All remaining requests receive conflict responses.

## Reasoning

This verifies that the concurrency strategy works correctly under simultaneous access and prevents double booking.

---

# 10. Application Architecture

## Decision

The application follows a layered architecture consisting of:

- Models
- Serializers
- Services
- Views

## Reasoning

Separating business logic from request handling improves readability, maintainability, and testability. The service layer contains the reservation logic, while the API layer focuses on request validation and response generation.
