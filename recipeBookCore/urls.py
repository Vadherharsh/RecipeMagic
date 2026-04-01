from django.contrib import admin
from django.urls import path, include
from recipes import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('hello/', views.hello_world, name='hello_world'),
    path('recipelist/', views.recipelist, name='recipelist'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('recipeview/<int:id>/', views.recipe_view, name='recipe_view'),
    path('recipe/<int:id>/pdf/', views.recipe_pdf, name='recipe_pdf'),
    # NEW: Add these two lines for forgot password and register
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('register/', views.register, name='register'),
    
    # ===== NEW: Random Recipe URL =====
    path('random-recipe/', views.random_recipe, name='random_recipe'),
    
    # ===== Trending Recipes =====
    path('trending/', views.trending_recipes, name='trending'),
    
    # ===== Favorites =====
    path('toggle-favorite/<int:id>/', views.toggle_favorite, name='toggle_favorite'),
    path('favorites/', views.favorites_list, name='favorites'),

    # ===== User Profile =====
    path('profile/<str:username>/', views.user_profile, name='user_profile'),

    # ===== OTP & Password Reset =====
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('resend-otp/', views.resend_otp, name='resend_otp'),
    path('reset-password-form/', views.reset_password, name='reset_password'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

            