# Design Decisions

This document explains the key architectural and implementation decisions made while developing the Event Booking System.

---

# 1. Multiple Seat Reservations

## Decision

A user may hold and confirm multiple seats for the same showtime, provided each seat is available.

## Rationale

Allowing multiple seat reservations reflects real-world booking scenarios where a user reserves seats for family or friends. Reservation conflicts are prevented at the seat level, allowing independent reservations for different seats without affecting consistency.

## Other Possible Approaches

- Restrict one active reservation per user per showtime.
- Limit the maximum number of seats per booking.

These rules can be introduced later as business requirements without changing the overall architecture.

---

# 2. Booking Close to Showtime

## Decision

Seat holds are allowed regardless of how close the showtime is.

## Rationale

The reservation system enforces a fixed two-minute hold duration and treats the showtime independently from the hold lifecycle. This keeps the booking flow predictable while avoiding additional scheduling rules.

## Other Possible Approaches

Many production booking systems introduce a configurable booking cutoff (for example, five to fifteen minutes before the event begins). This can be incorporated as a business rule if required.

---

# 3. Cancellation Behaviour

## Decision

Cancelling a reservation immediately releases the seat, making it available for new reservations.

## Rationale

Immediate availability maximizes seat utilization and provides the best user experience by allowing other users to reserve newly available seats without unnecessary delays.

## Other Possible Approaches

A cooldown period could be introduced to reduce abusive reservation patterns, although it would increase system complexity.

---

# 4. Hold Expiry During Confirmation

## Decision

If a hold expires before the confirmation request is processed, the confirmation request is rejected.

The API returns:

409 Conflict

with an appropriate error message indicating that the hold has expired.

## Rationale

Although the client originally viewed a valid reservation, the reservation state changed before confirmation was completed. Returning a conflict accurately communicates that the requested operation cannot be completed because the current state differs from the client's expectation.

The client may initiate a new reservation if the seat is still available.

---

# 5. Concurrency Control

## Decision

Concurrency is managed using database transactions together with row-level locking.

Implementation uses:

- transaction.atomic()
- select_for_update()

## Rationale

Seat reservation is a critical section where multiple users may attempt to reserve the same seat simultaneously.

Row-level locking guarantees that only one transaction can reserve a seat while competing transactions wait until the lock is released. This eliminates race conditions and prevents duplicate reservations.

---

# 6. Hold Expiry Strategy

## Decision

The system follows a lazy expiry strategy.

Whenever a reservation is accessed for holding, confirmation, or seat availability, the hold expiry is evaluated. Expired reservations are automatically released during normal request processing.

## Rationale

Lazy expiry avoids background infrastructure while ensuring expired holds do not permanently block seats.

## Other Possible Approaches

- Scheduled cleanup jobs
- Celery workers
- Database TTL mechanisms

These approaches are more suitable for large-scale deployments.

---

# 7. Idempotent Confirmation

## Decision

The Confirm Reservation endpoint is idempotent.

Repeated confirmation requests for an already confirmed reservation return the existing reservation rather than creating duplicate bookings.

## Rationale

Clients commonly retry requests after network interruptions or request timeouts.

Idempotent behaviour guarantees a consistent outcome regardless of how many times the confirmation request is submitted.

---

# 8. Error Handling

## Decision

Business failures return meaningful error responses rather than generic server errors.

Examples include:

- Seat already reserved
- Hold expired
- Reservation belongs to another user
- Reservation already cancelled
- Reservation not found

## Rationale

Clear error messages improve API usability and allow client applications to respond appropriately.

---

# 9. Data Integrity Under Concurrent Load

## Decision

A concurrent booking test is included with the project.

The test launches ten simultaneous reservation requests for the same seat.

## Expected Behaviour

- Exactly one reservation succeeds.
- Remaining requests receive conflict responses.

## Rationale

This validates that the concurrency strategy prevents duplicate reservations under simultaneous access.

---

# 10. Application Architecture

## Decision

The application follows a layered architecture consisting of:

- Models
- Serializers
- Services
- Views

## Rationale

Business logic is isolated within the service layer while the API layer remains responsible only for request validation and response generation.

This separation improves maintainability, readability, testing, and future extensibility.

