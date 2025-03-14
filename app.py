from dotenv import load_dotenv
from flask import Flask, render_template, request
from pages.toRecipe import get_recipes
from openai import OpenAI
import os

app = Flask(__name__)

@app.route('/')
@app.route('/home')
@app.route('/home.html', methods = ["POST", "GET"])
def home():
  return render_template('to-recipe.html')

@app.route('/toRecipe', methods = ["GET", "POST"])
def recipe():
  try:     
    print(f'### {request.full_path} : {request.method}')
    
    if request.method == 'GET':
      return render_template('to-recipe.html')

    form_data = request.form
    print(f'### form_data : {form_data}')
        
    if request.method == 'POST' and form_data.get('user-ingred'):
      ingredients = form_data['user-ingred']
      staples_list = form_data.getlist('staples') 
      diet_restrictions = form_data.getlist('diet')
      print(diet_restrictions)
            
      staples = ", ".join(staples_list)
      diet = ", ".join(diet_restrictions)

      if len(ingredients.strip()) == 0:
        print('Not enough ingredients inputted')
        return render_template('error.html')
            
      else: 
        recipes = get_recipes(ingredients, staples, diet)
        return render_template('results.html', recipes=recipes)
          
    else:
      return render_template('to-recipe.html')
    
  except Exception as e:
    print('Error Occurred: ', e)
    return render_template('error.html')

if __name__ == '__main__':
  app.run('0.0.0.0', port=80, debug=True)

