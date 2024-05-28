import os

import keras
import pandas as pd
from keras._tf_keras.keras.layers import Dense
from keras._tf_keras.keras.models import Sequential
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

import Actual_Model as am


def create_model():
    # Sprawdź, czy istnieje plik modelu Keras SavedModel
    if os.path.exists("my_model.keras"):
        print("File Exist")
        model_path = "my_model.keras"
        # Plik istnieje, wczytaj model
        model = keras.models.load_model(model_path)
        print("Create new parameters")
        file = "CO2_Emissions_Canada.csv"
        df = pd.read_csv(file)
        # Wybór cech i etykiety
        df_x = df.drop(columns=["Make", "Model", "Vehicle Class", "CO2 Emissions(g/km)", "Fuel Consumption Comb (mpg)"])

        # Przekształcenie zmiennych kategorycznych
        df_transmission = pd.get_dummies(df_x["Transmission"])
        df_fuel_type = pd.get_dummies(df_x["Fuel Type"])

        # Łączenie przekształconych danych z danymi oryginalnymi
        X = pd.concat([df_x, df_transmission, df_fuel_type], axis=1)

        # Usunięcie kolumn, które zostały przekształcone za pomocą get_dummies, aby uniknąć nadmiernego duplikowania danych
        X = X.drop(columns=["Transmission", "Fuel Type"])
        Y = df["CO2 Emissions(g/km)"]
        # Obsługa Kolumny Transmission, ktora jest Stringiem!
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=.2)
        # Skalowanie
        am.sc = StandardScaler()
        X_train = am.sc.fit_transform(X_train)
        X_test = am.sc.transform(X_test)
    else:
        print("Create new model")
        file = "CO2_Emissions_Canada.csv"
        df = pd.read_csv(file)
        # Wybór cech i etykiety
        df_x = df.drop(columns=["Make", "Model", "Vehicle Class", "CO2 Emissions(g/km)", "Fuel Consumption Comb (mpg)"])

        # Przekształcenie zmiennych kategorycznych
        df_transmission = pd.get_dummies(df_x["Transmission"])
        df_fuel_type = pd.get_dummies(df_x["Fuel Type"])

        # Łączenie przekształconych danych z danymi oryginalnymi
        X = pd.concat([df_x, df_transmission, df_fuel_type], axis=1)

        # Usunięcie kolumn, które zostały przekształcone za pomocą get_dummies, aby uniknąć nadmiernego duplikowania danych
        X = X.drop(columns=["Transmission", "Fuel Type"])
        Y = df["CO2 Emissions(g/km)"]
        # Obsługa Kolumny Transmission, ktora jest Stringiem!
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=.2)
        # Skalowanie
        am.sc = StandardScaler()
        X_train = am.sc.fit_transform(X_train)
        X_test = am.sc.transform(X_test)
        # Create model
        model = Sequential()
        model.add(Dense(units=32, activation='relu', input_dim=X_train.shape[1]))
        model.add(Dense(units=64, activation='relu'))
        model.add(Dense(units=1, activation='linear'))
        model.compile(loss='mean_squared_logarithmic_error', optimizer='adam')
        model.fit(X_train, Y_train, epochs=200, batch_size=32)
        # Save the model
        model.save("my_model.keras")

    am.model = model
    am.X_test = X_test
    am.Y_test = Y_test


def update_model():
    model_path = 'my_model.keras'
    if os.path.exists(model_path):
        os.remove(model_path)
        print(f"Plik {model_path} został usunięty.")
    else:
        print(f"Plik {model_path} nie istnieje.")
    create_model()


def preprocess_input(input_data):
    # Tworzenie DataFrame'a z danymi wejściowymi
    input_df = pd.DataFrame([input_data])

    # Przekształcenie zmiennych kategorycznych
    input_transmission = pd.get_dummies(input_df["Transmission"])
    input_fuel_type = pd.get_dummies(input_df["Fuel Type"])

    # Łączenie przekształconych danych z danymi oryginalnymi
    input_df = pd.concat([input_df.drop(columns=["Transmission", "Fuel Type"]), input_transmission, input_fuel_type], axis=1)

    # Uzyskanie listy kolumn użytych podczas treningu modelu
    columns_used_during_training = [
        'Engine Size(L)', 'Cylinders', 'Fuel Consumption City (L/100 km)', 'Fuel Consumption Hwy (L/100 km)', 'Fuel Consumption Comb (L/100 km)',
        'A10', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'AM5', 'AM6', 'AM7', 'AM8', 'AM9', 'AS10', 'AS4', 'AS5', 'AS6', 'AS7', 'AS8', 'AS9',
        'AV', 'AV10', 'AV6', 'AV7', 'AV8', 'M5', 'M6', 'M7', 'D', 'E', 'N', 'X', 'Z'
    ]

    # Dodaj brakujące kolumny z wartościami domyślnymi (zerami)
    for col in columns_used_during_training:
        if col not in input_df.columns:
            input_df[col] = 0

    # Upewnij się, że kolumny są w tej samej kolejności co podczas treningu modelu
    input_df = input_df[columns_used_during_training]

    # Skalowanie danych
    input_df_scaled = am.sc.transform(input_df)

    return input_df_scaled