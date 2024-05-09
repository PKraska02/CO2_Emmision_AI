import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from keras._tf_keras.keras.models import Sequential
from keras._tf_keras.keras.layers import Dense
import matplotlib.pyplot as plt

def main():
    file = r"C:\Users\Piotr\source\repos\CO2_Emmision_AI\CO2_Emissions_Canada.csv"
    df = pd.read_csv(file)
    # Wybór cech i etykiety
    df_x = df.drop(columns=["Make", "Model", "Vehicle Class", "CO2 Emissions(g/km)","Fuel Consumption Comb (mpg)"])

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
    #Skalowanie
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

    y_pred = model.predict(X_test)

    # Sortowanie danych testowych i przewidywanych według indeksu
    sorted_indices = Y_test.argsort()
    #print(sorted_indices)
    Y_test_sorted = Y_test.iloc[sorted_indices]
    y_pred_sorted = y_pred[sorted_indices]

    # Rysowanie posortowanych danych
    plt.scatter(Y_test_sorted, y_pred_sorted, color='blue')
    plt.plot([Y_test_sorted.min(), Y_test_sorted.max()], [Y_test_sorted.min(), Y_test_sorted.max()], color='red',
             linestyle='--')
    plt.xlabel('Actual CO2 Emissions(g/km)')
    plt.ylabel('Predicted CO2 Emissions(g/km)')
    plt.title('Actual vs Predicted CO2 Emissions')
    plt.show()


if __name__ == "__main__":
    main()
