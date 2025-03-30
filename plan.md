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

#### 5. Search Functionality
- **What to Do**: Let users find others.  
- **How**:  
  - Create a search form (fields: name, role, location).  
  - Add a view to filter users using Django’s ORM (e.g., `User.objects.filter(role__contains="director")`).  
  - Make a search results template to list matching users.  
- **Goal**: Users can search and find people.

Okay, you're right. Step 6 in the original plan is quite dense and covers three distinct major features: Connections, Messaging, and a Feed. Let's break that down into more manageable, sequential steps suitable for incremental development.

Here's a refined breakdown of the original Step 6, focusing on delivering one piece of core networking functionality at a time:

**Revised Step 6: Networking Features (Broken Down)**

**Step 6.1: Connection Model & Request/Accept Logic**

*   **Goal:** Establish the backend foundation for connections. Allow users to send, accept, or reject connection requests.
*   **Tasks:**
    1.  **Create `Connection` Model:**
        *   Define a new model named `Connection` (likely in a new `connections` app or within the `users` app).
        *   Fields:
            *   `requester`: ForeignKey to `User` (the person sending the request).
            *   `receiver`: ForeignKey to `User` (the person receiving the request).
            *   `status`: CharField with choices like 'pending', 'accepted', 'rejected'. (Default: 'pending').
            *   `created_at`: DateTimeField (auto_now_add=True).
        *   Add constraints (e.g., `UniqueConstraint`) to prevent duplicate pending requests between the same two users.
    2.  **Create Migrations:** Run `makemigrations` and `migrate`.
    3.  **Implement `send_request` View:**
        *   Create a view that takes a target `user_id`.
        *   Check if a connection/request already exists between the logged-in user and the target user.
        *   If not, create a new `Connection` object with `requester=request.user`, `receiver=target_user`, `status='pending'`.
        *   Add appropriate URL routing for this view.
    4.  **Implement `manage_request` View (Accept/Reject):**
        *   Create a view that takes a `connection_id` and an `action` ('accept' or 'reject').
        *   Verify the logged-in user is the `receiver` of the connection request.
        *   Update the `Connection` object's `status` based on the action. If rejecting, you could potentially delete the record or set status to 'rejected'. 'Accepted' is the key status.
        *   Add appropriate URL routing.

**Step 6.2: Display Connection Status & Actions on Profiles**

*   **Goal:** Integrate the connection logic into the user interface, primarily on user profiles.
*   **Tasks:**
    1.  **Update `profile_view`:**
        *   In the `profile_view`, determine the connection status between `request.user` and `profile_user`. Check for existing `Connection` objects involving both users.
        *   Pass this status information (e.g., 'not_connected', 'request_sent', 'request_received', 'connected') to the template context.
    2.  **Update `profile.html` Template:**
        *   Conditionally display buttons/text based on the connection status:
            *   If `not_connected`: Show a "Send Connection Request" button linking to the `send_request` view for `profile_user`.
            *   If `request_sent` (current user sent request to profile user): Show "Connection Request Sent". Maybe add a "Cancel Request" button (optional for MVP).
            *   If `request_received` (profile user sent request to current user): Show "Accept Request" and "Reject Request" buttons linking to the `manage_request` view with the correct `connection_id`.
            *   If `connected`: Show "Connected" or a "Remove Connection" button (optional for MVP).
        *   Hide these buttons/options entirely if the user is viewing their *own* profile (`profile_user == user`).

**Step 6.3: List Connections & Pending Requests**

*   **Goal:** Provide dedicated pages for users to see who they are connected with and who wants to connect with them.
*   **Tasks:**
    1.  **Create `list_connections` View:**
        *   Query `Connection` objects where the `request.user` is either the `requester` or `receiver`, and the `status` is 'accepted'.
        *   Extract the list of connected users (the *other* user in each connection object).
        *   Pass the list of connected users to a new template.
    2.  **Create `list_connections.html` Template:**
        *   Display the list of connected users, linking to their profiles.
    3.  **Create `list_pending_requests` View:**
        *   Query `Connection` objects where `request.user` is the `receiver` and `status` is 'pending'.
        *   Pass this list of pending `Connection` objects (including the requester info) to a new template.
    4.  **Create `list_pending_requests.html` Template:**
        *   Display the list of users who have sent requests.
        *   Include "Accept" and "Reject" buttons for each request, linking to the `manage_request` view.
    5.  **Add URLs:** Create URL patterns for these new list views.
    6.  **Update `base.html`:** Add navigation links to "My Connections" and "Pending Requests".

