import os
import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split
#import tensorflow as tf
import numpy as np


def main():
    file = r"C:\Users\Piotr\source\repos\CO2-Emmision-AI\archive\CO2 Emissions_Canada.csv"
    df = pd.read_csv(file)
    data = df.dtypes
    print(data)
    ## Normalize Data ##
    x = data.drop("CO2 Emissions(g/km)")
    y = data["CO2 Emissions(g/km)"]
    '''
    # TODO, przerobić z przykładem do naszych danych
    # Załóżmy, że masz dane wejściowe w postaci listy kolorów jako stringi
colors = ['red', 'blue', 'green', 'red', 'white']

# Tworzenie słownika mapującego unikalne kolory na liczby całkowite
color_to_index = {'red': 0, 'blue': 1, 'green': 2, 'white': 3}

# Przekształcenie kolorów na liczby całkowite przy użyciu mapowania
indexed_colors = [color_to_index[color] for color in colors]

# Konwersja indeksów kolorów na wektory one-hot
one_hot_colors = tf.keras.utils.to_categorical(indexed_colors)

# Wyświetlenie przekształconych danych
print(one_hot_colors)
    '''
    ## Make model ##

if __name__ == "__main__":
    main()
