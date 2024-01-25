from flask import Flask, render_template, request, redirect, session, flash
from flask_app import app 
from flask_app.models.recipe_model import Recipe
from flask_app.models.user_model import User

@app.route('/recipes/new')
def create_recipe_page():
    if 'user_id' not in session:
        return redirect('/')

    return render_template("create_recipe.html")



@app.route('/recipes/create', methods=['POST'])
def create_recipe():
    
    data = {
        'user_id': session['user_id'],
        'name': request.form['name'],
        'description': request.form['description'],
        'instruction': request.form['instruction'],
        'under_30_minutes': request.form['under_30_minutes'],
        'date_cooked': request.form['date_cooked']
    }

    if not Recipe.validate_recipe(request.form):
        return redirect('/recipes/new')
    
    
    Recipe.create_recipe(data)
    return redirect('/dash')


#route to read one recipe
@app.route('/recipes/<int:id>')
def show_one_recipe(id):
    if 'user_id' not in session:
        flash("You must be logged in to view this page")
        session.clear()
        return redirect('/')

    data = {
        'id': id
        } 
    
    current_user = User.get_user_with_id({'user_id': session['user_id']})

    recipe = Recipe.read_one_recipe(data)
    return render_template('view_one_recipe.html', recipe = recipe, current_user = current_user)

#route to edit one recipe
@app.route('/recipes/edit/<int:id>')
def edit_one_page(id):
    if 'user_id' not in session:
        flash("You must be logged in to view this page")
        session.clear()
        return redirect('/')

    data = {
        'id': id
    }

    recipe = Recipe.read_one_recipe(data)

    return render_template('edit_recipe.html', recipe = recipe)

#route to edit the recipe we are currently viewing
@app.route('/recipes/update', methods=['POST'])
def edit_recipe():

    data = {
        'id' : request.form['id'],
        'user_id': session['user_id'],
        'name': request.form['name'],
        'description': request.form['description'],
        'instruction': request.form['instruction'],
        'under_30_minutes': request.form['under_30_minutes'],
        'date_cooked': request.form['date_cooked']
    }

    id = request.form['id']

    if not Recipe.validate_recipe(request.form):
        return redirect(f'/recipes/edit/{data.id}')

    Recipe.update_recipe(data)

    return redirect('/dash')

@app.route('/recipes/delete/<int:recipe_id>')
def delete_recipe(recipe_id):
    this_recipe = {
        'id': recipe_id
    }

    Recipe.delete_recipe(this_recipe)

    return redirect('/dash')