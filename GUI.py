import tkinter as tk
from tkinter import messagebox

import matplotlib.pyplot as plt

import AI_model as ai
import Actual_Model as am
from tkinter import ttk


def show_plot():
    # Wykonaj predykcję za pomocą modelu
    y_pred = am.model.predict(am.X_test)

    # Sortowanie danych testowych i przewidywanych według indeksu
    sorted_indices = am.Y_test.argsort()
    Y_test_sorted = am.Y_test.iloc[sorted_indices]
    y_pred_sorted = y_pred[sorted_indices]

    # Rysowanie posortowanych danych
    plt.scatter(Y_test_sorted, y_pred_sorted, color='blue')
    plt.plot([Y_test_sorted.min(), Y_test_sorted.max()], [Y_test_sorted.min(), Y_test_sorted.max()], color='red',
             linestyle='--')
    plt.xlabel('Aktualna Emisja CO2(g/km)')
    plt.ylabel('Przewidywana Emisja CO2(g/km)')
    plt.title('Aktualna vs Przewidywana Emisja CO2')
    plt.show()


def display_form(container):
    # Clear the container
    for widget in container.winfo_children():
        widget.destroy()

    # Oryginalne etykiety kolumn
    original_labels = {
        'Engine Size(L)': 'Pojemność silnika (L)',
        'Cylinders': 'Cylindry',
        'Transmission': 'Skrzynia biegów',
        'Fuel Type': 'Rodzaj paliwa',
        'Fuel Consumption City (L/100 km)': 'Zużycie paliwa w mieście (L/100 km)',
        'Fuel Consumption Hwy (L/100 km)': 'Zużycie paliwa na autostradzie (L/100 km)',
        'Fuel Consumption Comb (L/100 km)': 'Średnie zużycie paliwa (L/100 km)'
    }

    numeric_fields = [
        'Engine Size(L)',
        'Fuel Consumption City (L/100 km)',
        'Fuel Consumption Hwy (L/100 km)',
        'Fuel Consumption Comb (L/100 km)'
    ]

    transmission_options = [
        'A10', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'AM5', 'AM6', 'AM7', 'AM8', 'AM9',
        'AS10', 'AS4', 'AS5', 'AS6', 'AS7', 'AS8', 'AS9', 'AV', 'AV10', 'AV6', 'AV7', 'AV8', 'M5', 'M6', 'M7'
    ]

    fuel_type_options = ['D', 'E', 'N', 'X', 'Z']

    entries = {}

    # Create a frame to center the form
    form_frame = tk.Frame(container, padx=20, pady=20)
    form_frame.pack(expand=True)

    for i, field in enumerate(original_labels.keys()):
        label_text = original_labels[field]
        label = tk.Label(form_frame, text=label_text)  # Użyj przetłumaczonych etykiet
        label.grid(row=i, column=0, padx=10, pady=5, sticky=tk.W)

        if field in numeric_fields:
            entry = tk.Spinbox(form_frame, from_=0, to=100, increment=0.1, width=30)
        elif field == 'Cylinders':
            entry = tk.Spinbox(form_frame, from_=0, to=16, increment=1, width=30)
        elif field == 'Transmission':
            entry = ttk.Combobox(form_frame, values=transmission_options, width=30, state='readonly')
        elif field == 'Fuel Type':
            entry = ttk.Combobox(form_frame, values=fuel_type_options, width=30, state='readonly')
        else:
            entry = tk.Entry(form_frame, width=32)

        entry.grid(row=i, column=1, padx=10, pady=5)
        entries[field] = entry

    # Define the submit function
    def submit():
        input_data = {field: entry.get() for field, entry in entries.items()}
        for field, value in input_data.items():
            if value == "":
                messagebox.showerror("Błąd", f"Pole '{original_labels[field]}' nie może być puste.")
                return
        # Clear the form
        for widget in container.winfo_children():
            widget.destroy()
        # Przetwórz dane wejściowe w odpowiedni format
        input_features = ai.preprocess_input(input_data)
        pred_c02_emmision = am.model.predict(input_features)
        # Display the result
        result_text = f"Przewidywana emisja CO2 twojego pojazdu wynosi: {pred_c02_emmision.item()} g/km"
        result_label = tk.Label(container, text=result_text, font=("Arial", 16))
        result_label.pack(pady=20)

    # Add a submit button
    submit_button = tk.Button(form_frame, text="Wyślij", command=submit)
    submit_button.grid(row=len(original_labels), column=0, columnspan=2, pady=20)

    result_label = tk.Label(form_frame, text="")
    result_label.grid(row=len(original_labels) + 1, column=0, columnspan=2)



def update_model():
    def on_yes():
        confirmation_window.destroy()
        messagebox.showinfo("Confirmation", "Uczenie nowego modelu, proszę czekać.")
        ai.update_model()
        messagebox.showinfo("Confirmation", "Nowy model został utworzony pomyślnie.")

    def on_no():
        confirmation_window.destroy()

    confirmation_window = tk.Toplevel()
    confirmation_window.title("Confirmation")
    confirmation_window.geometry("1000x150")

    # Center the window on the screen
    window_width = 1000
    window_height = 150

    screen_width = confirmation_window.winfo_screenwidth()
    screen_height = confirmation_window.winfo_screenheight()

    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)

    confirmation_window.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

    label = tk.Label(confirmation_window,
                     text="Czy na pewno chcesz kontynuować? Operacja pernamentnie usunie aktualny model i utworzy nowy.",
                     font=("Arial", 14))
    label.pack(pady=20)

    button_frame = tk.Frame(confirmation_window)
    button_frame.pack(pady=10)

    yes_button = tk.Button(button_frame, text="TAK", command=on_yes, width=10)
    yes_button.grid(row=0, column=0, padx=10)

    no_button = tk.Button(button_frame, text="NIE", command=on_no, width=10)
    no_button.grid(row=0, column=1, padx=10)
