# messaging/models.py
from django.db import models
from django.contrib.auth.models import User  # Or your custom user model if you have one


class Message(models.Model):
    sender = models.ForeignKey(
        User, related_name="sent_messages", on_delete=models.CASCADE
    )
    recipient = models.ForeignKey(
        User, related_name="received_messages", on_delete=models.CASCADE
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    # is_read = models.BooleanField(default=False) # Optional for MVP, useful later

    def __str__(self):
        return f"From {self.sender.username} to {self.recipient.username} at {self.timestamp:%Y-%m-%d %H:%M}"

    class Meta:
        ordering = ["timestamp"]  # Default order when fetching messages
