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

# ============================================
# RECIPE PDF GENERATION
# ============================================
import io
import os
from django.conf import settings
from django.http import FileResponse, HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem, Image, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

def recipe_pdf(request, id):
    try:
        recipe = RecipesList.objects.get(id=id)
    except RecipesList.DoesNotExist:
        return HttpResponse("Recipe not found", status=404)
        
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=50, leftMargin=50, topMargin=50, bottomMargin=50)
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        alignment=1, # Center
        textColor=colors.HexColor("#e65100"),
        fontSize=24,
        spaceAfter=14
    )
    
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        alignment=1,
        textColor=colors.HexColor("#666666"),
        fontSize=12,
        spaceAfter=20
    )
    
    h2_style = ParagraphStyle(
        'CustomH2',
        parent=styles['Heading2'],
        textColor=colors.HexColor("#333333"),
        fontSize=18,
        spaceBefore=16,
        spaceAfter=10,
        borderPadding=(0,0,4,0)
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        leading=16,
        textColor=colors.HexColor("#444444")
    )
    
    Story = []
    
    # Header Branding
    branding_style = ParagraphStyle('Brand', parent=styles['Normal'], alignment=1, fontSize=10, textColor=colors.HexColor("#888888"), spaceAfter=20)
    Story.append(Paragraph("<b>RecipeMagic<font color='#e65100'>.</font></b> Premium Recipe Collection", branding_style))
    
    # Title
    Story.append(Paragraph(recipe.recipe_name, title_style))
    
    # Image
    if recipe.recipe_image:
        # Assuming recipe.recipe_image is a FileField/ImageField, getting the actual file path
        img_path = os.path.join(settings.MEDIA_ROOT, str(recipe.recipe_image))
        if os.path.exists(img_path):
            try:
                # Add image, preserve aspect ratio, fit within 6 inches wide, 3.5 inches high
                img = Image(img_path, width=6*inch, height=3.5*inch, kind='proportional')
                img_table = Table([[img]], colWidths=[6.5*inch])
                img_table.setStyle(TableStyle([
                    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 20),
                ]))
                Story.append(img_table)
            except Exception as e:
                pass # Skip image if it fails to load or incorrect format
                
    # Description
    if recipe.recipe_dec:
        Story.append(Paragraph(f"<i>{recipe.recipe_dec}</i>", subtitle_style))
        
    # Meta info in a nice table
    meta_data = [[
        Paragraph(f"<b>Cuisine:</b><br/>{recipe.cuisine_type}", normal_style),
        Paragraph(f"<b>Difficulty:</b><br/>{recipe.difficulty}", normal_style),
        Paragraph(f"<b>Time:</b><br/>{recipe.cooking_time}", normal_style),
        Paragraph(f"<b>Rating:</b><br/>{recipe.recipe_rating}/5", normal_style)
    ]]
    
    meta_table = Table(meta_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1.2*inch])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f9f9f9")),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.HexColor("#e0e0e0")),
        ('BOX', (0,0), (-1,-1), 0.25, colors.HexColor("#e0e0e0")),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
        ('TOPPADDING', (0,0), (-1,-1), 12),
    ]))
    Story.append(meta_table)
    Story.append(Spacer(1, 25))
    
    # Divider
    Story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e0e0e0"), spaceBefore=1, spaceAfter=20))
    
    # Ingredients
    Story.append(Paragraph("Ingredients", h2_style))
    ingredients_list = []
    if hasattr(recipe, 'get_ingredients_list'):
        ingredients_list = recipe.get_ingredients_list
    elif recipe.recipe_ingredients:
        ingredients_list = recipe.recipe_ingredients.split(",")
        
    if ingredients_list:
        items = [ListItem(Paragraph(item, normal_style)) for item in ingredients_list]
        Story.append(ListFlowable(items, bulletType='bullet', leftIndent=15, spaceAfter=5))
    else:
        Story.append(Paragraph("No ingredients listed.", normal_style))
    Story.append(Spacer(1, 20))
    
    # Divider
    Story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e0e0e0"), spaceBefore=1, spaceAfter=20))
    
    # Directions
    Story.append(Paragraph("Directions", h2_style))
    directions_list = []
    if hasattr(recipe, 'get_directions_list'):
        directions_list = recipe.get_directions_list
    elif hasattr(recipe, 'recipe_direcions') and recipe.recipe_direcions: # Notice the typo in the model name 'recipe_direcions'
        directions_list = recipe.recipe_direcions.split("|")
        
    if directions_list:
        items = [ListItem(Paragraph(step, normal_style)) for step in directions_list]
        Story.append(ListFlowable(items, bulletType='1', leftIndent=15, spaceAfter=10))
    else:
        Story.append(Paragraph("No directions listed.", normal_style))
        
    # Build PDF
    def add_footer(canvas, doc):
        canvas.saveState()
        canvas.setFont('Helvetica', 9)
        canvas.setFillColor(colors.HexColor("#aaaaaa"))
        canvas.drawString(inch, 0.75 * inch, f"Generated automatically by RecipeMagic ({request.get_host()})")
        canvas.restoreState()
        
    doc.build(Story, onFirstPage=add_footer, onLaterPages=add_footer)
    
    buffer.seek(0)
    filename = f"{recipe.recipe_name.replace(' ', '_')}.pdf"
    return FileResponse(buffer, as_attachment=True, filename=filename)

