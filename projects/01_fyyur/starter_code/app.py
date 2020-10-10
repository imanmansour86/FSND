#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler, error
from flask_wtf import Form
from flask_migrate import Migrate
from forms import *
import sys

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


class Show(db.Model):
    __tablename__ = 'show'

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    venue = db.relationship('Venue')
    venue_id = db.Column(db.Integer, db.ForeignKey(
        'venue.id', ondelete='CASCADE'), nullable=False)
    artist = db.relationship('Artist')
    artist_id = db.Column(db.Integer, db.ForeignKey(
        'artist.id', ondelete='CASCADE'), nullable=False)


class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(120)))
    website = db.Column(db.String(500))
    seeking_talent = db.Column(db.Boolean(), default=False)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship('Show')

    # TODO: implement any missing fields, as a database migration using Flask-Migrate


class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(120)))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(500))
    seeking_venue = db.Column(db.Boolean(), default=False)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship('Show')

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.

    data = []

# Get distince location
    locations = Venue.query.distinct(Venue.city, Venue.state).order_by(
        Venue.state, Venue.city).all()

# Iterate over cities and states
    for location in locations:
        data_venues = []

    # get venues by area
        venues = Venue.query.filter_by(
            city=location.city).filter_by(state=location.state).all()
        for venue_row in venues:
            upcoming_shows = Show.query.filter(Show.venue_id == venue_row.id).filter(
                Show.start_time > datetime.now()).all()
            data_venues.append({'id': venue_row.id, 'name': venue_row.name,
                                'num_upcoming_shows': len(upcoming_shows)})

        data.append({
            'city': location.city,
            'state': location.state,
            'venues': data_venues
        })

    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

    search_string = request.form.get('search_term')
    search_term = Venue.query.filter(
        Venue.name.ilike('%{}%'.format(search_string))).all()
    datas = []
    response = {}
    for word in search_term:
        upcoming_shows = Show.query.filter(Show.venue_id == word.id).filter(
            Show.start_time > datetime.now()).all()
        datas.append({'id': word.id, 'name': word.name,
                      'num_upcoming_shows': len(upcoming_shows)})

        response = {
            'count': len(search_term),
            'data': datas
        }

    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id

    # Get venue by Id:
    data_venue = Venue.query.filter(Venue.id == venue_id).first()

    upcoming_shows_dict = []
    upcoming_shows = Show.query.filter(Show.venue_id == venue_id).filter(
        Show.start_time > datetime.now()).all()  # get upcoming shows by id
    for upcoming_show in upcoming_shows:
        upcoming_shows_dict.append({

            'artist_id': upcoming_show.artist.id,
            'artist_name': upcoming_show.artist.name,
            'artist_image_link': upcoming_show.artist.image_link,
            'start_time': str(upcoming_show.start_time)
        })

    past_shows_dict = []
    past_shows = Show.query.filter(Show.venue_id == venue_id).filter(
        Show.start_time < datetime.now()).all()  # get past_shows_count  by id

    for past_show in past_shows:
        past_shows_dict.append({

            'artist_id': past_show.artist.id,
            'artist_name': past_show.artist.name,
            'artist_image_link': past_show.artist.image_link,
            'start_time': str(past_show.start_time)
        })

    data = {
        'id': data_venue.id,
        'name': data_venue.name,
        'genres': data_venue.genres,
        'address': data_venue.address,
        'city': data_venue.city,
        'state': data_venue.state,
        'phone': data_venue.phone,
        'website': data_venue.website,
        'facebook_link': data_venue.facebook_link,
        'seeking_talent': data_venue.seeking_talent,
        'image_link': data_venue.image_link,
        'past_shows': past_shows_dict,
        'upcoming_shows': upcoming_shows_dict,
        'past_shows_count': len(past_shows),
        'upcoming_shows_count': len(upcoming_shows)
    }

    return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    error = False
    try:
        venue = Venue(
            name=request.form['name'],
            city=request.form['city'],
            state=request.form['state'],
            address=request.form['address'],
            phone=request.form['phone'],
            genres=request.form['genres'],
            facebook_link=request.form['facebook_link']
        )
        print(venue)
        db.session.add(venue)
        db.session.commit()

    except:
        error = True
        db.session.rollback()
        print('this is an error')
        print("Oops!", sys.exc_info()[0], "occurred.")

    finally:
        db.session.close()
    if error:
        flash('An error occurred. Venue ' +
              request.form['name'] + ' could not be listed.')
        abort(400)

    else:
        flash('Venue ' + request.form['name'] + ' was successfully listed!')

    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion

    # on successful db insert, flash success
    # flash('Venue ' + request.form['name'] + ' was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
    error = False
    try:
        venue = Venue.query.filter_by(id=venue_id).delete()
        db.session.commit()
    except:
        error = True
        db.session.rollback()
    finally:
        db.session.close()
    if error:
        abort(400)
        flash('Cannot delete Venue')
    else:
        flash('Delete Venue completed')

    return render_template('pages/home.html')

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    # return None

#  Artists
#  ----------------------------------------------------------------


