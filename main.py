import os
from flask import Flask, render_template, request, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from datetime import datetime

# TODO add dimensions
# TODO add sessions / user identification
# TODO add admin accounts
# TODO add possibility to show/hide coordinates
# TODO display current server seed
# !BUG entry will go in even if one entry of coordinates is empty:
# !BUG str will result as "int int '' "
# !BUG same thing happens if name is empty

#? maybe keep single coordinate (y_coord) omission a feature?

# get working directory
_cwd = os.getcwd()

# declaring variables used to config Flask app instance
SECRET_KEY = os.urandom(24).hex()
WTF_CSRF_SECRET_KEY = 'other-key'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_cwd, 'coords.db')
SQALCHEMY_ECHO = True

# specify folder paths for templates and static files
app = Flask(__name__, template_folder='templates', static_folder='static')
app.debug = True

app.config.from_object(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Coordinate:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def returnAsString(self):
        if (self.x != None and self.y != None and self.z != None ):
            return self.x + ' ' + self.y + ' ' + self.z


# passing an object when declaring a model simply means that
# the created class is a sub-class of the class between parenthesis
class Coordinates(db.Model):
    __tablename__ = 'coords_table'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    coords = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(2048), nullable=False, unique=True)

    # allows you to give each object 
    # a string representation to recognize it for debugging purposes.
    def __repr__(self):
        return f"Coordinates : {self.coords}, Description: {self.description}"


with app.app_context():
    db.create_all()


@app.route('/reset')
def resetDB():
    db.drop_all()

    return redirect(url_for('index'))   

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/enter_coordinates', methods = ['GET', 'POST'])
def showForm():
    return render_template('create.html')

   
@app.route('/submit_coordinates', methods=['GET','POST'])
def submitForm():
    loc_name = request.form.get('coords-info')
    
    x_coord = request.form.get('coord-x')
    y_coord = request.form.get('coord-y')
    z_coord = request.form.get('coord-z')

    dim = request.form.get('dim')

    # check if coords have been inserted, skip if any of them is not correct
    coords = Coordinate(x_coord, y_coord, z_coord)
    curr_date = datetime.now()
    if(coords.returnAsString().isspace() == False and loc_name.isspace() == False):
        entry = Coordinates(coords=str(coords.returnAsString()), date=curr_date, description=str(loc_name))
        db.session.add(entry)

        try:
            db.session.commit()
        except IntegrityError:
            print("Error!")
            flash("Entry failed! It probably exists in database already!", 'error')
            db.session.rollback()
    else:
        print("Error!")
        flash("Entry not inserted! Check if values are not null!", 'error')

    return render_template('create.html')

# TODO check if table exists before getting coord_list
@app.route('/coord-list')
def showList():
    coord_list = Coordinates.query.all()
    if (not coord_list):
        flash('Empty list!', 'error')

    return render_template('list.html', coordinate_list = coord_list)

@app.route('/coord-list/delete/', methods=['GET', 'POST'])
def deleteEntry():
    ID_to_remove = request.form.get('clicked_btn')
    Coordinates.query.filter_by(id=ID_to_remove).delete()
    
    try:
        db.session.commit()
    except IntegrityError:
        print("Error!")
        flash("Deletion failed!")
        db.session.rollback()
    else:
        print("Error!")
        flash("Deletion failed!")

    return redirect(url_for(('showList')))

if __name__ == '__main__':
    app.run()