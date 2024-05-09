import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from keras._tf_keras.keras.models import Sequential
from keras._tf_keras.keras.layers import Dense


def main():
    file = r"C:\Users\Piotr\source\repos\CO2_Emmision_AI\CO2_Emissions_Canada.csv"
    df = pd.read_csv(file)
    # Obsługa Kolumny Transmission, ktora jest Stringiem!
    df["Transmission"] = pd.factorize(df["Transmission"])[0]
    df["Fuel Type"] = pd.factorize(df["Fuel Type"])[0]
    # Wybór cech i etykiety
    X = pd.get_dummies(df.drop(columns=["Make", "Model", "Vehicle Class", "CO2 Emissions(g/km)"]))
    Y = df["CO2 Emissions(g/km)"]
    # Obsługa Kolumny Transmission, ktora jest Stringiem!
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=.2)
    X_train.head()
    Y_train.head()
    # Create model
    model = Sequential()
    model.add(Dense(units=32, activation='relu', input_dim=len(X_train.columns)))
    model.add(Dense(units=64, activation='relu'))
    model.add(Dense(units=1, activation='linear'))
    model.compile(loss='mean_squared_logarithmic_error', optimizer='adam')
    model.fit(X_train, Y_train, epochs=200, batch_size=32)

    y_hat = model.predict(X_test)
    y_hat = [0 if val < 0.5 else 1 for val in y_hat]
    accuracy = accuracy_score(Y_test, y_hat)
    print(accuracy)


if __name__ == "__main__":
    main()
