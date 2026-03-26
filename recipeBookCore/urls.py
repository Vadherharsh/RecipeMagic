from django.contrib import admin
from django.urls import path
from recipes import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('hello/', views.hello_world, name='hello_world'),
    path('recipelist/', views.recipelist, name='recipelist'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('recipeview/<int:id>/', views.recipe_view, name='recipe_view'),
    
    # NEW: Add these two lines for forgot password and register
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('register/', views.register, name='register'),
    
    # ===== NEW: Random Recipe URL =====
    path('random-recipe/', views.random_recipe, name='random_recipe'),
    
    # ===== Trending Recipes =====
    path('trending/', views.trending_recipes, name='trending'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

            