"""Blogly application."""

from flask import Flask, render_template, redirect, request, flash
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.utils import secure_filename

from models import db, connect_db, Pet
from forms import AddPetForm, EditPetForm
from api_classes import PetFinder

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adoption'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = 'EXTRA SUPER SESCRT'
DebugToolbarExtension(app)
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False


@app.route('/')
def display_pets():
    """Displays list of all pets"""

    available_pets = Pet.query.filter_by(available=True).all()
    unavailable_pets = Pet.query.filter_by(available=False).all()
    return render_template(
        'pets.html',
        available_pets=available_pets,
        unavailable_pets=unavailable_pets,
        random=PetFinder.get_random())


@app.route('/add', methods=['POST', 'GET'])
def handle_add_form():
    """Function will handle the AddPetForm"""

    form = AddPetForm()
    if form.validate_on_submit():
        import pdb
        pdb.set_trace()
        pet = Pet(
            **{
                key: value
                for (key, value) in form.data.items() if key != 'csrf_token'
            })
        db.session.add(pet)
        db.session.commit()
        flash(f"Successfully added {pet.name}")
        return redirect('/')
    else:
        return render_template('add_pet.html', form=form)


@app.route('/<int:pet_id>', methods=['POST', 'GET'])
def display_pet_and_handle_edits(pet_id: int):
    """Displays pet information as well as an edit for for that pet"""

    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet)
    if form.validate_on_submit():
        pet.photo_url = form.photo_url.data
        pet.notes = form.notes.data
        pet.available = form.available.data
        db.session.add(pet)
        db.session.commit()
        flash(f"Upgraded fanciness on {pet.name}")
        return redirect(f'/{pet_id}')
    else:
        return render_template('pet.html', pet=pet, form=form)