---
*Pause Point: At this stage, the core connection mechanism is functional and visible.*
---

**Step 6.4: Basic Messaging Model & Send Functionality**

*   **Goal:** Allow connected users to send simple text messages to each other.
*   **Tasks:**
    1.  **Create `Message` Model:**
        *   Define a new model named `Message` (likely in a new `messaging` app).
        *   Fields:
            *   `sender`: ForeignKey to `User`.
            *   `recipient`: ForeignKey to `User`.
            *   `content`: TextField.
            *   `timestamp`: DateTimeField (auto_now_add=True).
            *   `is_read`: BooleanField (default=False) (Optional for MVP, but useful later).
    2.  **Create Migrations:** Run `makemigrations` and `migrate`.
    3.  **Create `send_message` View:**
        *   This view might handle POST requests from a message form.
        *   It needs the `recipient_id` and the message `content`.
        *   **Crucially:** Verify that the `sender` (`request.user`) and `recipient` are actually connected (check for an 'accepted' `Connection` between them).
        *   If connected, create and save the `Message` object.
        *   Redirect back to the conversation view (or wherever the form was).
    4.  **Add URL:** Create a URL pattern for sending messages.

**Step 6.5: Display Conversation View**

*   **Goal:** Show the message history between the logged-in user and one specific connection.
*   **Tasks:**
    1.  **Create `conversation_view`:**
        *   Takes a `connection_user_id` (the user the current user is chatting with).
        *   Verify that `request.user` and the `connection_user` are connected.
        *   Fetch all `Message` objects where:
            *   (`sender`= `request.user` AND `recipient` = `connection_user`) OR
            *   (`sender`= `connection_user` AND `recipient` = `request.user`)
        *   Order messages by `timestamp`.
        *   Pass the messages and the `connection_user` to the template.
    2.  **Create `conversation.html` Template:**
        *   Display the messages chronologically.
        *   Include a simple form (textarea and submit button) that POSTs to the `send_message` view, including the `recipient_id` (likely as a hidden input).
    3.  **Add URL:** Create a URL pattern for the conversation view (e.g., `/messages/<str:username>/`).
    4.  **Link from Connections List:** Update `list_connections.html` to link each connection to their respective `conversation_view`.

---
*Pause Point: Basic 1-on-1 messaging between connections is now functional.*
---

**Step 7: Feed (posts, comments, activity)**
Many steps that gemini just implemented instead of giving the plan first, ill add slowly point by point whats going on

* Models: Post, Comment

* Apps: We can create a new feed app for this, or potentially integrate parts into users or portfolio where relevant (though a dedicated feed app is likely cleaner). Let's plan for a feed app.

**Step 7.1: Feed, Post & Comment Models**

Goal: Define the database structure for posts and comments.

Tasks:

* Create feed App:

    * Run python manage.py startapp feed in your terminal.

    * Add 'feed' to INSTALLED_APPS in settings.py.

* Define Post Model (feed/models.py)
* Define Comment Model (feed/models.py)
* Create Migrations:

    * Run python manage.py makemigrations feed

    * Run python manage.py migrate

**Step 7.2: Create Manual Post Functionality**

Goal: Allow logged-in users to write and submit their own text posts.

Tasks:

* Create Post Form (feed/forms.py)
* Create create_post View (feed/views.py)
* Create create_post.html Template (templates/feed/create_post.html)
* Add URL (feed/urls.py)
* Include in Main URLs (moviepeople/urls.py)
* Add Navigation Link: Add a "Create Post" link in base.html pointing to {% url 'feed:create_post' %}.

**Step 7.3: Modify Portfolio View to Create Posts**
Goal: Automatically create a Post of type portfolio_add when a user adds a new portfolio item.

**Step 7.4: Create the Main Feed View & Template**
Goal: Display a chronological list of posts (both user-generated and automatic) from the logged-in user and their connections.

Tasks:

* Create feed_view (feed/views.py)
* Create feed.html Template (templates/feed/feed.html)
* Add URL (feed/urls.py)
* Update Navigation: Make sure there's a "Feed" link in base.html pointing to {% url 'feed:feed_view' %}. This could be your main home link after login.

**Step 7.5:  Post Detail & Comment Functionality**
Goal: Create a page to view a single post and its comments, and allow users to add new comments.

Tasks:

* Create Comment Form (feed/forms.py)
* Create post_detail View (feed/views.py)
* Create post_detail.html Template (templates/feed/post_detail.html)
* Add URLs (feed/urls.py)

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