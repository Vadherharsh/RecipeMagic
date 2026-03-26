from django.contrib import admin
from .models import RecipesList, recipeRequest

class RecipesListAdmin(admin.ModelAdmin):
    # What shows in the list view - Added new fields!
    list_display = ('recipe_name', 'cuisine_type', 'calories', 'protein', 'fat', 'carbs', 'recipe_rating', 'difficulty', 'id')
    
    # Add search functionality
    search_fields = ('recipe_name', 'recipe_dec', 'cuisine_type')
    
    # Add filters - More filter options now!
    list_filter = ('cuisine_type', 'difficulty', 'recipe_rating')
    
    # Make it look nice with all fields organized
    fieldsets = (
        ('Basic Information', {
            'fields': ('recipe_name', 'recipe_dec', 'recipe_image')
        }),
        ('Recipe Details', {
            'fields': ('recipe_ingredients', 'recipe_direcions', 'recipe_rating')
        }),
        ('Nutrition Information', {  # NEW SECTION
            'fields': ('calories', 'protein', 'fat', 'carbs'),
            'description': 'Enter nutrition values per serving (numbers only, no "g" needed)'
        }),
        ('Additional Info', {  # NEW SECTION
            'fields': ('cuisine_type', 'cooking_time', 'difficulty'),
        }),
    )
    
    # Make calories, protein, etc. editable directly in list view
    list_editable = ('calories', 'protein', 'fat', 'carbs', 'recipe_rating')

class recipeRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'recipe_name')
    search_fields = ('user', 'email', 'recipe_name')

# Register with the improved classes
admin.site.register(RecipesList, RecipesListAdmin)
admin.site.register(recipeRequest, recipeRequestAdmin)

# Customize admin header
admin.site.site_header = "RecipeMagic Administration"
admin.site.site_title = "RecipeMagic Admin"
admin.site.index_title = "Welcome to RecipeMagic Dashboard"