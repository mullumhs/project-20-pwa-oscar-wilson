from flask import render_template, request, redirect, url_for, flash
from models import db, Element

# Define your routes inside the 'init_routes' function
# Feel free to rename the routes and functions as you see fit
# You may need to use multiple methods such as POST and GET for each route
# You can use render_template or redirect as appropriate
# You can also use flash for displaying status messages

def init_routes(app):

    @app.route('/', methods=['GET'])
    def index():
        # This route should retrieve all items from the database and display them on the page.
        elements = Element.query.all()
        return render_template('index.html', message='Displaying all items', elements=elements, edit_mode=False)
    
    @app.route('/edit', methods=['GET'])
    def edit_mode():
        # This route retrieves all items from the database and displays them on the page, but clicking on the individual items takes you to its update page.
        elements = Element.query.all()
        return render_template('index.html', message='Displaying all items (Edit Mode)', elements=elements, edit_mode=True)
    
    @app.route('/element/<int:id>', methods=['GET'])
    def element_view(id):
        # This route retrieves an items from the database and displays it on the page.
        element = Element.query.get_or_404(id)
        return render_template('element.html', element=element)


    @app.route('/add', methods=['GET', 'POST'])
    def add_element():
        # This route should handle adding a new item to the database.
        if request.method == 'POST':
                       
            try:
                mp = float(request.form['melting_point'])
            except:
                mp = None

            try:
                bp = float(request.form['boiling_point'])
            except:
                bp = None

            if request.form['radioactive'] == '0':
                radioactive = False
            else:
                radioactive = True

            try:
                most_stable_isotope = int(request.form['most_stable_isotope_found'])
            except:
                most_stable_isotope = None

            new_element = Element(
                name = request.form['name'],
                symbol = request.form['symbol'],
                atomic_number = int(request.form['atomic_number']),
                atomic_weight = float(request.form['atomic_weight']),
                group = int(request.form['group']),
                period = int(request.form['period']),
                x_coord = int(request.form['x_coord']),
                y_coord = int(request.form['y_coord']),
                metal = request.form['metal'],
                melting_point = mp,
                boiling_point = bp,
                radioactive = radioactive,
                most_stable_isotope_found = most_stable_isotope,
                most_stable_halflife_found = request.form['most_stable_halflife_found']
            )
            db.session.add(new_element)
            db.session.commit()
            return render_template('index.html', message='Item added successfully')
        return render_template('write.html', element=None)



    @app.route('/update/<int:id>', methods=['GET','POST'])
    def update_element(id):
        # This route should handle updating an existing item identified by the given ID.
        element = Element.query.get_or_404(id)
        if request.method == 'POST':
            try:
                mp = float(request.form['melting_point'])
            except:
                mp = None

            try:
                bp = float(request.form['boiling_point'])
            except:
                bp = None

            if request.form['radioactive'] == '0':
                radioactive = False
            else:
                radioactive = True

            try:
                most_stable_isotope = int(request.form['most_stable_isotope_found'])
            except:
                most_stable_isotope = None

            element.name = request.form['name']
            element.symbol = request.form['symbol']
            element.atomic_number = int(request.form["atomic_number"])
            element.atomic_weight = float(request.form["atomic_weight"])
            element.group = int(request.form['group'])
            element.period = int(request.form['period'])
            element.x_coord = int(request.form['x_coord'])
            element.y_coord = int(request.form['y_coord'])
            element.metal = request.form['metal']
            element.melting_point = mp
            element.boiling_point = bp
            element.radioactive = radioactive
            element.most_stable_isotope_found = most_stable_isotope
            element.most_stable_halflife_found = request.form['most_stable_halflife_found']
        
            db.session.commit()
            return render_template('index.html', message=f'Item updated successfully')
        return render_template('write.html', element=element)



    @app.route('/delete', methods=['GET', 'POST'])
    def delete_element():
        if request.method == "POST":
            id=int(request.form['id'])
            element = Element.query.get_or_404(id)
            db.session.delete(element)
            db.session.commit()
            return render_template('index.html', message=f'Item deleted successfully')
        elements = Element.query.all()
        return render_template('delete.html', elements=elements)