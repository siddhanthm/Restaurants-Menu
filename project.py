from flask import Flask , render_template, request, redirect, url_for , flash , jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
import bleach

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/restaurants/JSON/')
def restaurantsJSON():
    names = session.query(Restaurant).all()
    return jsonify(Restaurants = [i.serialize for i in names])


@app.route('/restaurants/<int:restaurant_id>/JSON/')
def restaurantsmenuJSON(restaurant_id):
    names = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
    return jsonify(MenuItems = [i.serialize for i in names])

@app.route('/restaurants/<int:restaurant_id>/<int:Menu_ID>/JSON/')
def restaurantsmenuitemJSON(restaurant_id, Menu_ID):
    names = session.query(MenuItem).filter_by(restaurant_id = restaurant_id, id = Menu_ID).one()
    return jsonify(MenuItems = names.serialize)

@app.route('/')
@app.route('/restaurants/')
def restaurants():
    res = session.query(Restaurant).all()
    return render_template('restaurants.html', res = res)

@app.route('/restaurants/new/', methods = ['GET', 'POST'])
def newRestaurants():
    if request.method == 'POST':
        newres = Restaurant(name = request.form['name'])
        session.add(newres)
        session.commit()
        flash("Restaurant successfully added!")
        return redirect(url_for('restaurants'))
    else:
        return render_template('newres.html')

@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    res = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
    return render_template('menu.html', items = items, restaurant= res)

 
@app.route('/restaurants/<int:restaurant_id>/delete/', methods = ['GET', 'POST'])
def deleteRestaurants(restaurant_id):
    res = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':
        if res:
            session.delete(res)
            session.commit()
            flash("Restaurant delete")
            return redirect(url_for('restaurants'))

    else:
        return render_template('delres.html', restaurant_id = restaurant_id, restaurant = res)

# Task 1: Create route for newMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/new', methods = ['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'], description=request.form[
                           'description'], price=request.form['price'], course=request.form['course'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        flash("New item successfully created!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitems.html', restaurant_id=restaurant_id)




@app.route('/restaurants/<int:restaurant_id>/<int:Menu_ID>/edit/', methods = ['GET', 'POST'])
def editMenuItem(restaurant_id, Menu_ID):
    editeditem = session.query(MenuItem).filter_by(id = Menu_ID , restaurant_id = restaurant_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editeditem.name = request.form['name']
        if request.form['description']:
            editeditem.description = request.form['description']
        if request.form['price']:
            editeditem.price = request.form['price']
        if request.form['course']:
            editeditem.course = request.form['course']
        session.add(editeditem)
        session.commit()
        flash("Menu editted!")
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else:
        return render_template('editmenuitems.html', restaurant_id = restaurant_id, Menu_ID = Menu_ID, item = editeditem)



@app.route('/restaurants/<int:restaurant_id>/<int:Menu_ID>/delete/', methods = ['GET', 'POST'])
def deleteMenuItem(restaurant_id, Menu_ID):
    deleteitem = session.query(MenuItem).filter_by(id = Menu_ID, restaurant_id = restaurant_id).one()
    if request.method == 'POST':
        if deleteitem:
            session.delete(deleteitem)
            session.commit()
            flash("Item successfully deleted!")
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else:
        return render_template('deletemenuitems.html', restaurant_id = restaurant_id, Menu_ID =Menu_ID, item = deleteitem)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)