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

        if request.args.get('message') != None:
            message=request.args.get('message')
        
        if request.args.get('color_view') != None:
            color_view=request.args.get('color_view')

        leftover_elements = Element.query.all() # this will only be used for the elements that arent coloured

        elements = {}
        
        if color_view == "states":
            elements["--color_gas"] = Element.query.filter(Element.boiling_point<298).all()
            elements["--color_liquid"] = Element.query.filter(and_(Element.boiling_point>298 ), (Element.melting_point<298)).all()
            elements["--color_solid"] = Element.query.filter(or_(Element.melting_point>298, or_(Element.atomic_number==6, Element.atomic_number==33), Element.atomic_number.between(105, 111), Element.atomic_number==114)).all()
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
            elements["--color_lanthanides"] = Element.query.filter( or_(or_(Element.atomic_number == 57, Element.atomic_number == 71), and_((Element.group == 0), (Element.period == 6))) ).all()
            elements["--color_actinides"] = Element.query.filter( or_(or_(Element.atomic_number == 89, Element.atomic_number == 103), and_((Element.group == 0), (Element.period == 7))) ).all()
            elements["--color_triels"] = Element.query.filter(Element.group == 13).all()
            elements["--color_tetrels"] = Element.query.filter(Element.group == 14).all()
            elements["--color_pnictogens"] = Element.query.filter(Element.group == 15).all()
            elements["--color_chalcogens"] = Element.query.filter(Element.group == 16).all()
            elements["--color_halogen"] = Element.query.filter(Element.group == 17).all()
            elements["--color_noble_gas"] = Element.query.filter(Element.group == 18).all()
        else: # This is the default colour view, for element properties
            elements["--color_alkali_metal"] = Element.query.filter(and_(Element.group == 1), (Element.metal == "metal")).all()
            elements["--color_alkaline_earth_metals"] = Element.query.filter(and_(Element.group == 2), (Element.metal == "metal")).all()
            elements["--color_transition_metals"] = Element.query.filter( and_(Element.metal == 'metal', or_(Element.group.between(4, 12), and_((Element.period < 6), (Element.group == 3)))) ).all()
            elements["--color_lanthanides"] = Element.query.filter( or_(or_(Element.atomic_number == 57, Element.atomic_number == 71), and_((Element.group == 0), (Element.period == 6))) ).all()
            elements["--color_actinides"] = Element.query.filter( or_(or_(Element.atomic_number == 89, Element.atomic_number == 103), and_((Element.group == 0), (Element.period == 7))) ).all()
            elements["--color_non_metal"] = Element.query.filter(and_(Element.metal == "non-metal", Element.group != 18)).all()
            elements["--color_semi_metal"] = Element.query.filter(Element.metal == "semi-metal").all()
            elements["--color_post_transition_metals"] = Element.query.filter(and_(Element.metal == "metal", Element.group > 12)).all()
            elements["--color_noble_gas"] = Element.query.filter(and_(Element.group == 18, Element.metal == "non-metal")).all()

        return render_template('index.html', message=message, elements=elements, leftover_elements=leftover_elements, edit_mode=False, color_view=color_view)
    
    @app.route('/edit', methods=['GET'])
    def edit_mode():
        # This route retrieves all items from the database and displays them on the page, but clicking on the individual items takes you to its update page.
        elements = {"--color_edit_mode":Element.query.all()}
        return render_template('index.html', message='Edit mode: click on an element to update it.', elements=elements, leftover_elements=Element.query.all(), edit_mode=True)
    
    @app.route('/element/<int:id>', methods=['GET'])
    def element_view(id):
        # This route retrieves an items from the database and displays it on the page.
        element = Element.query.get_or_404(id)

        # Retrieve a colour -- note db.session.query(Element.id)... returns a list of tuples that look like (id,) which is why I'm looking for (id,) instead of id
        if (id,) in db.session.query(Element.id).filter(and_(Element.group == 1), (Element.metal == "metal")).all():
            color = "--color_alkali_metal"
        elif (id,) in db.session.query(Element.id).filter(and_(Element.group == 2), (Element.metal == "metal")).all():
            color = "--color_alkaline_earth_metals"
        elif (id,) in db.session.query(Element.id).filter( and_(Element.metal == 'metal', or_(Element.group.between(4, 12), and_((Element.period < 6), (Element.group == 3)))) ).all():
            color = "--color_transition_metals"
        elif (id,) in db.session.query(Element.id).filter( or_(or_(Element.atomic_number == 57, Element.atomic_number == 71), and_((Element.group == 0), (Element.period == 6))) ).all():
            color = "--color_lanthanides"
        elif (id,) in db.session.query(Element.id).filter( or_(or_(Element.atomic_number == 89, Element.atomic_number == 103), and_((Element.group == 0), (Element.period == 7))) ).all():
            color = "--color_actinides"
        elif (id,) in db.session.query(Element.id).filter(and_(Element.metal == "non-metal", Element.group != 18)).all():
            color = "--color_non_metal"
        elif (id,) in db.session.query(Element.id).filter(Element.metal == "semi-metal").all():
            color = "--color_semi_metal"
        elif (id,) in db.session.query(Element.id).filter(and_(Element.metal == "metal", Element.group > 12)).all():
            color = "--color_post_transition_metals"
        elif (id,) in db.session.query(Element.id).filter(and_(Element.group == 18, Element.metal == "non-metal")).all():
            color = "--color_noble_gas"
        else:
            color = "--color_unsure"

        return render_template('element.html', element=element, color=color)


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
            return redirect(url_for('index',message='Element added successfully'))
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
            return redirect(url_for('index', message='Element updated successfully'))
        return render_template('write.html', element=element)



    @app.route('/delete', methods=['GET', 'POST'])
    def delete_element():
        if request.method == "POST":
            id=int(request.form['id'])
            element = Element.query.get_or_404(id)
            db.session.delete(element)
            db.session.commit()
            return redirect(url_for('index', message='Element deleted successfully'))
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
    
    @app.route('/resetelements', methods=['GET'])
    def reset_elements():
        # This dictionary isn't the best practice, but it was the most convenient to make
        periodic_dict = {
            'name':['Hydrogen', 'Helium', 'Lithium', 'Beryllium', 'Boron', 'Carbon', 'Nitrogen', 'Oxygen', 'Fluorine', 'Neon', 'Sodium', 'Magnesium', 'Aluminium', 'Silicon', 'Phosphorus', 'Sulfur', 'Chlorine', 'Argon', 'Potassium', 'Calcium', 'Scandium', 'Titanium', 'Vanadium', 'Chromium', 'Manganese', 'Iron', 'Cobalt', 'Nickel', 'Copper', 'Zinc', 'Gallium', 'Germanium', 'Arsenic', 'Selenium', 'Bromine', 'Krypton', 'Rubidium', 'Strontium', 'Yttrium', 'Zirconium', 'Niobium', 'Molybdenum', 'Technetium', 'Ruthenium', 'Rhodium', 'Palladium', 'Silver', 'Cadmium', 'Indium', 'Tin', 'Antimony', 'Tellurium', 'Iodine', 'Xenon', 'Caesium', 'Barium', 'Lanthanum', 'Cerium', 'Praseodymium', 'Neodymium', 'Promethium', 'Samarium', 'Europium', 'Gadolinium', 'Terbium', 'Dysprosium', 'Holmium', 'Erbium', 'Thulium', 'Ytterbium', 'Lutetium', 'Hafnium', 'Tantalum', 'Tungsten', 'Rhenium', 'Osmium', 'Iridium', 'Platinum', 'Gold', 'Mercury', 'Thallium', 'Lead', 'Bismuth', 'Polonium', 'Astatine', 'Radon', 'Francium', 'Radium', 'Actinium', 'Thorium', 'Protactinium', 'Uranium', 'Neptunium', 'Plutonium', 'Americium', 'Curium', 'Berkelium', 'Californium', 'Einsteinium', 'Fermium', 'Mendelevium', 'Nobelium', 'Lawrencium', 'Rutherfordium', 'Dubnium', 'Seaborgium', 'Bohrium', 'Hassium', 'Meitnerium', 'Darmstadtium', 'Roentgenium', 'Copernicium', 'Nihonium', 'Flerovium', 'Moscovium', 'Livermorium', 'Tennessine', 'Oganesson'],
            'symbol':['H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne', 'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar', 'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr', 'Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te', 'I', 'Xe', 'Cs', 'Ba', 'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn', 'Fr', 'Ra', 'Ac', 'Th', 'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm', 'Md', 'No', 'Lr', 'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt', 'Ds', 'Rg', 'Cn', 'Nh', 'Fl', 'Mc', 'Lv', 'Ts', 'Og'],
            'atomic_number':['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59', '60', '61', '62', '63', '64', '65', '66', '67', '68', '69', '70', '71', '72', '73', '74', '75', '76', '77', '78', '79', '80', '81', '82', '83', '84', '85', '86', '87', '88', '89', '90', '91', '92', '93', '94', '95', '96', '97', '98', '99', '100', '101', '102', '103', '104', '105', '106', '107', '108', '109', '110', '111', '112', '113', '114', '115', '116', '117', '118'],
            'atomic_weight':['1.008', '4.0026', '6.94', '9.0122', '10.81', '12.011', '14.007', '15.999', '18.998', '20.18', '22.99', '24.305', '26.982', '28.085', '30.974', '32.06', '35.45', '39.95', '39.098', '40.078', '44.956', '47.867', '50.942', '51.996', '54.938', '55.845', '58.933', '58.693', '63.546', '65.38', '69.723', '72.63', '74.922', '78.971', '79.904', '83.798', '85.468', '87.62', '88.906', '91.224', '92.906', '95.95', '97', '101.07', '102.91', '106.42', '107.87', '112.41', '114.82', '118.71', '121.76', '127.6', '126.9', '131.29', '132.91', '137.33', '138.91', '140.12', '140.91', '144.24', '145', '150.36', '151.96', '157.25', '158.93', '162.5', '164.93', '167.26', '168.93', '173.05', '174.97', '178.49', '180.95', '183.84', '186.21', '190.23', '192.22', '195.08', '196.97', '200.59', '204.38', '207.2', '208.98', '209', '210', '222', '223', '226', '227', '232.04', '231.04', '238.03', '237', '244', '243', '247', '247', '251', '252', '257', '258', '259', '266', '267', '268', '267', '270', '271', '278', '281', '282', '285', '286', '289', '290', '293', '294', '294'],
            'group':['1', '18', '1', '2', '13', '14', '15', '16', '17', '18', '1', '2', '13', '14', '15', '16', '17', '18', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '1', '2', '3', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '1', '2', '3', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18'],
            'period':['1', '1', '2', '2', '2', '2', '2', '2', '2', '2', '3', '3', '3', '3', '3', '3', '3', '3', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '5', '5', '5', '5', '5', '5', '5', '5', '5', '5', '5', '5', '5', '5', '5', '5', '5', '5', '6', '6', '6', '6', '6', '6', '6', '6', '6', '6', '6', '6', '6', '6', '6', '6', '6', '6', '6', '6', '6', '6', '6', '6', '6', '6', '6', '6', '6', '6', '6', '6', '7', '7', '7', '7', '7', '7', '7', '7', '7', '7', '7', '7', '7', '7', '7', '7', '7', '7', '7', '7', '7', '7', '7', '7', '7', '7', '7', '7', '7', '7', '7', '7'],
            'x_coord':['1', '18', '1', '2', '13', '14', '15', '16', '17', '18', '1', '2', '13', '14', '15', '16', '17', '18', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18'],
            'y_coord':['1', '1', '2', '2', '2', '2', '2', '2', '2', '2', '3', '3', '3', '3', '3', '3', '3', '3', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '5', '5', '5', '5', '5', '5', '5', '5', '5', '5', '5', '5', '5', '5', '5', '5', '5', '5', '6', '6', '6', '9', '9', '9', '9', '9', '9', '9', '9', '9', '9', '9', '9', '9', '9', '6', '6', '6', '6', '6', '6', '6', '6', '6', '6', '6', '6', '6', '6', '6', '7', '7', '7', '10', '10', '10', '10', '10', '10', '10', '10', '10', '10', '10', '10', '10', '10', '7', '7', '7', '7', '7', '7', '7', '7', '7', '7', '7', '7', '7', '7', '7'],
            'metal':['non-metal', 'non-metal', 'metal', 'metal', 'semi-metal', 'non-metal', 'non-metal', 'non-metal', 'non-metal', 'non-metal', 'metal', 'metal', 'metal', 'semi-metal', 'non-metal', 'non-metal', 'non-metal', 'non-metal', 'metal', 'metal', 'metal', 'metal', 'metal', 'metal', 'metal', 'metal', 'metal', 'metal', 'metal', 'metal', 'metal', 'semi-metal', 'semi-metal', 'non-metal', 'non-metal', 'non-metal', 'metal', 'metal', 'metal', 'metal', 'metal', 'metal', 'metal', 'metal', 'metal', 'metal', 'metal', 'metal', 'metal', 'metal', 'semi-metal', 'semi-metal', 'non-metal', 'non-metal', 'metal', 'metal', 'metal', 'metal', 'metal', 'metal', 'metal', 'metal', 'metal', 'metal', 'metal', 'metal', 'metal', 'metal', 'metal', 'metal', 'metal', 'metal', 'metal', 'metal', 'metal', 'metal', 'metal', 'metal', 'metal', 'metal', 'metal', 'metal', 'metal', 'metal', 'metal', 'non-metal', 'metal', 'metal', 'metal', 'metal', 'metal', 'metal', 'metal', 'metal', 'metal', 'metal', 'metal', 'metal', 'metal', 'metal', 'metal', 'metal', 'metal', 'metal', 'metal', 'metal', 'metal', 'metal', 'unsure', 'unsure', 'unsure', 'unsure', 'unsure', 'unsure', 'unsure', 'unsure', 'unsure', 'unsure'],
            'melting_point':['14.01', 'none', '453.69', '1560', '2349', 'none', '63.15', '54.36', '53.53', '24.56', '370.87', '923', '933.47', '1687', '317.3', '388.36', '171.6', '83.8', '336.53', '1115', '1814', '1941', '2183', '2180', '1519', '1811', '1768', '1728', '1357.77', '692.88', '302.9146', '1211.4', 'none', '453', '265.8', '115.79', '312.46', '1050', '1799', '2128', '2750', '2896', '2430', '2607', '2237', '1828.05', '1234.93', '594.22', '429.75', '505.08', '903.78', '722.66', '386.85', '161.4', '301.59', '1000', '1193', '1068', '1208', '1297', '1315', '1345', '1099', '1585', '1629', '1680', '1734', '1802', '1818', '1097', '1925', '2506', '3290', '3695', '3459', '3306', '2719', '2041.4', '1337.33', '234.43', '577', '600.61', '544.7', '527', '575', '202', '300', '973', '1323', '2115', '1841', '1405.3', '917', '912.5', '1449', '1613', '1259', '1173', '1133', '1125', '1100', '1100', '1900', '2400', 'none', 'none', 'none', 'none', 'none', 'none', 'none', '283', '700', '284', '700', '700', '700', '325'],
            'boiling_point':['20.28', '4.22', '1560', '2742', '4200', '3825', '77.36', '90.2', '85.03', '27.07', '1156', '1363', '2792', '3538', '550', '717.87', '239.11', '87.3', '1032', '1757', '3109', '3560', '3680', '2944', '2334', '3134', '3200', '3186', '2835', '1180', '2673', '3106', '887', '958', '332', '119.93', '961', '1655', '3609', '4682', '5017', '4912', '4538', '4423', '3968', '3236', '2435', '1040', '2345', '2875', '1860', '1261', '457.4', '165.03', '944', '2170', '3737', '3716', '3793', '3347', '3273', '2067', '1802', '3546', '3503', '2840', '2993', '3141', '2223', '1469', '3675', '4876', '5731', '6203', '5869', '5285', '4701', '4098', '3129', '629.88', '1746', '2022', '1837', '1235', '610', '211.3', '890', '2010', '3471', '5061', '4300', '4404', '4273', '3501', '2880', '3383', '2900', '1743', '1269', 'none', 'none', 'none', 'none', '5800', 'none', 'none', 'none', 'none', 'none', 'none', 'none', '340', '1400', 'none', '1400', '1100', '883', '450'],
            'radioactive':['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
            'most_stable_isotope_found':['none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', '97', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', '145', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', '209', '209', '210', '222', '223', '226', '227', '232', '231', '238', '237', '244', '243', '247', '247', '251', '252', '257', '258', '259', '266', '267', '268', '269', '270', '271', '278', '282', '282', '285', '286', '289', '290', '293', '294', '294'],
            'most_stable_halflife_found':['none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', '4.21±0.16 million years', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', '17.7 years', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', '20 quintillion years', '102 to 125 years', '8.1 to 8.3 hours', '3.82 days', '22 minutes', '1600 years', '21.77 years', '14.0 billion years', '17.4 days', '4.5 billion years', '2.14 million years', '80 to 82 million years', '7360 years', '15.6 million years', '1380 years', '898 years', '471.7 days', '100.5 days', '51.6 days', '58 minutes', '11 hours', '48 to 78 minutes', '16 to 32 hours', '13 minutes', '2.4 minutes', '46 seconds', '4.5 to 8 seconds', '14 seconds', '130 seconds', '30 seconds', '10 to 20 seconds', '2.1 seconds', '0.65 seconds', '50 to 80 milliseconds', '78 to 80 milliseconds', '0.7 milliseconds'],
            }
        
        # Check if none of the data in trhe dictionary has been deleted
        checkywecky = [len(periodic_dict[key]) for key in periodic_dict]
        if checkywecky.count(checkywecky[0]) == len(checkywecky):
            # If so, clear the database
            db.session.query(Element).delete()
            db.session.commit()
        else:
            raise Exception
        
        # Add every element
        for n in range(checkywecky[0]):
            try:
                mp = float(periodic_dict['melting_point'][n])
            except:
                mp = None

            try:
                bp = float(periodic_dict['boiling_point'][n])
            except:
                bp = None

            if periodic_dict['radioactive'][n] == '1':
                radioactive = True
            else:
                radioactive = False

            try:
                most_stable_isotope = int(periodic_dict['most_stable_isotope_found'][n])
            except:
                most_stable_isotope = None

            if periodic_dict['most_stable_halflife_found'][n] == 'none':
                most_stable_halflife = None
            else:
                most_stable_halflife = periodic_dict['most_stable_halflife_found'][n].strip()

            new_element = Element(
                name = periodic_dict['name'][n].strip().capitalize(),
                symbol = periodic_dict['symbol'][n].strip().capitalize(),
                atomic_number = int(periodic_dict['atomic_number'][n]),
                atomic_weight = float(periodic_dict['atomic_weight'][n]),
                group = int(periodic_dict['group'][n]),
                period = int(periodic_dict['period'][n]),
                x_coord = int(periodic_dict['x_coord'][n]),
                y_coord = int(periodic_dict['y_coord'][n]),
                metal = periodic_dict['metal'][n],
                melting_point = mp,
                boiling_point = bp,
                radioactive = radioactive,
                most_stable_isotope_found = most_stable_isotope,
                most_stable_halflife_found = most_stable_halflife
            )
            db.session.add(new_element)
            db.session.commit()
        
        # Finish
        return redirect(url_for('index', message='Periodic table successfully reset.'))