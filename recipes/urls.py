from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home_view, name='home'),           # 👈 CHANGED: Now home at root
    path('login/', views.login_view, name='login'),   # 👈 CHANGED: Login at /login/
    path('logout/', views.logout_view, name='logout'),
    path('hello/', views.hello_world, name='hello'),
    path('recipelist/', views.recipelist, name='recipelist'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('recipeview/<int:id>/', views.recipe_view, name='recipe_view'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)