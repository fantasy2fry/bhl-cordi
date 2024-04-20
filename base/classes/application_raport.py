import tkinter as tk
from tkinter import ttk
from gettext import translation, gettext as _


# Ustawienie tłumaczenia na podstawie wybranego języka
def set_language(lang_code):
    global _
    try:
        lang_translation = translation('app', localedir='locales', languages=[lang_code])
        lang_translation.install()
        _ = lang_translation.gettext
    except FileNotFoundError:
        _ = lambda s: s


# Funkcja, która tworzy okno aplikacji z problemami
def create_app(language, problems_list, get_problems_function):
    set_language(language)

    root = tk.Tk()
    root.title(_("Analiza zawartości plików"))

    # Styl dla pogrubionego tekstu
    style = ttk.Style()
    style.configure("Bold.TLabel", font=('Arial', 10, 'bold'))

    notebook = ttk.Notebook(root)
    main_tab = ttk.Frame(notebook)
    notebook.add(main_tab, text=_('Główna'))
    notebook.pack(expand=1, fill="both")

    problems_frame = ttk.LabelFrame(main_tab, text=_("Tematy zarejestrowanych problemów:"))
    problems_frame.pack(fill='x', expand=True, padx=10, pady=10)

    problems_label = ttk.Label(problems_frame, text=", ".join(problems_list), anchor="w")
    problems_label.pack(fill='x')

    problems_dict = get_problems_function()
    total_problems = sum(problems_dict.values())

    # Pogrubiona etykieta z łączną liczbą zarejestrowanych problemów, wyrównana do lewej
    total_label = ttk.Label(problems_frame, text=_("Łączna liczba zarejestrowanych problemów: {}").format(total_problems), style="Bold.TLabel", anchor="w")
    total_label.pack(fill='x')

    for problem, count in problems_dict.items():
        if problem in problems_list:
            label_text = _("Liczba problemów w kategorii '{}': {}").format(problem, count)
            label = ttk.Label(problems_frame, text=label_text, anchor="w")
            label.pack(fill='x')

    root.mainloop()


# Symulacja funkcji, która zwraca słownik z problemami i ich ilościami
def get_registered_problems():
    return {
        "Diamond inheritance problem": 1,
        "Not using the super() function": 3,
        "Static variable issue": 2,
    }


# Przykład użycia funkcji
if __name__ == "__main__":
    selected_language = "ru"  # Tutaj ustawiasz język
    selected_problems = [
        "Diamond inheritance problem",
        "Not using the super() function",
        "Static variable issue",
    ]
    create_app(selected_language, selected_problems, get_registered_problems)
