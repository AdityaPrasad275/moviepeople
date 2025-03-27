### Minimum Viable Product (MVP) Plan for "LinkedIn for Movie People"

#### Overview
We’re building a starting prototype (MVP) for a platform like "LinkedIn for movie people." This platform will let film industry professionals showcase their work and connect with others in the industry. The MVP will focus on the most important features to test the idea with users, keeping it simple and doable for a junior software developer. We’ll use a boring, well-tested tech stack to make development straightforward and reliable. The UI won’t be fancy—it’s all about getting the core functionality working.

#### Vision
The goal is to create a platform where film professionals (like directors, actors, or editors) can:
- Show off their work (like a portfolio).
- Find and connect with others in the industry.
- Test if this idea is useful to users.

After the MVP is built, we can get feedback and add more features later.

---

### Tech Stack
We’ll use a simple, boring, and well-understood tech stack that’s easy to work with:
- **Backend**: Django (Pythaon)  
  - Why? Django is a framework that does a lot for you (like user logins and database stuff) and is easy to learn. Python is readable, which helps junior developers.
- **Database**: PostgreSQL  
  - Why? It’s a solid, free database that works great with Django and can handle growth later.
- **Frontend**: Django templates with Bootstrap  
  - Why? Django templates let us build pages on the server (no fancy frontend frameworks yet), and Bootstrap makes them look decent and work on phones without much effort.

This stack is "boring" because it’s been around forever, has tons of tutorials, and won’t surprise you with weird problems.

---

### Most Important Base Features
For the MVP, we’ll focus on these core features that solve the main problems:
1. **User Authentication**  
   - Problem: Users need to sign up and log in to use the platform.  
   - What: Let users create accounts, log in, and log out.
2. **User Profiles with Portfolio**  
   - Problem: Film pros need a place to show their work.  
   - What: Each user gets a profile with their info (like role and location) and a portfolio section for projects (title, description, and media like videos or images).
3. **Networking Tools**  
   - Problem: Users want to connect with others in the industry.  
   - What:  
     - **Connections**: Send and accept connection requests (like LinkedIn friends).  
     - **Messaging**: Send simple text messages to connections.  
     - **Feed**: See updates from connections (like new projects they add).
4. **Search Functionality**  
   - Problem: Users need to find people to connect with.  
   - What: Search for users by name, role (e.g., "director"), or location.

These features cover the basics: signing up, showing work, connecting, and finding people.

---

### Problems to Solve
- **Identity**: Users need a secure way to join and access their stuff (authentication).  
- **Showcase**: They need an easy way to share their projects (profiles/portfolio).  
- **Networking**: They need tools to build relationships (connections, messaging, feed).  
- **Discovery**: They need to find the right people (search).  
- **Simplicity**: Keep it basic so a junior developer can build it and users can test it.

---

### Detailed Development Plan
Here’s how to build it, broken into parts a junior developer can follow. Each step builds on the last one.

#### 1. Set Up the Project
- **What to Do**: Get the basics ready.  
- **How**:  
  - Install Python and Django (`pip install django`).  
  - Create a new Django project (`django-admin startproject moviepeople`).  
  - Install PostgreSQL and set it up (download it, create a database called `moviepeople_db`).  
  - Update `settings.py` in Django to use PostgreSQL (add database name, user, password).  
  - Run `python manage.py migrate` to set up the database.  
- **Goal**: A working Django project connected to a database.

#### 2. User Authentication
- **What to Do**: Let users sign up and log in.  
- **How**:  
  - Use Django’s built-in auth system (it’s already there!).  
  - Create a `users` app (`python manage.py startapp users`).  
  - Add signup, login, and logout views using Django’s `LoginView`, `LogoutView`, and a simple signup form.  
  - Make basic templates (HTML files) for signup and login pages.  
- **Goal**: Users can create accounts and log in.

