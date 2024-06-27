from flask import Flask, render_template, request, jsonify
from flask_cors import CORS,cross_origin
import pickle
import pandas as pd
import numpy as np

app=Flask(__name__)
cors=CORS(app)
model=pickle.load(open('model.pkl','rb'))
car=pd.read_csv('veri.csv')

@app.route('/',methods=['GET','POST'])
def index():
    
    default_year = int(car['year'].median())
    default_km_driven = int(car['km_driven'].median())
    default_mileage = float(car['mileage(km/ltr/kg)'].median())
    default_engine = float(car['engine'].median())
    default_max_power = float(car['max_power'].median())
    default_seats = int(car['seats'].median())
    
    seller_types = car["seller_type"].unique()
    transmissions = car["transmission"].unique()
    fuels = car["fuel"].unique()
    owners = car["owner"].unique()
    brands = car["brand"].unique()

    return render_template('index.html',
                           default_year=default_year,
                           default_km_driven=default_km_driven,
                           default_mileage=default_mileage,
                           default_engine=default_engine,
                           default_max_power=default_max_power,
                           default_seats=default_seats,
                           seller_types=seller_types,
                           transmissions=transmissions,
                           fuels=fuels,
                           owners=owners,
                           brands=brands)


@app.route('/predict',methods=['POST'])
@cross_origin()
def predict():

    year = int(request.form['year'])
    km_driven = int(request.form['km_driven'])
    mileage = float(request.form['mileage'])
    engine = float(request.form['engine'])
    max_power = float(request.form['max_power'])
    seats = int(request.form['seats'])
    seller_type = request.form['seller_type']
    transmission = request.form['transmission']
    fuel = request.form['fuel']
    owner = request.form['owner']
    brand = request.form['brand']

    input_data = pd.DataFrame([[year, km_driven, mileage, engine, max_power, seats, seller_type, transmission, fuel, owner, brand]],
                              columns=['year', 'km_driven', 'mileage(km/ltr/kg)', 'engine', 'max_power', 'seats', 'seller_type', 'transmission', 'fuel', 'owner', 'brand'])

    prediction=model.predict(input_data)

    prediction = model.predict(input_data)

    return jsonify({'price': prediction[0]})



if __name__=='__main__':
    app.run(debug=True)