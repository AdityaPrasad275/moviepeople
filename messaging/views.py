# messaging/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.db.models import Q  # Needed for complex lookups

# --- IMPORTANT: Import your Connection model ---
# Adjust the import path based on where your Connection model lives
# Example if it's in a 'connections' app:
from connections.models import Connection

# Example if it's in the 'users' app:
# from users.models import Connection

from .models import Message

# messaging/views.py
# ... (keep existing imports and send_message view)


@login_required
def conversation_view(request, username):  # Takes username from URL
    try:
        other_user = User.objects.get(username=username)
    except User.DoesNotExist:
        # Handle error: User not found (maybe redirect to connections or 404)
        # raise Http404("User not found") # A standard way to handle this
        return redirect("list_connections")  # Or redirect as before

    # Get the logged-in user
    user = request.user

    # --- SECURITY CHECK: Verify users are connected ---
    # (Same check as in send_message)
    are_connected = Connection.objects.filter(
        (
            Q(requester=user, receiver=other_user)
            | Q(requester=other_user, receiver=user)
        )
        & Q(status="accepted")
    ).exists()

    if (
        not are_connected and user != other_user
    ):  # Allow viewing empty page if not connected? Or deny? Let's deny for MVP.
        # Handle error: Not connected
        # You could show a message "Connect with this user to send messages"
        return redirect(
            "profile_view", username=other_user.username
        )  # Redirect to their profile

    # Fetch messages between the two users
    messages = Message.objects.filter(
        (Q(sender=user, recipient=other_user) | Q(sender=other_user, recipient=user))
    ).order_by(
        "timestamp"
    )  # Ensure chronological order

    context = {
        "other_user": other_user,
        "messages": messages,
    }
    return render(request, "messaging/conversation.html", context)


@login_required  # Ensures only logged-in users can send messages
@require_POST  # Ensures this view only accepts POST requests (form submissions)
def send_message(request):
    recipient_id = request.POST.get("recipient_id")
    content = request.POST.get("content")

    if not recipient_id or not content:
        # Handle error: Missing data (maybe add Django messages framework later)
        # For MVP, we might just redirect back or show a simple error
        # We need the recipient's username to redirect back to the conversation
        # This is a bit tricky here, maybe redirect to connections list for now on error?
        return redirect("list_connections")  # Redirect somewhere sensible on error

    # Get the recipient user object
    try:
        recipient = User.objects.get(id=recipient_id)
    except User.DoesNotExist:
        # Handle error: Recipient not found
        return redirect("list_connections")  # Or another error page

    sender = request.user

    # --- SECURITY CHECK: Verify users are connected ---
    are_connected = Connection.objects.filter(
        (
            Q(requester=sender, receiver=recipient)
            | Q(requester=recipient, receiver=sender)
        )
        & Q(status="accepted")
    ).exists()

    if not are_connected:
        # Handle error: Users are not connected, cannot send message
        # Maybe flash a message: "You can only message your connections."
        # For MVP, redirect back to the profile or conversation page
        # Redirecting back to the conversation requires the username
        # We can get it from the recipient object we fetched
        return redirect("conversation", username=recipient.username)  # Redirect back

    # If all checks pass, create and save the message
    if sender != recipient:  # Prevent sending messages to oneself (optional)
        Message.objects.create(sender=sender, recipient=recipient, content=content)

    # Redirect back to the conversation page with the recipient
    # The 'conversation' name is what we'll define in urls.py for conversation_view
    return redirect("messaging:conversation", username=recipient.username)
