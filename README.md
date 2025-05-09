the whole plan is in plan.md

## STEP 1
- set up django and postgresql. made a 'moviepeople_db' named database in postgres. updated settings.py with database configuration to use postgresql. ran `python manage.py migrate` to set up the database. 
- the whole `migrate` command worked so ig its set up correctly.

## STEP 2
- used django's built-in auth system to let users sign up and log in. created a `users` app.
- added signup, login, and logout views using Django's `LoginView`, `LogoutView`, and a simple signup form.
- made basic templates for signup and login pages.


## STEP 3
- gave users a profile page with extra info and a portfolio.
- extended Django's User model with fields like `role` (text), `location` (text), and `bio` (text). Used a `Profile` model linked to `User`.
- created a view to show the profile and another to edit it (used Django forms).
- added templates for viewing and editing the profile.
- tested it by adding a profile for myself.

Error log:
- i forgot to do `python manage.py makemigrations` before `migrate` so the profile model was not created in the database. 
- the user with usernme adi and password aditya275 doesnt have a profile lmao. because it was registered before step 3
<details>
<summary> users with no profile fix</summary>
first open up shell 

```python
python manage.py shell
```
then run this code
```python
from django.contrib.auth.models import User
from users.models import Profile

# Get all users
users = User.objects.all()

# Create profiles for users who don't have one
for user in users:
    try:
        # Check if profile exists
        profile = user.profile
        print(f"Profile for {user.username} already exists")
    except Profile.DoesNotExist:
        # Create profile if it doesn't exist
        Profile.objects.create(user=user)
        print(f"Created profile for {user.username}")
```

</details>

## STEP 4
- let users add projects to their profile.
- created a `PortfolioItem` model in a new `portfolio` app.
- added views to create, edit, and delete portfolio items (used Django forms).
- showed portfolio items on the profile page template.

## Step 5: Searching for a user
- created a search form (fields: username, role, location).
- url to the other user to see their profile

Error log:
- when going to difffernt guy's profile, it was showing that user's name in the navbar instead of the logged in user's name. this was beacuse in base.html i was using `{{ user.username }}` and same in profile too. django  autopopoulates user keyword to whatever idk. so i changed in profile.html to profile_user which was being passed by profile_view instead of being autopopulated by django.

## Step 6: Networking (Connections and messaging)
6.1 added connections to db
6.2 added view to request connections
6.3 added view to see pending requests and connections
6.4 Added messaging system
6.5 added view to send messages and see messages

## Step 7: Feed (Posts, comments and activity)
- added a post and comment model to db
- added a view to create posts and feed view tro see posts from people you are connected to.
- added a view to create comments and see comments on posts.

