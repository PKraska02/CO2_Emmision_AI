import tkinter as tk

import Actual_Model as am
import GUI as gui
from AI_model import create_model


def main():
    print("Create GUI")
    root = tk.Tk()
    root.title("Aplikacja predykująca emisję CO2 pojazdu")
    root.geometry("1280x840")

    # Define a style for the buttons
    button_style = {
        "font": ("Arial", 12),
        "bg": "#4CAF50",
        "fg": "white",
        "activebackground": "#45a049",
        "activeforeground": "white",
        "width": 30,
        "height": 2
    }

    # Create the model and test data
    create_model()

    # Create a main frame to hold all content
    main_frame = tk.Frame(root, padx=20, pady=20)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Create a frame for buttons
    button_frame = tk.Frame(main_frame)
    button_frame.pack(pady=20)

    # Create a frame for the form and result display
    form_frame = tk.Frame(main_frame)
    form_frame.pack(pady=20, fill=tk.BOTH, expand=True)

    # Create and pack buttons with styling
    button_train = tk.Button(button_frame, text="Utwórz nowy model", command=lambda: gui.update_model(), **button_style)
    button_train.grid(row=0, column=0, padx=10, pady=10)

    # Increase width for the middle button
    button_plot_style = button_style.copy()
    button_plot_style['width'] = 40  # Increase width of the middle button

    button_plot = tk.Button(button_frame, text="Pokaż wykres skuteczności aktualnego modelu", command=lambda: gui.show_plot(am.model, am.X_test, am.Y_test),
                            **button_plot_style)
    button_plot.grid(row=0, column=1, padx=10, pady=10)

    button_check = tk.Button(button_frame, text="Sprawdź ile CO2 produkuje twój pojazd",
                             command=lambda: gui.display_form(form_frame), **button_style)
    button_check.grid(row=0, column=2, padx=10, pady=10)

    # Optional: Add some additional styling or widgets if needed
    # Example: A title label
    title_label = tk.Label(main_frame, text="Aplikacja predykująca emisję CO2 pojazdu", font=("Arial", 24))
    title_label.pack(pady=20)

    # Uruchom pętlę główną tkinter
    root.mainloop()


if __name__ == "__main__":
    main()
