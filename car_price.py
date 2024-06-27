import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.preprocessing import LabelEncoder

# Load the dataset
df = pd.read_csv('car.csv')

# Clean and preprocess data
# Rename columns
df = df.rename(columns={'selling_price': 'price'})

# Extracting numeric values from 'max_power' column
df['max_power'] = df['max_power'].str.extract('(\d+)', expand=False).astype(float)

# Handle missing values
mis_values = ["mileage(km/ltr/kg)", "engine", "max_power", "seats"]
for col in mis_values:
    df[col].fillna(df[col].median(), inplace=True)

# Extract 'brand' from 'name'
df["brand"] = df["name"].apply(lambda x: x.split()[0])

# Encode categorical variables
categoricals = ["brand", "fuel", "seller_type", "transmission", "owner"]
le = LabelEncoder()
for col in categoricals:
    df[col] = le.fit_transform(df[col])

# Train Extra Trees model
X = df.drop(columns=["price", "name"], axis=1).values
y = df["price"].values
model = ExtraTreesRegressor()
model.fit(X, y)

# Streamlit app
def main():
    st.title("Car Price Prediction")

    # User input form
    st.header("Enter Car Information")

    brand_options = np.sort(df["brand"].unique())
    brand = st.selectbox("Brand", brand_options)

    year = st.number_input("Year of Manufacture", min_value=int(df["year"].min()), max_value=int(df["year"].max()),
                           value=int(df["year"].median()), step=1)

    km_driven = st.number_input("Kilometers Driven", min_value=int(df["km_driven"].min()),
                                max_value=int(df["km_driven"].max()), value=int(df["km_driven"].median()), step=1000)

    fuel_options = np.sort(df["fuel"].unique())
    fuel = st.selectbox("Fuel Type", fuel_options)

    seller_type_options = np.sort(df["seller_type"].unique())
    seller_type = st.selectbox("Seller Type", seller_type_options)

    transmission_options = np.sort(df["transmission"].unique())
    transmission = st.selectbox("Transmission", transmission_options)

    owner_options = np.sort(df["owner"].unique())
    owner = st.selectbox("Owner Type", owner_options)

    mileage = st.number_input("Mileage (km/ltr/kg)", min_value=float(df["mileage(km/ltr/kg)"].min()),
                              max_value=float(df["mileage(km/ltr/kg)"].max()),
                              value=float(df["mileage(km/ltr/kg)"].median()), step=0.1)

    engine = st.number_input("Engine Capacity", min_value=float(df["engine"].min()),
                             max_value=float(df["engine"].max()), value=float(df["engine"].median()), step=100.0)

    max_power = st.number_input("Maximum Power (HP)", min_value=float(df["max_power"].min()),
                                max_value=float(df["max_power"].max()), value=float(df["max_power"].median()), step=10.0)

    seats_options = np.sort(df["seats"].unique())
    seats = st.selectbox("Number of Seats", seats_options)

    # Predict price on user input
    if st.button("Predict Price"):
        # Encode categorical variables for prediction
        le_brand = le.transform([brand])[0]
        le_fuel = le.transform([fuel])[0]
        le_seller_type = le.transform([seller_type])[0]
        le_transmission = le.transform([transmission])[0]
        le_owner = le.transform([owner])[0]

        # Prepare input data
        input_data = np.array([le_brand, year, km_driven, le_fuel, le_seller_type, le_transmission, le_owner,
                               mileage, engine, max_power, seats]).reshape(1, -1)

        # Predict price
        prediction = model.predict(input_data)
        st.success(f"The estimated price of the car is ₹ {prediction[0]:,.2f}")

if __name__ == "__main__":
    main()
