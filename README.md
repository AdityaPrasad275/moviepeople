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