#### 3. User Profiles
- **What to Do**: Give users a profile page with extra info and a portfolio.  
- **How**:  
  - In the `users` app, extend Django’s User model with fields like `role` (text), `location` (text), and `bio` (text). Use a `Profile` model linked to `User`.  
  - Create a view to show the profile and another to edit it (use Django forms).  
  - Add templates for viewing and editing the profile.  
  - Test it by adding a profile for yourself.  
- **Goal**: Users can fill out and see their profiles.

#### 4. Portfolio Functionality
- **What to Do**: Let users add projects to their profile.  
- **How**:  
  - Create a `PortfolioItem` model in a new `portfolio` app (`python manage.py startapp portfolio`).  
  - Fields: `user` (link to User), `title` (text), `description` (text), `media_url` (text for video links, like YouTube).  
  - Add views to create, edit, and delete portfolio items (use Django forms).  
  - Show portfolio items on the profile page template.  
  - For simplicity, let users paste video URLs (e.g., YouTube links) instead of uploading files.  
- **Goal**: Users can add projects with titles, descriptions, and video links.

#### 5. Networking Features
- **What to Do**: Build tools for connecting and talking.  
- **How**:  
  - **Connections**:  
    - Create a `Connection` model: `user_from` (User), `user_to` (User), `status` (text: "pending" or "accepted").  
    - Add views to send a connection request and accept/reject it.  
    - Show a list of connections on the profile page.  
  - **Messaging**:  
    - Create a `Message` model: `sender` (User), `recipient` (User), `content` (text), `timestamp` (date).  
    - Add views to send a message and see a list of messages with a connection.  
    - Make a simple messaging template.  
  - **Feed**:  
    - Create an `Activity` model: `user` (User), `action` (text, e.g., "added a project"), `timestamp` (date).  
    - Add a view to show activities from a user’s connections.  
    - Make a feed template.  
- **Goal**: Users can connect, message, and see updates from each other.

#### 6. Search Functionality
- **What to Do**: Let users find others.  
- **How**:  
  - Create a search form (fields: name, role, location).  
  - Add a view to filter users using Django’s ORM (e.g., `User.objects.filter(role__contains="director")`).  
  - Make a search results template to list matching users.  
- **Goal**: Users can search and find people.

#### 7. Basic UI
- **What to Do**: Make it usable, not pretty.  
- **How**:  
  - Add Bootstrap (download it or use a CDN link in your templates).  
  - Use Bootstrap classes to style forms, buttons, and lists (e.g., profile, search results).  
  - Keep it simple: focus on function, not design.  
- **Goal**: Pages look okay and work on phones.

#### 8. Testing
- **What to Do**: Make sure it works.  
- **How**:  
  - Write simple tests in Django (e.g., test login works, test adding a portfolio item).  
  - Manually test everything: sign up, add a project, connect with yourself, send a message, search.  
  - Fix bugs you find.  
- **Goal**: The app doesn’t crash and does what it’s supposed to.

#### 9. Deployment
- **What to Do**: Put it online so others can try it.  
- **How**:  
  - Use Heroku (it’s free for small projects and easy).  
  - Follow Heroku’s Django guide: push your code with Git, set up PostgreSQL, run migrations.  
  - Test the live site.  
- **Goal**: The app is online for users to test.

---

### Additional Tips for a Junior Developer
- **Use Git**: Save your work with Git (`git init`, `git add .`, `git commit -m "message"`) so you can undo mistakes.  
- **Keep it Simple**: Don’t overthink—stick to the plan.  
- **Google Everything**: Stuck? Search “Django how to [problem]” (e.g., “Django how to add user profile”).  
- **Test as You Go**: After each step, check if it works before moving on.  
- **Ask for Help**: If you’re lost, ask a friend or post on Stack Overflow.

---

### What’s Next?
After the MVP is live:
- Get feedback from users (e.g., film students or friends in the industry).  
- Fix bugs and add small improvements.  
- Later, think about extras like video uploads, better search, or a nicer UI.

This plan gives you a clear path to build a working prototype. Start with step 1, and take it one piece at a time—you’ve got this!