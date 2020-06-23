from . import main
from flask import render_template, request, redirect, url_for
from ..models import Pitch, Comments
from .forms import PitchForm, CommentsForm
from .. import db
import requests

@main.route('/')
def index():

    pitches = Pitch.query.all()

    title = 'Pitch'
    url = 'http://quotes.stormconsultancy.co.uk/random.json'
    r = requests.get(url).json()
    print(r)
    data = {
        'author': r['author'],
        'quote': r['quote']
    }
    return render_template('index.html', title=title, data=data, pitches=pitches)

@main.route('/create_pitch', methods=['GET', 'POST'])
def pitch():
    form = PitchForm()
    if form.is_submitted():
        title = form.title.data
        pitch = form.pitch.data

        pitch = Pitch(title = title, pitch=pitch)

        db.session.add(pitch)
        db.session.commit()

        return redirect(url_for('main.index'))
    
    title = 'New pitch'
    return render_template('pitch.html', title=title, form=form)

@main.route('/pitch/<int:pitch_id>', methods=['GET', 'POST'])
def single_pitch(pitch_id):
    pitch = Pitch.get_single_pitch(pitch_id)
    comments=Comments.query.all()
    print(comments)
    form = CommentsForm()
    if form.is_submitted():
        comment = form.comments.data
        pitch_id = pitch_id
        save_comment = Comments(comment=comment, pitch_id = pitch_id)
        db.session.add(save_comment)
        db.session.commit()
        return redirect(url_for('main.single_pitch', pitch_id=pitch_id))
    
    title = 'single_pitch'
    return render_template('single_pitch.html', pitch=pitch, title=title, comments = comments, form = form)

@main.route('/update_pitch/<int:pitch_id>', methods=['GET', 'POST'])
def update_pitch(pitch_id):
    pitch = Pitch.get_single_pitch(pitch_id)
    if request.method == 'POST':
        pitch.title = request.form['title']
        pitch.pitch = request.form['pitch']
        db.session.commit()
        return redirect(url_for('main.index'))
    else:
        title = 'update'
        return render_template('update_pitch.html', title=title, pitch=pitch)

@main.route('/delete/<int:pitch_id>', methods=['GET', 'POST'])
def delete(pitch_id):
    pitch = Pitch.get_single_pitch(pitch_id)
    db.session.delete(pitch)
    db.session.commit()
    return redirect(url_for('main.index'))