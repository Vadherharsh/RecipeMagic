# 🍳 RecipeMagic

A full-featured **Recipe Management Web Application** built with **Django 5.2**. Browse, search, and discover delicious recipes with advanced filtering, nutrition tracking, and user authentication.

---

## ✨ Features

### 🔍 Recipe Browsing & Search
- Browse all recipes with a beautiful card-based layout
- **Advanced Search** — filter by name, cuisine type, difficulty level, and minimum rating
- **Sorting** — sort recipes by rating, name, or newest first
- **Random Recipe** — feeling adventurous? Get a random recipe suggestion

### 🥗 Recipe Details
- Full recipe view with ingredients, directions, and ratings
- **Nutrition Information** — calories, protein, fat, and carbs per serving
- **Cuisine Type** — Indian, Chinese, Italian, Mexican, Thai, Gujarati, Kathiyawadi, Punjabi, and more
- **Cooking Time & Difficulty** — know what you're getting into before you start

### 👤 User Authentication
- **Login / Logout** system
- **User Registration** — create new accounts
- **Forgot Password** — reset password with a temporary password

### 📬 Contact & Recipe Requests
- Submit recipe requests through the contact form
- Request specific recipes you'd like to see added

### ⚙️ Admin Dashboard
- Custom Django admin panel with organized fieldsets
- Inline editing for nutrition values and ratings
- Search and filter recipes directly from the admin
- Branded admin header — *"RecipeMagic Administration"*

---

## 🛠️ Tech Stack

| Layer        | Technology           |
|--------------|----------------------|
| **Backend**  | Python 3, Django 5.2 |
| **Database** | SQLite3              |
| **Frontend** | HTML5, CSS3, Django Templates |
| **Auth**     | Django Built-in Authentication |

---

## 📁 Project Structure

```
RecipeMagic/
├── manage.py                  # Django management script
├── recipeBookCore/            # Project settings & configuration
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── recipes/                   # Main app
│   ├── models.py              # RecipesList & recipeRequest models
│   ├── views.py               # All view functions
│   ├── admin.py               # Custom admin configuration
│   ├── urls.py                # App-level URL routing
│   └── templates/             # HTML templates
│       ├── index.html         # Home page
│       ├── recipePage.html    # Recipe listing with filters
│       ├── recipe_view.html   # Individual recipe detail
│       ├── login.html         # Login page
│       ├── register.html      # Registration page
│       ├── forgot_password.html
│       ├── contact.html       # Contact / request form
│       ├── about.html         # About page
│       ├── trending.html      # Trending recipes
│       ├── template.html      # Base template
│       └── footer.html        # Footer partial
├── static/                    # Static assets (CSS)
│   ├── style.css
│   ├── index.css
│   ├── contact.css
│   └── main.css
└── .gitignore
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+** installed
- **pip** (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Vadherharsh/RecipeMagic.git
   cd RecipeMagic
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **macOS / Linux:**
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install django pillow
   ```

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser** (to access the admin panel)
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Open in browser**
   ```
   http://127.0.0.1:8000/
   ```

---

## 📌 Available URLs

| URL                        | Description              |
|----------------------------|--------------------------|
| `/`                        | Home page                |
| `/recipelist/`             | Recipe listing with filters |
| `/recipeview/<id>/`        | Recipe detail page       |
| `/contact/`                | Contact / request form   |
| `/about/`                  | About page               |
| `/login/`                  | Login page               |
| `/register/`               | Registration page        |
| `/forgot-password/`        | Forgot password          |
| `/random-recipe/`          | Random recipe redirect   |
| `/admin/`                  | Django admin panel       |

---

## 👨‍💻 Author

**Harsh Vadher**

- GitHub: [@Vadherharsh](https://github.com/Vadherharsh)

---

## 📄 License

This project is open source and available for educational purposes.
