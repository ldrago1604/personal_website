"""
views.py is used to route all other html pages which is used in website.
"""
from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)


# the route() decorator to tell Flask what URL should trigger our function.
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('note added successfully', category='success')

    return render_template("home.html", user=current_user)

@login_required
@views.route('/delete-note/<int:id>')
def delete_note(id):
    note = Note.query.filter_by(id=id).first()
    print(note)
    db.session.delete(note)
    db.session.commit()

    return redirect(url_for('views.home'))


@login_required
@views.route('/update-note/<int:id>', methods=['GET', 'POST'])
def update_note(id):
    note = Note.query.filter_by(id=id).first()

    if request.method == 'POST':
        up_note = request.form.get('update-note')
        note = Note.query.filter_by(id=id).first()
        note.data = up_note
        db.session.add(note)
        db.session.commit()

        return redirect(url_for('views.home'))


    return render_template('update_note.html', note=note, user=current_user)