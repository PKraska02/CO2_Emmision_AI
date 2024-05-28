import keras
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from keras._tf_keras.keras.models import Sequential
from keras._tf_keras.keras.layers import Dense
import os
import GUI as gui
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
        sc = StandardScaler()
        X_train = sc.fit_transform(X_train)
        X_test = sc.transform(X_test)
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
        sc = StandardScaler()
        X_train = sc.fit_transform(X_train)
        X_test = sc.transform(X_test)
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
