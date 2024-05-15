import tkinter as tk
import GUI as gui
from AI_model import create_model, update_model



def main():
    print("Create GUI")
    root = tk.Tk()
    root.title("Aplikacja AI")
    root.geometry("1280x840")
    model, X_test, Y_test = create_model()

    # Tworzenie przycisków i ich umieszczenie obok siebie
    button_train = tk.Button(root, text="Włącz uczenie", command=update_model)
    button_train.pack(side=tk.LEFT, padx=10, pady=10)

    button_plot = tk.Button(root, text="Pokaż wykres", command=lambda: gui.show_plot(model, X_test, Y_test))
    button_plot.pack(side=tk.LEFT, padx=10, pady=10)

    button_check = tk.Button(root, text="Sprawdź ile CO2", command=gui.check_co2)
    button_check.pack(side=tk.LEFT, padx=10, pady=10)

    # Uruchom pętlę główną tkinter
    root.mainloop()


if __name__ == "__main__":
    main()
