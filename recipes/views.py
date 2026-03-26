from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import RecipesList, recipeRequest
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
import random

# Create your views here.

def hello_world(request):
    return HttpResponse("<h1 style='color:red;'>hello world</h1>")

# HOME PAGE - Shows all recipes
def home_view(request):
    recipes_data = RecipesList.objects.all()
    return render(request, "index.html", {"recipes_data": recipes_data})

# CONTACT PAGE
def contact(request):
    if request.GET:
        user_name = request.GET.get("username")
        user_email = request.GET.get("email")
        user_recipe_name = request.GET.get("RecipeName")
        user_recipe_image = request.GET.get("RecipeImage")
        print(user_name, user_email, user_recipe_name, user_recipe_image)

        recipeRequest.objects.create(
            user=user_name, 
            email=user_email, 
            recipe_name=user_recipe_name, 
            recipe_image=user_recipe_image
        )
        messages.info(request, "Request submitted successfully")    
        return redirect("/contact/")

    return render(request, "contact.html")

# ABOUT PAGE
def about(request):
    return render(request, "about.html")

# RECIPE LIST PAGE WITH ADVANCED SEARCH
def recipelist(request):
    recipes_data = RecipesList.objects.all()
    
    # Get search parameters from request
    search_query = request.GET.get('search', '')
    cuisine = request.GET.get('cuisine', '')
    difficulty = request.GET.get('difficulty', '')
    min_rating = request.GET.get('min_rating', '')
    sort_by = request.GET.get('sort_by', '')
    
    # Apply filters
    if search_query:
        recipes_data = recipes_data.filter(recipe_name__icontains=search_query)
    
    if cuisine:
        recipes_data = recipes_data.filter(cuisine_type=cuisine)
    
    if difficulty:
        recipes_data = recipes_data.filter(difficulty=difficulty)
    
    if min_rating:
        recipes_data = recipes_data.filter(recipe_rating__gte=int(min_rating))
    
    # Apply sorting
    if sort_by == 'rating':
        recipes_data = recipes_data.order_by('-recipe_rating')
    elif sort_by == 'name':
        recipes_data = recipes_data.order_by('recipe_name')
    elif sort_by == 'newest':
        recipes_data = recipes_data.order_by('-id')  # Assuming higher id = newer
    
    # Get unique values for filter dropdowns
    cuisines = RecipesList.objects.values_list('cuisine_type', flat=True).distinct()
    difficulties = RecipesList.objects.values_list('difficulty', flat=True).distinct()
    
    context = {
        'recipes_data': recipes_data,
        'cuisines': cuisines,
        'difficulties': difficulties,
        'search_query': search_query,
        'selected_cuisine': cuisine,
        'selected_difficulty': difficulty,
        'selected_rating': min_rating,
        'selected_sort': sort_by,
    }
    
    return render(request, "recipePage.html", context)

# RECIPE DETAIL VIEW PAGE
def recipe_view(request, id):
    recipes_data = RecipesList.objects.get(id=id)
    print(recipes_data)
    ingredients = recipes_data.recipe_ingredients.split(",")
    return render(request, "recipe_view.html", {
        "recipes_data": recipes_data,
        "ingredients": ingredients
    })

# LOGIN VIEW
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')  # after login go to home page
        else:
            messages.error(request, "Invalid Username or Password")

    return render(request, "login.html")

# LOGOUT VIEW
def logout_view(request):
    logout(request)
    return redirect('login')

# ============================================
# FORGOT PASSWORD FUNCTIONALITY
# ============================================
def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        
        # Check if user exists with this email
        try:
            user = User.objects.get(email=email)
            
            # Generate a random temporary password
            temp_password = f"Temp@{random.randint(1000, 9999)}"
            
            # Set temporary password
            user.set_password(temp_password)
            user.save()
            
            # In a real project, you would send an email here
            # For now, we'll show the password on screen (for testing)
            messages.success(request, f"Your temporary password is: {temp_password}")
            messages.info(request, "Please login with this password and change it later.")
            
            return redirect('login')
            
        except User.DoesNotExist:
            messages.error(request, "No account found with this email address!")
    
    return render(request, "forgot_password.html")

# ============================================
# REGISTER (CREATE ACCOUNT) FUNCTIONALITY
# ============================================
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        
        # Validation checks
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('register')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect('register')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect('register')
        
        # Create new user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        
        messages.success(request, "Account created successfully! Please login.")
        return redirect('login')
    
    return render(request, "register.html")

# ============================================
# RANDOM RECIPE FUNCTIONALITY
# ============================================
def random_recipe(request):
    """Redirect to a random recipe"""
    import random
    recipes = RecipesList.objects.all()
    
    if recipes.exists():
        random_recipe = random.choice(recipes)
        return redirect('recipe_view', id=random_recipe.id)
    else:
        messages.error(request, "No recipes available yet!")
        return redirect('recipelist')
    
# ============================================
# USER PROFILE PAGE
# ============================================
def user_profile(request, username):
    """Display user profile with their activity"""
    profile_user = get_object_or_404(User, username=username)
    
    # Get user's recipes (if they have any - you'd need a UserRecipe model for this)
    # For now, we'll show their reviews and favorites
    
    # Get user's reviews
    user_reviews = Review.objects.filter(user=profile_user).select_related('recipe').order_by('-created_at')
    
    # Get user's favorites
    user_favorites = Favorite.objects.filter(user=profile_user).select_related('recipe').order_by('-created_at')
    
    # Get counts
    review_count = user_reviews.count()
    favorite_count = user_favorites.count()
    
    # Calculate average rating given by user
    avg_rating_given = user_reviews.aggregate(Avg('rating'))['rating__avg']
    if avg_rating_given:
        avg_rating_given = round(avg_rating_given, 1)
    else:
        avg_rating_given = 0
    
    # Check if this is the logged-in user's own profile
    is_own_profile = False
    if request.user.is_authenticated and request.user.username == username:
        is_own_profile = True
    
    context = {
        'profile_user': profile_user,
        'user_reviews': user_reviews,
        'user_favorites': user_favorites,
        'review_count': review_count,
        'favorite_count': favorite_count,
        'avg_rating_given': avg_rating_given,
        'is_own_profile': is_own_profile,
    }
    
    return render(request, 'profile.html', context)


# ============================================
# TRENDING RECIPES
# ============================================
def trending_recipes(request):
    """Show most popular recipes based on ratings"""
    # Order by highest rating first, then by newest
    recipes = RecipesList.objects.all().order_by('-recipe_rating', '-id')
    
    # Add avg_rating attribute for template compatibility
    for recipe in recipes:
        recipe.avg_rating = recipe.recipe_rating
    
    context = {
        'trending_recipes': recipes,
        'total_recipes': recipes.count(),
    }
    
    return render(request, 'trending.html', context)

