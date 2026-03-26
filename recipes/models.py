from django.db import models

class RecipesList(models.Model):
    recipe_name = models.CharField(max_length=200, null=False, blank=False)
    recipe_dec = models.CharField(max_length=500, null=False, blank=False)
    recipe_rating = models.IntegerField(null=False, blank=False)
    recipe_direcions = models.CharField(max_length=500, null=False, blank=False)
    recipe_ingredients = models.CharField(
        max_length=500,
        null=False,
        blank=False,
        help_text="enter value split by ',' ex: <b>nutritional yeast, soya sauce</b>"
    )
    recipe_image = models.ImageField(upload_to="RecipeImages", blank=True, null=True)
    
    # ===== NEW FIELDS - Add these! =====
    
    # Nutrition Fields
    calories = models.IntegerField(default=0, help_text="Calories per serving")
    protein = models.FloatField(default=0, help_text="Protein in grams")
    fat = models.FloatField(default=0, help_text="Fat in grams")
    carbs = models.FloatField(default=0, help_text="Carbohydrates in grams")
    
    # Cuisine Type
    cuisine_type = models.CharField(
        max_length=100, 
        default="Indian",
        choices=[
            ('Indian', 'Indian'),
            ('Chinese', 'Chinese'),
            ('Italian', 'Italian'),
            ('Mexican', 'Mexican'),
            ('Thai', 'Thai'),
            ('Continental', 'Continental'),
            ('Gujarati', 'Gujarati'),
            ('Kathiyawadi', 'Kathiyawadi'),
            ('Punjabi', 'Punjabi'),
            ('South Indian', 'South Indian'),
            ('Dessert', 'Dessert'),
            ('Breakfast', 'Breakfast'),
            ('Other', 'Other')
        ]
    )
    
    # Cooking Time
    cooking_time = models.CharField(
        max_length=50, 
        default="30 mins",
        help_text="e.g., 15 mins, 30-40 mins, 1 hour"
    )   
    
    # Difficulty Level
    difficulty = models.CharField(
        max_length=20, 
        default="Easy",
        choices=[
            ('Easy', 'Easy'),
            ('Medium', 'Medium'),
            ('Hard', 'Hard')
        ]
    )

    def __str__(self):
        return self.recipe_name


class recipeRequest(models.Model):
    user = models.CharField(max_length=500, null=False, blank=False)
    email = models.EmailField(null=False, blank=False)
    recipe_name = models.CharField(max_length=500, null=False, blank=False)
    recipe_image = models.ImageField(upload_to="RecipeRequestImages", blank=True, null=True)

    def __str__(self):
        return f"{self.recipe_name} requested by {self.user}"