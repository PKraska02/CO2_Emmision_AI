import matplotlib.pyplot as plt


def show_plot(model, X_test, Y_test):
    # Wykonaj predykcję za pomocą modelu
    y_pred = model.predict(X_test)

    # Sortowanie danych testowych i przewidywanych według indeksu
    sorted_indices = Y_test.argsort()
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

def check_co2():
    pass

