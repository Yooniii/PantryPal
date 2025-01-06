import os
import requests
from openai import OpenAI

API_KEY = os.getenv('API_KEY') # load API key

# Extract recipes from the content field
def extract_recipes(response):
  content = response.choices[0].message.content

  # Split recipe names using the "## Recipe" pattern
  recipes = content.split("## Recipe")[1:]  
  parsed_recipes = []
  
  # Split ingredients & instructions 
  for recipe in recipes:
    ingredients = []
    instructions = []
    missing_ingr =[]
    current_section = ""

    lines = recipe.strip().split("\n")
    name = lines[0].strip(":").strip()

    for line in lines[1:]:
      if line.startswith("### Ingredients"):
        current_section = "ingredients"
        continue  
      
      if line.startswith("### Instructions"):
        current_section = "instructions"
        continue 

      if current_section == "ingredients" and line.strip():
        if ('missing' in line):
          missing_ingr.append(line.strip("- ").strip().split('(missing)')[0].strip())
        else:
          ingredients.append(line.strip("- ").strip())

      elif current_section == "instructions" and line.strip():
        instructions.append(line.strip("- ").strip())
    
    parsed_recipes.append({
      "name": name,
      "ingredients": ingredients,
      "missing_ingredients": missing_ingr,
      "instructions": instructions
    })

  return parsed_recipes

# Returns recipes
def provide_recipe(ingredients, staples):
  all_ingredients = ingredients + staples
  client = OpenAI(api_key=API_KEY, base_url="https://api.perplexity.ai")

  messages = [
    {
      "role": "system",
      "content": (
        "You are a culinary expert. Generate three DISTINCT recipes "
        "using (some, not necessarily all) ingredients provided by the user."
        "Do not use any asterisks or say anything else: strictly follow this format: "
        "\n ## Recipe <number>. <Recipe Name> \n"
        "### Ingredients: "
        "List all required ingredients here, each one on a new line. "
        "Indicate missing ingredients by appending '(missing)' next to them."
        "\n ### Instructions: "
        "Provide step-by-step cooking instructions, each step on a new line. "
        "Steps should be concise but detailed enough to follow (1-2 sentences per step)."
        "\n\n"            
      ),
    },
    {   
      "role": "user",
      "content": (
        f"The ingredients I have: {all_ingredients}."
        "Give me recipes using (some, not necessarily all) of them."
      ),
    },
  ]

  response = client.chat.completions.create(
    model="llama-3.1-sonar-large-128k-online",
    messages=messages
  )

  # Parse the response
  recipes = extract_recipes(response)

  # Display the results
  for recipe in recipes:
    image_url = fetch_recipe_image(recipe["name"])
    recipe["image_url"] = image_url
    print({recipe['image_url']})
    
    print(f"Recipe {recipe['name']}")
    print("Ingredients:")

    for ingredient in recipe['ingredients']:
      print(ingredient)
    
    print("Instructions:\n")
    for instruction in enumerate(recipe['instructions']):
      print(f"{instruction}")

  return recipes

# Fetch an image for a given recipe
def fetch_recipe_image(recipe_name):
  endpoint = "https://api.bing.microsoft.com/v7.0/images/search"
  api_key = os.getenv('IMAGE_API_KEY')
  headers = {"Ocp-Apim-Subscription-Key": api_key}
  params = {"q": recipe_name, "count": 1}

  response = requests.get(endpoint, headers=headers, params=params)
  if response.status_code == 200:
    data = response.json()
    if data["value"]:
      return data["value"][0]["contentUrl"]  # Return the URL of first image
  
  return None

        
def get_recipes(ingredients, staples):
  print('get_recipes starting...')
  recipes = provide_recipe(ingredients, staples)

  return recipes
