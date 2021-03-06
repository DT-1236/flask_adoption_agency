from flask import Flask, render_template, redirect, flash
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
        add_new_pet(form)
        return redirect('/')
    else:
        return render_template('add_pet.html', form=form)


@app.route('/<int:pet_id>', methods=['POST', 'GET'])
def display_pet_and_handle_edits(pet_id: int):
    """Displays pet information as well as an edit for for that pet"""

    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet)
    if form.validate_on_submit():
        edit_existing_pet(pet, form)
        return redirect(f'/{pet_id}')
    else:
        return render_template('pet.html', pet=pet, form=form)


def handle_uploaded_photo(pet: Pet, form: (AddPetForm, EditPetForm)):
    """Updates the Pet object to have an appropriate photo_url or to indicate that the image is on file.
    Saves the uploaded file to static/pet_photos/{pet.id}.{file_extension}.
    Does not commit - must be done outside of the function call"""
    if form.uploaded_photo.data:
        image_file = form.uploaded_photo.data
        filename = secure_filename(image_file.filename)
        extension = filename[filename.rfind('.') + 1:]
        filepath = f"static//pet_photos//{pet.id}.{extension}"
        image_file.save(filepath)
        pet.photo_url = f".{extension} on file"
    else:
        pet.photo_url = form.photo_url.data


def add_new_pet(form: AddPetForm):
    """Runs in the an add pet view function. Processes the AddPetForm and adds a new pet"""
    pet_dict = {
        key: value
        for (key, value) in form.data.items()
        if key not in ('csrf_token', 'uploaded_photo')
    }
    pet = Pet(**pet_dict)
    db.session.add(pet)
    db.session.commit()
    # Need a pet_id to create a path
    handle_uploaded_photo(pet, form)
    db.session.add(pet)
    db.session.commit()
    flash(f"Successfully added {pet.name}")


def edit_existing_pet(pet: Pet, form: EditPetForm):
    """Runs in an edit pet view function. Processes the EditPetForm to edit an existing pet"""
    pet.notes = form.notes.data
    pet.available = form.available.data
    handle_uploaded_photo(pet, form)
    db.session.add(pet)
    db.session.commit()
    flash(f"Upgraded fanciness on {pet.name}")