@app.route('/artists')
def artists():
    # TODO: replace with real data returned from querying the database

    data = []
    all_artists = Artist.query.order_by(Artist.id).all()
    for artist in all_artists:
        data.append({

            'id': artist.id,
            'name': artist.name
        })

    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".

    search_string = request.form.get('search_term')
    artists = Artist.query.filter(
        Artist.name.ilike('%{}%'.format(search_string))).all()
    response = {}
    datas = []
    for artist in artists:
        upcoming_shows = Show.query.filter(Show.artist_id == artist.id).filter(
            Show.start_time > datetime.now()).all()
        datas.append({
            'id': artist.id,
            'name': artist.name,
            'num_upcoming_shows': len(upcoming_shows)
        })

        response = {
            'count': len(artists),
            'data': datas
        }

    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id

    # Get artist by Id:
    # first gets object inside the array
    data_artist = Artist.query.filter(Artist.id == artist_id).first()
    past_shows_dict = []
    past_shows = Show.query.filter(Show.artist_id == artist_id).filter(
        Show.start_time < datetime.now()).all()
    for past_show in past_shows:
        past_shows_dict.append({
            'venue_id': past_show.venue.id,
            'venue_name': past_show.venue.name,
            'venue_image_link': past_show.venue.image_link,
            'start_time': str(past_show.start_time)
        })

    upcoming_shows_dict = []
    upcoming_shows = Show.query.filter(Show.artist_id == artist_id).filter(
        Show.start_time > datetime.now()).all()  # get upcoming shows by id
    for upcoming_show in upcoming_shows:
        upcoming_shows_dict.append({

            'venue_id': upcoming_show.venue.id,
            'venue_name': upcoming_show.venue.name,
            'venue_image_link': upcoming_show.venue.image_link,
            'start_time': str(upcoming_show.start_time)
        })

    data = {
        'id': data_artist.id,
        'name': data_artist.name,
        'genres': data_artist.genres,
        'city': data_artist.city,
        'state': data_artist.state,
        'phone': data_artist.phone,
        'website': data_artist.website,
        'facebook_link': data_artist.facebook_link,
        'seeking_venue': data_artist.seeking_venue,
        'seeking_description': data_artist.seeking_description,
        'image_link': data_artist.image_link,
        'past_shows': past_shows_dict,
        'upcoming_shows': upcoming_shows_dict,
        'past_shows_count': len(past_shows),
        'upcoming_shows_count': len(upcoming_shows)
    }

    return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------


@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()

    artist = Artist.query.filter(Artist.id == artist_id).first()

    # TODO: populate form with fields from artist with ID <artist_id>
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes
    error = False
    try:
        artist = Artist.query.filter(Artist.id == artist_id).first()
        artist.name = request.form['name']
        artist.genres = request.form['genres']
        artist.city = request.form['city']
        artist.state = request.form['state']
        artist.phone = request.form['phone']
        artist.facebook_link = request.form['facebook_link']
        db.session.commit()
    except:
        error = True
        print('this is an error')
        print("Oops!", sys.exc_info()[0], "occurred.")
        db.session.rollback()

    finally:
        db.session.close()
    if error:
        flash('An error occurred. Artist ' +
              request.form['name'] + ' could not be updated.')
        abort(400)
    else:
        flash('Artist ' + request.form['name'] + ' was successfully updated!')

    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = Venue.query.filter(Venue.id == venue_id).first()

    # TODO: populate form with values from venue with ID <venue_id>
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes

    error = False
    try:
        venue = Venue.query.filter(Venue.id == venue_id).first()
        venue.name = request.form['name']
        venue.genres = request.form['genres']
        venue.city = request.form['city']
        venue.state = request.form['state']
        venue.phone = request.form['phone']
        venue.facebook_link = request.form['facebook_link']
        db.session.commit()
    except:
        error = True
        print('this is an error')
        print("Oops!", sys.exc_info()[0], "occurred.")
        db.session.rollback()

    finally:
        db.session.close()
    if error:
        flash('An error occurred. Venue ' +
              request.form['name'] + ' could not be updated.')
        abort(400)
    else:
        flash('Venue ' + request.form['name'] + ' was successfully updated!')

    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():

    error = False
    try:
        artist = Artist(
            name=request.form['name'],
            city=request.form['city'],
            state=request.form['state'],
            phone=request.form['phone'],
            genres=request.form['genres'],
            facebook_link=request.form['facebook_link']
        )
        db.session.add(artist)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print('this is an error')
        print("Oops!", sys.exc_info()[0], "occurred.")

    finally:
        db.session.close()
    if error:
        flash('An error occurred. Artist ' +
              request.form['name'] + ' could not be listed.')
        abort(400)
    else:
        flash('Artist ' + request.form['name'] + ' was successfully listed!')

    # called upon submitting the new artist listing form
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion

    # on successful db insert, flash success
    #flash('Artist ' + request.form['name'] + ' was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.

    data = []

    shows = Show.query.all()
    for show in shows:
        data.append({
            'venue_id': show.venue.id,
            'venue_name': show.venue.name,
            'artist_id': show.artist.id,
            'artist_name': show.artist.name,
            'artist_image_link': show.artist.image_link,
            'start_time': str(show.start_time)
        })

    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # TODO: insert form data as a new Show record in the db, instead
    error = False
    try:
        show = Show(
            artist_id=request.form['artist_id'],
            venue_id=request.form['venue_id'],
            start_time=request.form['start_time']
        )
        db.session.add(show)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print('this is an error')
        print("Oops!", sys.exc_info()[0], "occurred.")

    finally:
        db.session.close()
    if error:
        flash('An error occurred. Show ' +
              request.form['artist_id'] + ' could not be listed.')
        abort(400)
    else:
        flash('Show ' + request.form['artist_id'] +
              ' was successfully listed!')

    return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
