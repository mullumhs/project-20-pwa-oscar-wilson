from flask import render_template, request, redirect, url_for, flash
from models import db, Element
from sqlalchemy import or_, and_

# Define your routes inside the 'init_routes' function
# Feel free to rename the routes and functions as you see fit
# You may need to use multiple methods such as POST and GET for each route
# You can use render_template or redirect as appropriate
# You can also use flash for displaying status messages

def init_routes(app):

    @app.route('/', methods=['GET'])
    def index(message='Displaying the periodic table', color_view="default"):
        # This route should retrieve all items from the database and display them on the page.
        leftover_elements = Element.query.all() # this will only be used for the elements that arent coloured

        elements = {}
        
        if color_view == "states":
            elements["--color_gas"] = Element.query.filter(Element.boiling_point<298).all()
            elements["--color_liquid"] = Element.query.filter(and_(Element.boiling_point>298 ), (Element.melting_point<298)).all()
            elements["--color_solid"] = Element.query.filter(Element.melting_point>298).all()
        elif color_view == "radioactivity":
            elements["--color_radioactive"] = Element.query.filter(Element.radioactive == True).all()
            elements["--color_non_radioactive"] = Element.query.filter(Element.radioactive == False).all()
        elif color_view == "metallic_classification":
            elements["--color_non_metal"] = Element.query.filter(Element.metal == "non-metal").all()
            elements["--color_semi_metal"] = Element.query.filter(Element.metal == "semi-metal").all()
            elements["--color_metal"] = Element.query.filter(Element.metal == "metal").all()
        elif color_view == "groups":
            elements["--color_alkali_metal"] = Element.query.filter(Element.group == 1).all()
            elements["--color_alkaline_earth_metals"] = Element.query.filter(Element.group == 2).all()
            elements["--color_transition_metals"] = Element.query.filter(or_(Element.group.between(4, 12), and_((Element.period < 6), (Element.group == 3)))).all()
            elements["--color_lanthanides"] = Element.query.filter(or_(Element.atomic_number == 57, and_((Element.group == 0), (Element.period == 6)))).all()
            elements["--color_actinides"] = Element.query.filter(or_(Element.atomic_number == 89, and_((Element.group == 0), (Element.period == 7)))).all()
            elements["--color_triels"] = Element.query.filter(Element.group == 13).all()
            elements["--color_tetrels"] = Element.query.filter(Element.group == 14).all()
            elements["--color_pnictogens"] = Element.query.filter(Element.group == 15).all()
            elements["--color_chalcogens"] = Element.query.filter(Element.group == 16).all()
            elements["--color_halogen"] = Element.query.filter(Element.group == 17).all()
            elements["--color_noble_gas"] = Element.query.filter(Element.group == 18).all()
        else: # This is the default colour view, for element properties
            elements["--color_alkali_metal"] = Element.query.filter(and_(Element.group == 1), (Element.metal == "metal")).all()
            elements["--color_alkaline_earth_metals"] = Element.query.filter(and_(Element.group == 2), (Element.metal == "metal")).all()
            elements["--color_transition_metals"] = Element.query.filter(or_(Element.group.between(4, 12), and_((Element.period < 6), (Element.group == 3)))).all()
            elements["--color_lanthanides"] = Element.query.filter(or_(Element.atomic_number == 57, and_((Element.group == 0), (Element.period == 6)))).all()
            elements["--color_actinides"] = Element.query.filter(or_(Element.atomic_number == 89, and_((Element.group == 0), (Element.period == 7)))).all()
            elements["--color_non_metal"] = Element.query.filter(and_(Element.metal == "non-metal", Element.group != 18)).all()
            elements["--color_semi_metal"] = Element.query.filter(Element.metal == "semi-metal").all()
            elements["--color_post_transition_metal"] = Element.query.filter(and_(Element.metal == "metal", Element.group > 12)).all()
            elements["--color_noble_gas"] = Element.query.filter(and_(Element.group == 18, Element.metal == "non-metal")).all()

        return render_template('index.html', message=message, elements=elements, leftover_elements=leftover_elements, edit_mode=False)
    
    @app.route('/edit', methods=['GET'])
    def edit_mode():
        # This route retrieves all items from the database and displays them on the page, but clicking on the individual items takes you to its update page.
        elements = {"--color_edit_mode":Element.query.all()}
        return render_template('index.html', message='Edit mode: click on an element to update it.', elements=elements, leftover_elements=Element.query.all(), edit_mode=True)
    
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

            if request.form['radioactive'] == 'radioactive':
                radioactive = True
            else:
                radioactive = False

            try:
                most_stable_isotope = int(request.form['most_stable_isotope_found'])
            except:
                most_stable_isotope = None

            if request.form['most_stable_halflife_found'] == None or len(request.form['most_stable_halflife_found'].strip()) == 0:
                most_stable_halflife = None
            else:
                most_stable_halflife = request.form['most_stable_halflife_found'].strip()

            new_element = Element(
                name = request.form['name'].strip().capitalize(),
                symbol = request.form['symbol'].strip().capitalize(),
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
                most_stable_halflife_found = most_stable_halflife
            )
            db.session.add(new_element)
            db.session.commit()
            return index(message='Element added successfully')
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

            if request.form['radioactive'] == "radioactive":
                radioactive = True
            else:
                radioactive = False

            try:
                most_stable_isotope = int(request.form['most_stable_isotope_found'])
            except:
                most_stable_isotope = None

            if request.form['most_stable_halflife_found'] == None or len(request.form['most_stable_halflife_found'].strip()) == 0:
                most_stable_halflife = None
            else:
                most_stable_halflife = request.form['most_stable_halflife_found'].strip()

            element.name = request.form['name'].strip().capitalize()
            element.symbol = request.form['symbol'].strip().capitalize()
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
            element.most_stable_halflife_found = most_stable_halflife
        
            db.session.commit()
            return index(message='Element updated successfully')
        return render_template('write.html', element=element)



    @app.route('/delete', methods=['GET', 'POST'])
    def delete_element():
        if request.method == "POST":
            id=int(request.form['id'])
            element = Element.query.get_or_404(id)
            db.session.delete(element)
            db.session.commit()
            return index(message=f'Element deleted successfully')
        elements = Element.query.all()
        return render_template('delete.html', elements=elements)
    

    @app.route('/search', methods=['POST'])
    def search():
        try:
            float(request.form["search"].strip())
            is_number = True
        except:
            is_number = False

        results={}

        if is_number:
            search_query=float(request.form["search"].strip())
            results["Atomic Number"] = Element.query.filter(Element.atomic_number.between(search_query*0.67, search_query*1.5)).order_by(Element.atomic_number.asc()).all()
            results["Atomic Weight"] = Element.query.filter(Element.atomic_weight.between(search_query*0.67, search_query*1.5)).order_by(Element.atomic_number.asc()).all()
            results["Group"] = Element.query.filter(Element.group.between(search_query*0.67, search_query*1.5)).order_by(Element.atomic_number.asc()).all()
            results["Period"] = Element.query.filter(Element.period.between(search_query*0.67, search_query*1.5)).order_by(Element.atomic_number.asc()).all()
            results["Boiling Point"] = Element.query.filter(Element.boiling_point.between(search_query*0.67, search_query*1.5)).order_by(Element.atomic_number.asc()).all()
            results["Melting Point"] = Element.query.filter(Element.melting_point.between(search_query*0.67, search_query*1.5)).order_by(Element.atomic_number.asc()).all()
            results["Most Stable Isotope"] = Element.query.filter(Element.most_stable_isotope_found.between(search_query*0.67, search_query*1.5)).order_by(Element.atomic_number.asc()).all()
        else:
            search_query="%"+request.form["search"].strip()+"%"
            results["Element Name"] = Element.query.filter(Element.name.ilike(search_query)).order_by(Element.atomic_number.asc()).all()
            results["Element Symbol"] = Element.query.filter(Element.symbol.ilike(search_query)).order_by(Element.atomic_number.asc()).all()
            results["Metallic Classification"] = Element.query.filter(Element.metal.ilike(search_query)).order_by(Element.atomic_number.asc()).all()
            if search_query == "%"+"radioactive"+"%":
                results["Radioactivity"] = Element.query.filter(Element.radioactive == True).order_by(Element.atomic_number.asc()).all()

        sorting_key_A = lambda key: -len(results[key])
        results_order = [key for key in results]

        results_order.sort(key=sorting_key_A) # used so that the 'most relevant' section comes first (more results = more likely to be what the user wanted, right???))
        
        try:
            results_order.remove("Element Symbol")
            results_order.insert(0, "Element Symbol") # if there are results for this, that probably means they are the most relevant, so they are forced to the front
        except:
            pass

        results_order.append("Help")

        return render_template('search.html', results=results, results_order=results_order)