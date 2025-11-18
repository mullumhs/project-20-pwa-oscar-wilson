from flask import render_template, request, redirect, url_for, flash
from models import db, Element

# Define your routes inside the 'init_routes' function
# Feel free to rename the routes and functions as you see fit
# You may need to use multiple methods such as POST and GET for each route
# You can use render_template or redirect as appropriate
# You can also use flash for displaying status messages

def init_routes(app):

    @app.route('/', methods=['GET'])
    def get_items():
        # This route should retrieve all items from the database and display them on the page.
        elements = Element.query.all()
        return render_template('index.html', message='Displaying all items', elements=elements)



    @app.route('/add', methods=['GET', 'POST'])
    def create_item():
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
                group = int(request.form['group']),
                period = int(request.form['period']),
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
        return render_template('index.html', message='Add?')



    @app.route('/update', methods=['GET','POST'])
    def update_item():
        # This route should handle updating an existing item identified by the given ID.
        if request.method == 'POST':
            id=int(request.form['id'])
            element = Element.query.get_or_404(id)

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
            element.group = int(request.form['group'])
            element.period = int(request.form['period'])
            element.metal = request.form['metal']
            element.melting_point = mp
            element.boiling_point = bp
            element.radioactive = radioactive
            element.most_stable_isotope_found = most_stable_isotope
            element.most_stable_halflife_found = request.form['most_stable_halflife_found']
        
            db.session.commit()
        return render_template('index.html', message=f'Item updated successfully')



    @app.route('/delete', methods=['POST'])
    def delete_item():
        id=int(request.form['id'])
        element = Element.query.get_or_404(id)
        db.session.delete(element)
        db.session.commit()
        return render_template('index.html', message=f'Item deleted successfully')