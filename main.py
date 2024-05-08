import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

def main():
    file = r"C:\Users\Piotr\source\repos\CO2-Emmision-AI\archive\CO2 Emissions_Canada.csv"
    df = pd.read_csv(file)

    # Wybór cech i etykiety
    X = df.drop(columns=["Make", "Model", "Vehicle Class", "CO2 Emissions(g/km)"])
    y = df["CO2 Emissions(g/km)"]
    #Obsługa Kolumhy Transmitter, ktora jest Stringiem!

    # Tworzenie modelu
    model = Sequential([
        Dense(64, activation='relu', input_shape=(X.shape[1],)),
        Dense(32, activation='relu'),
        Dense(1)  # Warstwa wyjściowa
    ])

    # Kompilacja modelu
    model.compile(optimizer='adam', loss='mean_squared_error')

    # Trenowanie modelu
    model.fit(X, y, epochs=50, batch_size=32, validation_split=0.2)

if __name__ == "__main__":
    main()