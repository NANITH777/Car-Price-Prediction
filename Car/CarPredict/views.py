from django.shortcuts import render
from django.http import JsonResponse
import pickle
import pandas as pd

# Charger le modèle et les données
model = pickle.load(open('CarPredict/model.pkl', 'rb'))
car = pd.read_csv('CarPredict/veri.csv')

def index(request):
    # Calculer les valeurs par défaut et préparer le contexte
    default_year = int(car['year'].median())
    default_km_driven = int(car['km_driven'].median())
    default_mileage = float(car['mileage(km/ltr/kg)'].median())
    default_engine = float(car['engine'].median())
    default_max_power = float(car['max_power'].median())
    default_seats = int(car['seats'].median())

    # Obtenir les valeurs uniques pour les menus déroulants
    seller_types = car["seller_type"].unique()
    transmissions = car["transmission"].unique()
    fuels = car["fuel"].unique()
    owners = car["owner"].unique()
    brands = car["brand"].unique()

    context = {
        'default_year': default_year,
        'default_km_driven': default_km_driven,
        'default_mileage': default_mileage,
        'default_engine': default_engine,
        'default_max_power': default_max_power,
        'default_seats': default_seats,
        'seller_types': seller_types,
        'transmissions': transmissions,
        'fuels': fuels,
        'owners': owners,
        'brands': brands,
    }

    return render(request, "index.html", context)

def predict(request):
    if request.method == 'POST':
        try:
            year = int(request.POST['year'])
            km_driven = int(request.POST['km_driven'])
            mileage = float(request.POST['mileage'])
            engine = float(request.POST['engine'])
            max_power = float(request.POST['max_power'])
            seats = int(request.POST['seats'])
            seller_type = request.POST['seller_type']
            transmission = request.POST['transmission']
            fuel = request.POST['fuel']
            owner = request.POST['owner']
            brand = request.POST['brand']

            input_data = pd.DataFrame([[year, km_driven, mileage, engine, max_power, seats, seller_type, transmission, fuel, owner, brand]],
                                      columns=['year', 'km_driven', 'mileage(km/ltr/kg)', 'engine', 'max_power', 'seats', 'seller_type', 'transmission', 'fuel', 'owner', 'brand'])

            prediction = model.predict(input_data)

            # Retourner le résultat de la prédiction sous forme de JSON
            return JsonResponse({'price': prediction[0]})
        except Exception as e:
            # Gérer les erreurs éventuelles
            print(f"Error during prediction: {e}")
            return JsonResponse({'error': "Enter valid information. Prediction failed. Please try again."})
