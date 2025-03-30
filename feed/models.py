# feed/models.py
from django.db import models
from django.contrib.auth.models import User  # Or your custom user model

# Optional: Import PortfolioItem if you want a direct link later
# from portfolio.models import PortfolioItem


class Post(models.Model):
    POST_TYPE_CHOICES = [
        ("user_post", "User Post"),  # Manually created by user
        ("portfolio_add", "Portfolio Add"),  # Auto-created when portfolio item added
        # Add more types later? ('new_connection', 'job_alert', etc.)
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts"
    )  # The author or subject user
    post_type = models.CharField(
        max_length=20, choices=POST_TYPE_CHOICES, default="user_post"
    )
    content = models.TextField(
        blank=False, null=False
    )  # The main text content (user-written or system-generated)
    timestamp = models.DateTimeField(auto_now_add=True)

    # Optional: Link to related object (More advanced, skip for initial MVP if complex)
    # Using GenericForeignKey allows linking to different models (PortfolioItem, JobPost etc.)
    # from django.contrib.contenttypes.fields import GenericForeignKey
    # from django.contrib.contenttypes.models import ContentType
    # content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    # object_id = models.PositiveIntegerField(null=True, blank=True)
    # related_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ["-timestamp"]  # Show newest posts first

    def __str__(self):
        return f"{self.user.username} ({self.get_post_type_display()}) @ {self.timestamp:%Y-%m-%d %H:%M}"

class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments"
    )  # Link to the parent Post
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )  # Who wrote the comment
    content = models.TextField(blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["timestamp"]  # Show oldest comments first within a post

    def __str__(self):
        return f"Comment by {self.user.username} on post {self.post.id} @ {self.timestamp:%Y-%m-%d %H:%M}"
