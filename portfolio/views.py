from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import PortfolioItem
from .forms import PortfolioItemForm
from feed.models import Post


@login_required
def portfolio_list(request):
    items = PortfolioItem.objects.filter(user=request.user)
    return render(request, "portfolio/portfolio_list.html", {"items": items})


@login_required
def create_portfolio_item(request):
    if request.method == "POST":
        form = PortfolioItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            
            try:
                Post.objects.create(
                    user=request.user,
                    post_type='portfolio_add',
                    content=f"Added a new portfolio item: '{item.title}'"
                    # If using GenericForeignKey later, you'd link it here:
                    # content_type=ContentType.objects.get_for_model(portfolio_item),
                    # object_id=portfolio_item.pk,
                )
            except Exception as e:
                # Optional: Log error if post creation fails, but don't stop the user flow
                print(f"Error creating feed post for new portfolio item: {e}")
                
            return redirect("portfolio:portfolio_list")
    else:
        form = PortfolioItemForm()
    return render(request, "portfolio/portfolio_form.html", {"form": form})


@login_required
def edit_portfolio_item(request, pk):
    item = get_object_or_404(PortfolioItem, pk=pk, user=request.user)
    if request.method == "POST":
        form = PortfolioItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect("portfolio:portfolio_list")
    else:
        form = PortfolioItemForm(instance=item)
    return render(request, "portfolio/portfolio_form.html", {"form": form})


@login_required
def delete_portfolio_item(request, pk):
    item = get_object_or_404(PortfolioItem, pk=pk, user=request.user)
    if request.method == "POST":
        item.delete()
        return redirect("portfolio:portfolio_list")
    return render(request, "portfolio/portfolio_confirm_delete.html", {"item": item})
