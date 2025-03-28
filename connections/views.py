# connections/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q  # Required for complex lookups (OR conditions)
from .models import Connection
from django.urls import reverse  # To generate URLs dynamically


@login_required  # Ensures only logged-in users can access this view
def send_request(request, user_id):
    """
    View to send a connection request to another user.
    Handles POST request implicitly by being linked from a button/link.
    """
    receiver = get_object_or_404(User, id=user_id)
    requester = request.user

    # Prevent sending request to self
    if receiver == requester:
        messages.error(request, "You cannot send a connection request to yourself.")
        # Redirect back to the user's own profile or a relevant page
        return redirect(
            reverse("users:profile")
        )  # Assuming 'users:profile' is the view for the logged-in user's profile

    # Check if a connection or pending request already exists (in either direction)
    existing_connection = Connection.objects.filter(
        (Q(requester=requester, receiver=receiver))
        | (Q(requester=receiver, receiver=requester))
    ).first()  # .first() gets the object if it exists, or None

    if existing_connection:
        if existing_connection.status == Connection.STATUS_PENDING:
            if existing_connection.requester == requester:
                messages.warning(
                    request,
                    f"You already sent a pending request to {receiver.username}.",
                )
            else:
                messages.info(
                    request,
                    f"{receiver.username} has already sent you a pending request. Check your requests.",
                )
        elif existing_connection.status == Connection.STATUS_ACCEPTED:
            messages.info(
                request, f"You are already connected with {receiver.username}."
            )
        elif existing_connection.status == Connection.STATUS_REJECTED:
            # Decide if users can re-request after rejection. Let's allow it for now by creating a new one.
            # If you don't want to allow re-request, add a specific message here.
            # For now, we proceed to create a new request below if the status was rejected.
            pass  # Allow creating a new request if the old one was rejected

    # Only create if no *active* (pending/accepted) connection exists.
    # We rely on the UniqueConstraint to prevent duplicate *pending* requests if the rejected logic is skipped.
    # A more robust way for re-requesting might involve updating the 'rejected' status back to 'pending'.
    # Let's keep it simple: Create if no pending/accepted exists.
    # The UniqueConstraint will prevent duplicates if we try creating again without the rejected check above.

    can_create = (
        not existing_connection
        or existing_connection.status == Connection.STATUS_REJECTED
    )

    if can_create:
        try:
            # If a rejected request exists, maybe update it instead of creating new?
            # For simplicity, let's just try creating. The constraint handles duplicates.
            # If you want to re-activate a rejected request:
            # rejected_request = Connection.objects.filter(requester=requester, receiver=receiver, status=Connection.STATUS_REJECTED).first()
            # if rejected_request:
            #    rejected_request.status = Connection.STATUS_PENDING
            #    rejected_request.save()
            #    messages.success(request, f"Connection request sent again to {receiver.username}.")
            # else:
            #    Connection.objects.create(requester=requester, receiver=receiver)
            #    messages.success(request, f"Connection request sent to {receiver.username}.")

            # Simplest approach relying on constraint:
            Connection.objects.create(requester=requester, receiver=receiver)
            messages.success(
                request, f"Connection request sent to {receiver.username}."
            )

        except Exception as e:
            # This might catch the UniqueConstraint violation if the logic above failed
            messages.error(
                request, f"Could not send request. It might already exist. Error: {e}"
            )
    # If no new request was created because one already exists and isn't rejected:
    elif not existing_connection.status == Connection.STATUS_REJECTED:
        # Messages for existing pending/accepted requests were shown above
        pass

    # Redirect back to the profile of the user the request was sent to
    return redirect(
        reverse("users:user_profile", kwargs={"username": receiver.username})
    )

# connections/views.py
# ... (keep existing imports) ...
from django.core.exceptions import PermissionDenied


@login_required
def manage_request(request, connection_id, action):
    """
    View for the receiver to accept or reject a pending connection request.
    'action' should be 'accept' or 'reject'.
    """
    connection = get_object_or_404(Connection, id=connection_id)
    user = request.user

    # Security Check: Ensure the logged-in user is the receiver of this request
    if connection.receiver != user:
        # raise PermissionDenied("You do not have permission to manage this request.")
        # Or show a less technical error message:
        messages.error(request, "You cannot manage this connection request.")
        # Redirect to a safe page, like their own profile or dashboard
        return redirect(reverse("users:profile"))  # Or your main dashboard URL

    # Check if the request is actually pending
    if connection.status != Connection.STATUS_PENDING:
        messages.warning(request, "This request is no longer pending.")
        # Redirect back to the requester's profile or a requests list
        return redirect(
            reverse(
                "users:user_profile", kwargs={"username": connection.requester.username}
            )
        )

    if action == "accept":
        connection.status = Connection.STATUS_ACCEPTED
        connection.save()
        messages.success(
            request, f"You are now connected with {connection.requester.username}."
        )
        # Optional: Create a notification for the requester
    elif action == "reject":
        connection.status = Connection.STATUS_REJECTED
        connection.save()
        # OR: delete the request entirely?
        # connection.delete()
        messages.info(
            request,
            f"Connection request from {connection.requester.username} rejected.",
        )
        # Optional: Create a notification for the requester
    else:
        messages.error(request, "Invalid action.")

    # Redirect back to the profile of the user who sent the request
    # Or redirect to a page showing pending requests (we'll build this later)
    return redirect(
        reverse(
            "users:user_profile", kwargs={"username": connection.requester.username}
        )
    )


@login_required
def list_connections(request):
    """
    View to display a list of users the logged-in user is connected with.
    """
    user = request.user
    # Find all Connection objects where the status is 'accepted'
    # and the current user is either the requester or the receiver.
    accepted_connections = Connection.objects.filter(
        (Q(requester=user) | Q(receiver=user)), status=Connection.STATUS_ACCEPTED
    )

    # Extract the actual User objects they are connected *to*.
    connected_users = []
    for connection in accepted_connections:
        if connection.requester == user:
            connected_users.append(connection.receiver)
        else:
            connected_users.append(connection.requester)

    # Sort the list alphabetically by username for consistency
    connected_users.sort(key=lambda x: x.username.lower())

    context = {
        "connected_users": connected_users,
    }
    return render(request, "connections/list_connections.html", context)


@login_required
def list_pending_requests(request):
    """
    View to display incoming connection requests that are pending for the logged-in user.
    """
    user = request.user
    # Find all Connection objects where the logged-in user is the receiver
    # and the status is 'pending'.
    pending_requests = Connection.objects.filter(
        receiver=user, status=Connection.STATUS_PENDING
    ).select_related(
        "requester", "requester__profile"
    )  # Optimize query

    context = {
        "pending_requests": pending_requests,
    }
    return render(request, "connections/list_pending_requests.html", context)
