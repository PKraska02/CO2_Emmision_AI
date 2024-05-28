import tkinter as tk
from tkinter import messagebox

import matplotlib.pyplot as plt

import AI_model as ai


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

def display_form(container):
    # Clear the container
    for widget in container.winfo_children():
        widget.destroy()

    # Define the labels and entry fields
    fields = [
        'Marka', 'Model', 'Klasa pojazdu', 'Pojemność silnika (L)', 'Cylindry',
        'Skrzynia biegów', 'Rodzaj paliwa', 'Zużycie paliwa w mieście (L/100 km)',
        'Zużycie paliwa na autostradzie (L/100 km)', 'Średnie zużycie paliwa (L/100 km)',
        'Średnie zużycie paliwa (mpg)'
    ]

    entries = {}

    for i, field in enumerate(fields):
        label = tk.Label(container, text=field)
        label.grid(row=i, column=0, padx=10, pady=5, sticky=tk.W)

        entry = tk.Entry(container, width=30)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entries[field] = entry

    # Define the submit function
    def submit():
        input_data = {field: entry.get() for field, entry in entries.items()}
        # Clear the form
        for widget in container.winfo_children():
            widget.destroy()
        #TODO obliczenia

        # Display the result
        result_text = f"Przewidywana emisja CO2 twojego pojazdu wynosi: {input_data.get('Emisja CO2 (g/km)', 'Unknown')}"
        result_label = tk.Label(container, text=result_text, font=("Arial", 16))
        result_label.pack(pady=20)

    # Add a submit button
    submit_button = tk.Button(container, text="Wyślij", command=submit)
    submit_button.grid(row=len(fields), column=0, columnspan=2, pady=10)

    result_label = tk.Label(container, text="")
    result_label.grid(row=len(fields) + 1, column=0, columnspan=2)

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

    label = tk.Label(confirmation_window, text="Czy na pewno chcesz kontynuować? Operacja pernamentnie usunie aktualny model i utworzy nowy.", font=("Arial", 14))
    label.pack(pady=20)

    button_frame = tk.Frame(confirmation_window)
    button_frame.pack(pady=10)

    yes_button = tk.Button(button_frame, text="TAK", command=on_yes, width=10)
    yes_button.grid(row=0, column=0, padx=10)

    no_button = tk.Button(button_frame, text="NIE", command=on_no, width=10)
    no_button.grid(row=0, column=1, padx=10)
