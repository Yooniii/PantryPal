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
        ingredients.append(line.strip("- ").strip())

      elif current_section == "instructions" and line.strip():
        instructions.append(line.strip("- ").strip())

    parsed_recipes.append({
      "name": name,
      "ingredients": ingredients,
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
        "You are a culinary expert. Your task is to generate a DISTINCT recipes "
        "using (some, not necessarily all) ingredients provided by the user."
        "Your responses should not use any asterisks and should follow this structured format: "
        "\n"
        "## Recipe <number>: <Recipe Name>"
        "\n"
        "### Ingredients: "
        "List all required ingredients here, separating each one into a new line. "
        "Clearly indicate missing ingredients by appending '(missing)' next to them."
        "\n"
        "### Instructions: "
        "Provide step-by-step cooking instructions, with each step listed on a new line. "
        "Steps should be concise but detailed enough to follow (1-2 sentences per step)."
        "\n\n"            
      ),
    },
    {   
      "role": "user",
      "content": (
        f"Here is the list of ingredients I have: {all_ingredients}."
        "Give me recipes using most of these ingredients."
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
    print(f"Recipe {recipe['name']}")
    print("Ingredients:")

    for ingredient in recipe['ingredients']:
      print(ingredient)
    
    print("Instructions:\n")
    for instruction in enumerate(recipe['instructions']):
      print(f"{instruction}")

  return recipes
        
def get_recipes(ingredients, staples):
  print('get_recipes starting...')
  recipes = provide_recipe(ingredients, staples)
  return recipes
