# test_module.py
import tkinter as tk
from tkinter import messagebox
import random
import os
import json
import io
import pygame
from gtts import gTTS

AUDIO_DIR = "audio"

# Файли для різних рівнів складності
DIFFICULTY_FILES = {
    "easy": "slang_ukr_easy.json",
    "medium": "slang_ukr_medium.json",
    "hard": "slang_ukr_hard.json"
}


def safe_filename(name: str) -> str:
    """Безпечне ім'я файлу"""
    if not name:
        return "audio"
    keep = []
    for ch in name:
        if ch.isalnum() or ch in (" ", "_", "-"):
            keep.append(ch)
        else:
            keep.append("_")
    s = "".join(keep).strip()
    s = s.replace(" ", "_")
    if not s:
        return "audio"
    return s


def load_json(path):
    """Завантажує JSON файл"""
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
                return []
        except Exception:
            return []
    return []


def play_text_tts(text, lang='en'):
    """Озвучує текст без збереження файлу (тільки в пам'яті)"""
    try:
        tts = gTTS(text, lang=lang)

        # Зберігаємо в пам'ять (BytesIO), а не у файл
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)

        # Відтворюємо через pygame
        pygame.mixer.music.load(fp, 'mp3')
        pygame.mixer.music.play()
    except Exception as e:
        messagebox.showwarning("TTS помилка", f"Не вдалося озвучити текст: {e}")


