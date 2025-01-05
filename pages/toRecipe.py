toRecipe.py
import os
import requests
import urllib.parse

# Returns recipe names and missing ingredients
def provide_recipe(ingredients, staples):
  api_key = os.getenv('RECIPE_API_KEY')
  all_ingred = ingredients + staples
  URL = f"https://api.spoonacular.com/recipes/findByIngredients?apiKey={api_key}&ingredients={all_ingred}"
  r = requests.get(url=URL)
  data = r.json()

  recipe_names = [recipe['title'] for recipe in data]
  print(recipe_names)

  missing_ingred_lists = [
    [ingredient['name'] for ingredient in recipe['missedIngredients']]
    for recipe in data
  ]

  recipe_instr = get_instructions(recipe_names, missing_ingred_lists)

  print(missing_ingred_lists)
  return recipe_names, missing_ingred_lists

def get_instructions(recipe_names, ingredients):


# Returns array of image urls
def provide_images(recipe_names):    
    images = []
    width=768
    height=768
    model='flux'
    seed=None

    for name in recipe_names:
      prompt = f"Create a high-quality, visually stunning image of {name}, styled as a gourmet dish from a luxury restaurant."        
      encoded_prompt = urllib.parse.quote(prompt)  # Encode prompt for URL
      image_url = f"https://pollinations.ai/p/{encoded_prompt}?width={width}&height={height}&seed={seed}&model={model}"
      images.append(image_url)
      print(image_url)

    return images
        

def get_recipes(ingredients, staples):
  print('get_recipes starting...')
  recipe_names, missing_ingredients = provide_recipe(ingredients, staples)
    
  print('provide_images processing...')
  images = provide_images(recipe_names)
    
  return recipe_names, missing_ingredients, images
