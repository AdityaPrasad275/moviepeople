# feed/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import (
    reverse_lazy,
)  # Use reverse_lazy for class-based views or success_urls

from .models import Post, Comment  # Import models
from .forms import PostForm  # Import form

# Import Connection model (adjust path as needed)
from connections.models import Connection
from django.db.models import Q
from django.contrib.auth.models import User


@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(
                commit=False
            )  # Create Post object but don't save to DB yet
            post.user = request.user  # Set the author to the logged-in user
            post.post_type = (
                "user_post"  # Explicitly set type (though it's the default)
            )
            post.save()  # Now save the Post to the database
            return redirect(
                "feed:feed_view"
            )  # Redirect to the main feed page after posting
    else:  # If request.method is GET
        form = PostForm()  # Create an empty form

    # Render the same template for GET (show form) and POST (show form with errors if invalid)
    return render(request, "feed/create_post.html", {"form": form})


@login_required
def feed_view(request):
    user = request.user

    # 1. Get IDs of users the current user is connected to
    connection_queryset = Connection.objects.filter(status="accepted").filter(
        Q(requester=user) | Q(receiver=user)
    )
    connected_user_ids = set([user.id])  # Start with the current user's ID
    for conn in connection_queryset:
        if conn.requester == user:
            connected_user_ids.add(conn.receiver.id)
        else:
            connected_user_ids.add(conn.requester.id)

    # 2. Fetch posts from the user and their connections
    #    Order is handled by the Post model's Meta class ('-timestamp')
    posts = Post.objects.filter(
        user_id__in=connected_user_ids
    )  # Efficiently filter by user IDs

    # 3. Optional: Include the Post creation form directly on the feed page
    post_form = PostForm()

    # 4. Handle creation form submission IF submitted from this page
    #    (Alternative to dedicated create_post page, choose one or both)
    if request.method == "POST":
        # Check if this POST is for creating a post (e.g., add a name attribute to submit button)
        # For simplicity, let's assume any POST here is for creating a post *if* using the embedded form
        submitted_form = PostForm(request.POST)
        if submitted_form.is_valid():
            new_post = submitted_form.save(commit=False)
            new_post.user = request.user
            new_post.post_type = "user_post"
            new_post.save()
            return redirect("feed:feed_view")  # Redirect to refresh the feed
        else:
            # If form submitted here is invalid, pass it back to template to show errors
            post_form = submitted_form  # Use the invalid form with errors

    context = {
        "posts": posts,
        "post_form": post_form,  # Include the form for creating posts
    }
    return render(request, "feed/feed.html", context)

from .forms import CommentForm  # Import CommentForm


@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = (
        post.comments.all()
    )  # Get comments using related_name, ordered by model Meta

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post  # Link comment to the current post
            new_comment.user = request.user  # Set comment author
            new_comment.save()
            # Redirect back to the same post detail page to see the new comment
            return redirect("feed:post_detail", post_id=post.id)
    else:  # GET request
        comment_form = CommentForm()  # Create empty form

    context = {
        "post": post,
        "comments": comments,
        "comment_form": comment_form,
    }
    return render(request, "feed/post_detail.html", context)


# --- Add View for Adding Comments (Alternative - handled within post_detail now) ---
# We merged comment adding into post_detail view for simplicity.
# A separate add_comment view is possible but adds complexity for MVP.