def show_difficulty_selection(parent, callback):
    """Показує вікно вибору складності"""

    selection_win = tk.Toplevel(parent)
    selection_win.title("Оберіть рівень складності")
    selection_win.geometry("400x580")
    selection_win.resizable(False, False)
    selection_win.grab_set()

    # Центруємо вікно
    selection_win.update_idletasks()
    x = (selection_win.winfo_screenwidth() // 2) - (400 // 2)
    y = (selection_win.winfo_screenheight() // 2) - (420 // 2)
    selection_win.geometry(f"400x480+{x}+{y}")

    # Заголовок
    title_label = tk.Label(
        selection_win,
        text="Оберіть рівень складності:",
        font=("Arial", 16, "bold"),
        pady=20
    )
    title_label.pack()

    # Опис
    desc_label = tk.Label(
        selection_win,
        text="Виберіть рівень для тестування\nваших знань інтернет-сленгу",
        font=("Arial", 10),
        fg="#666"
    )
    desc_label.pack(pady=(0, 20))

    # Фрейм для кнопок
    buttons_frame = tk.Frame(selection_win)
    buttons_frame.pack(pady=10)

    def select_difficulty(level):
        selection_win.destroy()
        callback(level)

    # Кнопка Easy
    btn_easy = tk.Button(
        buttons_frame,
        text="🔵 Легкий",
        font=("Arial", 14, "bold"),
        bg="#007bff",
        fg="white",
        width=18,
        height=2,
        command=lambda: select_difficulty("easy"),
        cursor="hand2"
    )
    btn_easy.pack(pady=8)

    easy_desc = tk.Label(
        buttons_frame,
        text="Базові слова (lol, app, pic, brb...)",
        font=("Arial", 9),
        fg="#666"
    )
    easy_desc.pack()

    # Кнопка Medium
    btn_medium = tk.Button(
        buttons_frame,
        text="🟡 Середній",
        font=("Arial", 14, "bold"),
        bg="#ffc107",
        fg="white",
        width=18,
        height=2,
        command=lambda: select_difficulty("medium"),
        cursor="hand2"
    )
    btn_medium.pack(pady=8)

    medium_desc = tk.Label(
        buttons_frame,
        text="Популярні слова (selfie, emoji, vlog...)",
        font=("Arial", 9),
        fg="#666"
    )
    medium_desc.pack()

    # Кнопка Hard
    btn_hard = tk.Button(
        buttons_frame,
        text="🔴 Складний",
        font=("Arial", 14, "bold"),
        bg="#8b0000",
        fg="white",
        width=18,
        height=2,
        command=lambda: select_difficulty("hard"),
        cursor="hand2"
    )
    btn_hard.pack(pady=8)

    hard_desc = tk.Label(
        buttons_frame,
        text="Складні та рідкісні слова",
        font=("Arial", 9),
        fg="#666"
    )
    hard_desc.pack()

    # Кнопка скасування
    btn_cancel = tk.Button(
        selection_win,
        text="Скасувати",
        font=("Arial", 10),
        command=selection_win.destroy
    )
    btn_cancel.pack(pady=20)


def open_test_window(parent, slang_words=None):
    """Відкриває модальне вікно тестування"""

    def start_test(difficulty):
        # Завантажуємо слова з відповідного файлу
        filename = DIFFICULTY_FILES.get(difficulty)
        if not filename:
            messagebox.showerror("Помилка", "Невірний рівень складності")
            return

        test_words = load_json(filename)

        # Перевірка: чи достатньо слів
        if len(test_words) < 10:
            messagebox.showwarning(
                "Недостатньо слів",
                f"У файлі {filename} недостатньо слів для тесту.\nПотрібно мінімум 10 слів."
            )
            return

        # Вибираємо 10 випадкових слів
        selected_words = random.sample(test_words, 10)

        # Запускаємо тест
        run_test(parent, selected_words, difficulty)

    # Показуємо вікно вибору складності
    show_difficulty_selection(parent, start_test)


def run_test(parent, test_words, difficulty):
    """Запускає тестування з вибраними словами"""

    # Створюємо модальне вікно (але НЕ робимо grab_set, щоб воно не зникало)
    test_win = tk.Toplevel(parent)
    test_win.title(f"Тестування знань сленгу — {difficulty.upper()}")
    test_win.geometry("1000x580")
    test_win.resizable(False, False)
    # НЕ використовуємо grab_set(), щоб вікно не зникало

    # Змінні для відстеження прогресу
    current_question = {"index": 0}
    user_answers = []

    # Кольори для рівнів
    difficulty_colors = {
        "easy": "#007bff",  # Синій
        "medium": "#ffc107",  # Жовтий
        "hard": "#8b0000"  # Темно-червоний (бордовий)
    }
    difficulty_color = difficulty_colors.get(difficulty, "#007bff")

    # ====== ШАПКА З ІНСТРУКЦІЄЮ ======
    header_frame = tk.Frame(test_win, bg="#f0f0f0", padx=10, pady=10)
    header_frame.pack(fill="x")

    # Рівень складності
    difficulty_labels = {
        "easy": "🔵 Легкий рівень",
        "medium": "🟡 Середній рівень",
        "hard": "🔴 Складний рівень"
    }

    level_label = tk.Label(
        header_frame,
        text=difficulty_labels.get(difficulty, "Тест"),
        font=("Arial", 11, "bold"),
        bg="#f0f0f0",
        fg=difficulty_color
    )
    level_label.pack()

    title_label = tk.Label(
        header_frame,
        text="Перевірте свої знання сленгу!",
        font=("Arial", 14, "bold"),
        bg="#f0f0f0"
    )
    title_label.pack()

    info_label = tk.Label(
        header_frame,
        text="Вам пропонується 10 випадкових слів.\n"
             "Введіть слово англійською на основі значення та перекладу.\n"
             "Регістр ігнорується (LOL = lol).",
        font=("Arial", 10),
        bg="#f0f0f0",
        fg="#555"
    )
    info_label.pack()

    # ====== ПРОГРЕС-БАР ======
    progress_frame = tk.Frame(test_win, bg="#e0e0e0", padx=10, pady=8)
    progress_frame.pack(fill="x")

    progress_label = tk.Label(
        progress_frame,
        text="Питання 1/10",
        font=("Arial", 12, "bold"),
        bg="#e0e0e0"
    )
    progress_label.pack()

    # ====== ОСНОВНА ЧАСТИНА: СПИСОК ПИТАНЬ ======
    main_frame = tk.Frame(test_win)
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Canvas з горизонтальною та вертикальною прокруткою
    canvas = tk.Canvas(main_frame)
    v_scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    h_scrollbar = tk.Scrollbar(main_frame, orient="horizontal", command=canvas.xview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

    canvas.grid(row=0, column=0, sticky="nsew")
    v_scrollbar.grid(row=0, column=1, sticky="ns")
    h_scrollbar.grid(row=1, column=0, sticky="ew")

    main_frame.grid_rowconfigure(0, weight=1)
    main_frame.grid_columnconfigure(0, weight=1)

    # Список для зберігання віджетів кожного питання
    question_widgets = []

    def play_audio_for_word(word):
        """Відтворення аудіо для слова (збереженого файлу)"""
        fname = safe_filename(word) + ".mp3"
        path = os.path.join(AUDIO_DIR, fname)

        if not os.path.exists(path):
            try:
                tts = gTTS(word, lang="en")
                tts.save(path)
            except Exception as e:
                messagebox.showwarning("TTS помилка", f"Не вдалося згенерувати аудіо: {e}")
                return

        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()
        except Exception as e:
            messagebox.showwarning("Audio помилка", f"Помилка відтворення: {e}")

    def check_answer(q_index):
        """Перевірка відповіді"""
        widgets = question_widgets[q_index]
        user_input = widgets["entry"].get().strip().lower()
        correct_word = test_words[q_index]["word"].strip().lower()

        # Перевірка
        is_correct = (user_input == correct_word)
        user_answers.append(is_correct)

        # Вимикаємо поле вводу та кнопку
        widgets["entry"].config(state="disabled")
        widgets["btn_submit"].config(state="disabled")

        # Показуємо результат
        result_frame = widgets["result_frame"]

        # Правильне слово
        color = "#28a745" if is_correct else "#dc3545"
        word_label = tk.Label(
            result_frame,
            text=test_words[q_index]["word"],
            font=("Arial", 11, "bold"),
            fg=color
        )
        word_label.pack(side="left", padx=5)

        # Транскрипція
        transcription = test_words[q_index].get("transcription", "")
        if transcription:
            trans_label = tk.Label(
                result_frame,
                text=f"[{transcription}]",
                font=("Arial", 10),
                fg="#666"
            )
            trans_label.pack(side="left", padx=5)

        # Кнопка аудіо
        btn_audio = tk.Button(
            result_frame,
            text="🔊",
            font=("Arial", 10),
            command=lambda: play_audio_for_word(test_words[q_index]["word"])
        )
        btn_audio.pack(side="left", padx=5)

        # Оновлюємо прогрес
        current_question["index"] = q_index + 1
        progress_label.config(text=f"Питання {current_question['index'] + 1}/10")

        # Активуємо наступне питання
        if q_index < 9:
            next_widgets = question_widgets[q_index + 1]
            next_widgets["entry"].config(state="normal")
            next_widgets["btn_submit"].config(state="normal")
            next_widgets["entry"].focus()
        else:
            # Тест завершено
            show_final_result()

    def show_final_result():
        """Показує фінальний результат"""
        correct_count = sum(user_answers)
        total = len(user_answers)

        # Текст оцінки
        if correct_count <= 3:
            message = "Треба попрацювати! 💪\nСпробуйте ще раз."
        elif correct_count <= 6:
            message = "Непогано! 👍\nВи на правильному шляху."
        elif correct_count <= 8:
            message = "Чудовий результат! 🎉"
        else:
            message = "Ідеально! 🏆\nВи справжній експерт!"

        # Створюємо вікно результату (НЕ модальне)
        result_win = tk.Toplevel(test_win)
        result_win.title("Результат тесту")
        result_win.geometry("350x220")
        result_win.resizable(False, False)

        # Центруємо
        result_win.update_idletasks()
        x = (result_win.winfo_screenwidth() // 2) - (350 // 2)
        y = (result_win.winfo_screenheight() // 2) - (220 // 2)
        result_win.geometry(f"350x220+{x}+{y}")

        # Результат
        result_label = tk.Label(
            result_win,
            text=f"Ваш результат:\n{correct_count}/{total}",
            font=("Arial", 18, "bold"),
            pady=20
        )
        result_label.pack()

        # Повідомлення
        msg_label = tk.Label(
            result_win,
            text=message,
            font=("Arial", 12),
            justify="center"
        )
        msg_label.pack(pady=10)

        # Кнопки
        buttons_frame = tk.Frame(result_win)
        buttons_frame.pack(pady=20)

        # Кнопка "Повторити тест"
        btn_repeat = tk.Button(
            buttons_frame,
            text="🔄 Повторити тест",
            font=("Arial", 11),
            command=lambda: [result_win.destroy(), test_win.destroy(), open_test_window(parent)]
        )
        btn_repeat.pack(side="left", padx=5)

        # Кнопка "Закрити"
        btn_close = tk.Button(
            buttons_frame,
            text="Закрити",
            font=("Arial", 11),
            command=result_win.destroy
        )
        btn_close.pack(side="left", padx=5)

    # Створюємо 10 рядків питань
    for i, word_data in enumerate(test_words):
        # Фрейм для кожного питання з кольоровою лінією зліва
        q_outer_frame = tk.Frame(scrollable_frame, relief="solid", borderwidth=1)
        q_outer_frame.pack(fill="x", pady=5)

        # Кольорова лінія зліва (індикатор складності)
        color_indicator = tk.Frame(q_outer_frame, bg=difficulty_color, width=5)
        color_indicator.pack(side="left", fill="y")

        # Основний фрейм питання
        q_frame = tk.Frame(q_outer_frame, padx=10, pady=8)
        q_frame.pack(side="left", fill="both", expand=True)

        # Номер питання
        num_label = tk.Label(q_frame, text=f"{i + 1}.", font=("Arial", 11, "bold"))
        num_label.grid(row=0, column=0, sticky="nw", padx=(0, 10))

        # Фрейм для значення та кнопки озвучування
        meaning_frame = tk.Frame(q_frame)
        meaning_frame.grid(row=0, column=1, sticky="w", padx=5)

        # Значення та переклад
        meaning = word_data.get("meaning", "")
        translation = word_data.get("translation", "")

        # Кнопка озвучування англійського значення
        btn_speak_meaning = tk.Button(
            meaning_frame,
            text="🔊",
            font=("Arial", 9),
            command=lambda m=meaning: play_text_tts(m, lang='en'),
            cursor="hand2",
            width=3,
            height=1
        )
        btn_speak_meaning.grid(row=0, column=0, padx=(0, 5))

        # Текст значення та перекладу
        info_text = f"Значення: {meaning}\nПереклад: {translation}"
        info_label = tk.Label(meaning_frame, text=info_text, font=("Arial", 10), justify="left", wraplength=450)
        info_label.grid(row=0, column=1, sticky="w")

        # Поле вводу
        entry_var = tk.StringVar()
        entry = tk.Entry(q_frame, textvariable=entry_var, font=("Arial", 11), width=20, state="disabled")
        entry.grid(row=0, column=2, padx=5)

        # Підтримка Enter для відправки
        entry.bind("<Return>", lambda e, idx=i: check_answer(idx))

        # Кнопка "Відправити"
        btn_submit = tk.Button(
            q_frame,
            text="Відправити",
            font=("Arial", 10),
            state="disabled",
            command=lambda idx=i: check_answer(idx)
        )
        btn_submit.grid(row=0, column=3, padx=5)

        # Фрейм для результату (спочатку порожній)
        result_frame = tk.Frame(q_frame)
        result_frame.grid(row=0, column=4, sticky="w", padx=10)

        # Зберігаємо віджети
        question_widgets.append({
            "entry": entry,
            "btn_submit": btn_submit,
            "result_frame": result_frame
        })

    # Активуємо перше питання
    question_widgets[0]["entry"].config(state="normal")
    question_widgets[0]["btn_submit"].config(state="normal")
    question_widgets[0]["entry"].focus()

    # ====== КНОПКА ЗАКРИТТЯ ======
    close_frame = tk.Frame(test_win, padx=10, pady=10)
    close_frame.pack(fill="x")

    btn_close = tk.Button(
        close_frame,
        text="Закрити тест",
        font=("Arial", 11),
        command=test_win.destroy
    )
    btn_close.pack(side="right")