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
            new_element = Element(
                name=request.form['name'],
                symbol=request.form['symbol'],
                group=request.form['group'],
                period=request.form['period'],
                metal=request.form['metal'],
                melting_point=request.form['melting_point'],
                boiling_point=request.form['boiling_point'],
                radioactive=request.form['radioactive'],
                most_stable_isotope_found=67,#request.form['most_stable_isotope_found'],
                most_stable_halflife_found='69ms'#request.form['most_stable_halflife_found']
            )
            db.session.add(new_element)
            db.session.commit()
            return render_template('index.html', message='Item added successfully')
        return render_template('index.html', message='Add?')



    @app.route('/update', methods=['POST'])
    def update_item():
        # This route should handle updating an existing item identified by the given ID.
        return render_template('index.html', message=f'Item updated successfully')



    @app.route('/delete', methods=['POST'])
    def delete_item():
        # This route should handle deleting an existing item identified by the given ID.
        return render_template('index.html', message=f'Item deleted successfully')