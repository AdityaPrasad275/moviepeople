from django.db import models
from django.contrib.auth.models import User


# Under the hood, this creates a database table with columns for each field.
# The ForeignKey establishes a many-to-one relationship between portfolio items and users - each user can have multiple portfolio items, but each item belongs to only one user.

class PortfolioItem(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="portfolio_items"
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    media_url = models.URLField(help_text="Enter a YouTube or Vimeo URL")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
