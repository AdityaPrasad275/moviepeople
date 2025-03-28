# connections/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone  # Import timezone


class Connection(models.Model):
    """
    Represents a connection request or an established connection
    between two users.
    """

    STATUS_PENDING = "pending"
    STATUS_ACCEPTED = "accepted"
    STATUS_REJECTED = "rejected"
    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_ACCEPTED, "Accepted"),
        (STATUS_REJECTED, "Rejected"),
    ]

    # Who sent the request?
    # related_name helps us query from the User model later,
    # e.g., user.sent_requests.all()
    requester = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_requests"
    )

    # Who received the request?
    # e.g., user.received_requests.all()
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="received_requests"
    )

    # What is the status of this connection?
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING
    )

    # When was the request created/connection established?
    created_at = models.DateTimeField(default=timezone.now)  # Use timezone.now

    # Optional: When was the status last updated?
    # updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Ensures that a user cannot send multiple pending requests
        # to the same other user.
        constraints = [
            models.UniqueConstraint(
                fields=["requester", "receiver"], name="unique_connection_request"
            )
        ]
        ordering = ["-created_at"]  # Default order when fetching connections

    def __str__(self):
        return f"{self.requester.username} -> {self.receiver.username} ({self.get_status_display()})"
