from market import app
from flask import render_template, redirect, url_for, flash, get_flashed_messages, request
from market.models import Item, User
from market.forms import RegisterForm, LoginForm, ComprarProducto, VenderProducto
from market import db
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/a')
def hello_world():
    return '<h1>Hello, World Hugouno1!</h1>'

@app.route('/about/<username>')
def about_page(username):
    return f'<h1><strong>this is the about page of {username}</strong></h1>'

@app.route('/')
@app.route('/home')
def index_page():
    return render_template('index.html')

@app.route('/market', methods=['GET','POST'])
@login_required
def market_page():
    compra_form = ComprarProducto()
    ventas_form = VenderProducto()
    if request.method == "POST":
        #Logica de compra
        nombre_producto = request.form.get('nombre_producto')
        p_item_object = Item.query.filter_by(name=nombre_producto).first()
        if p_item_object:
            if current_user.puede_pagar(p_item_object):
                p_item_object.comprar(current_user)
                flash(f"Compraste: {p_item_object.name} con precio de {p_item_object.price}", category='success')
            else:
                flash(f"Lastimosamente, no tiene el dinero suficiente para comprar {p_item_object.name}", category='danger')
        #Logica de venta
        producto_vendido = request.form.get('nombre_producto_vendido')
        s_item_object = Item.query.filter_by(name=producto_vendido).first()
        if s_item_object:
            if current_user.puede_vender(s_item_object):
                s_item_object.vender(current_user)
                flash(f"Vendiste: {s_item_object.name} con precio de {s_item_object.price}", category='success')
            else:
                flash(f"Lastimosamente, no se pudo vender: {p_item_object.name}", category='danger')
        return redirect(url_for('market_page'))


    if request.method == "GET":
        items = Item.query.filter_by(owner=None)
        owened_item = Item.query.filter_by(owner=current_user.id)
        return render_template('market.html', item_name = items, compra_form=compra_form, ventas_form=ventas_form, owened_items=owened_item)

    #if compra_form.validate_on_submit():
        #print(request.form)
        #print(request.form.get('nombre_producto')) #atributo especifico
    #items = Item.query.all()  #esto sirve para obtener todos los registros de la base de datos de dicho modelo
    #items = [
        #{'id':1,'name':'Phone','barcode':'3212312321','price':200},
        #{'id':2,'name':'TV','barcode':'321268321','price':400},
        #{'id':3,'name':'Key','barcode':'3280892821','price':600}
    #]
    

@app.route('/register', methods=['GET','POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit(): #condicional cuando se envia el form
        user_to_create = User(username=form.username.data,
        email_address=form.email_address.data,
        password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Cuenta creada correctamente, Bienvenido: {user_to_create.username}', category='success')
        return redirect(url_for('market_page'))

    if form.errors != {}: #si no hay error de validacion
        for err_msg in form.errors.values():
            flash(f'Hay un error al crear el usuario: {err_msg}', category='danger')

    return render_template('register.html',form=form)

@app.route('/login', methods=['GET','POST'])
def login_page():
    form = LoginForm()

    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Logueado correctamente: {attempted_user.username}', category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Username y contraseña no son correctas. Intenta nuevamente', category='danger')
    return render_template('login.html',form=form)

@app.route('/logout', methods=['GET','POST'])
def logout_page():
    logout_user()
    flash("Has cerrado sesión", category='info')
    return redirect(url_for('index_page'))