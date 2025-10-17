# slang_gui_ukr.py
import json
import os
import sys
import shutil
import time

from fpdf import FPDF, XPos, YPos
from gtts import gTTS
import pygame
import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
import re
# Імпорт модуля тестування
from test_module import open_test_window

# ------------------------ Конфигурація ------------------------
JSON_FILE = "slang_ukr_hard.json"
AUDIO_DIR = "audio"
WINDOW_SIZE = "940x600"

os.makedirs(AUDIO_DIR, exist_ok=True)

# ------------------------ Завантаження даних ------------------------
def load_json(path):
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

slang_words = load_json(JSON_FILE)

# ------------------------ Ініціалізація аудіо ------------------------
pygame_inited = False
try:
    pygame.mixer.init()
    pygame_inited = True
except Exception as e:
    print("Warning: pygame init failed:", e, file=sys.stderr)

# ------------------------ Типи слів, кольори, підказки ------------------------
TYPE_COLORS = {
    "Акронім": "#1E90FF",
    "Ініціалізм": "#2E8B57",
    "Усічення": "#FF8C00",
    "Бленд": "#8A2BE2",
    "Лексичні запозичення": "#A0522D",
    "Семантичний зсув": "#20B2AA",
    "Неологізм": "#DC143C",
    "Фонетичні/орфографічні ігри": "#FF1493"
}

TYPE_HELP = {
    "Акронім": "Слово, утворене з перших букв фрази (LOL, NATO)",
    "Ініціалізм": "Скорочення, де букви вимовляються окремо (AFK, BRB)",
    "Усічення": "Скорочені форми слів (app, pic, net)",
    "Бленд": "Слово, утворене з двох і більше слів (brunch, vlog)",
    "Лексичні запозичення": "Слова, запозичені з інших мов (emoji, meme)",
    "Семантичний зсув": "Слова, які змінили значення (cloud, wall)",
    "Неологізм": "Відносно нове слово або вираз (selfie, googling)",
    "Фонетичні/орфографічні ігри": "Ігрові форми слів (u, thx, 4ever)"
}

# ------------------------ Утиліти ------------------------
def safe_filename(name: str) -> str:
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

def save_json(path, data):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        messagebox.showerror("Помилка", f"Не вдалося зберегти {path}:\n{e}")

# ------------------------ GUI: базова ініціалізація ------------------------
root = tk.Tk()
root.title("Словник інтернет-сленгу")
root.geometry(WINDOW_SIZE)
root.minsize(1040, 520)

search_var = tk.StringVar()
search_frame = tk.Frame(root)
search_frame.grid(row=0, column=0, columnspan=2, sticky="we", padx=10, pady=(10,0))
search_label = tk.Label(search_frame, text="Пошук:", font=("Arial", 11))
search_label.pack(side="left")
search_entry = tk.Entry(search_frame, textvariable=search_var, font=("Arial", 11))
search_entry.pack(side="left", fill="x", expand=True, padx=(6,6))

# ------------------------ Список слів ------------------------
list_frame = tk.Frame(root)
list_frame.grid(row=1, column=0, sticky="nswe", padx=10, pady=10)
list_scroll = tk.Scrollbar(list_frame, orient=tk.VERTICAL)
listbox = tk.Listbox(list_frame, yscrollcommand=list_scroll.set, font=("Arial", 12), width=20)
list_scroll.config(command=listbox.yview)
list_scroll.pack(side="right", fill="y")
listbox.pack(side="left", fill="both", expand=True)

current_list = slang_words.copy()

def populate_listbox(filter_text=""):
    listbox.delete(0, tk.END)
    global current_list
    if filter_text:
        ft = filter_text.lower()
        current_list = [w for w in slang_words if ft in w.get("word", "").lower()]
    else:
        current_list = slang_words.copy()
    for item in current_list:
        listbox.insert(tk.END, item.get("word", ""))

def on_search_key(event=None):
    populate_listbox(search_var.get().strip())

search_entry.bind("<KeyRelease>", on_search_key)
populate_listbox()

# ------------------------ Поля інформації (права панель) ------------------------
info_frame = tk.Frame(root)
info_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(1, weight=1)
info_frame.grid_rowconfigure(8, weight=1)
info_frame.grid_columnconfigure(1, weight=1)

selected_word_label = tk.Label(info_frame, text="", font=("Arial", 20, "bold"), fg="black")
selected_word_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0,8))

tk.Label(info_frame, text="Слово:", font=("Arial", 12, "bold")).grid(row=1, column=0, sticky="w")
word_var = tk.StringVar()
word_entry = tk.Entry(info_frame, textvariable=word_var, font=("Arial", 12))
word_entry.grid(row=1, column=1, sticky="we", pady=2)

tk.Label(info_frame, text="Транскрипція:", font=("Arial", 12, "bold")).grid(row=2, column=0, sticky="w")
transcription_var = tk.StringVar()
transcription_entry = tk.Entry(info_frame, textvariable=transcription_var, font=("Arial", 12))
transcription_entry.grid(row=2, column=1, sticky="we", pady=2)

tk.Label(info_frame, text="Значення:", font=("Arial", 12, "bold")).grid(row=3, column=0, sticky="w")
meaning_var = tk.StringVar()
meaning_entry = tk.Entry(info_frame, textvariable=meaning_var, font=("Arial", 12))
meaning_entry.grid(row=3, column=1, sticky="we", pady=2)

tk.Label(info_frame, text="Переклад:", font=("Arial", 12, "bold")).grid(row=4, column=0, sticky="nw")
translation_text = scrolledtext.ScrolledText(info_frame, font=("Arial", 11), height=4, wrap=tk.WORD)
translation_text.grid(row=4, column=1, sticky="we", pady=2)

tk.Label(info_frame, text="Походження:", font=("Arial", 12, "bold")).grid(row=5, column=0, sticky="w")
origin_var = tk.StringVar()
origin_entry = tk.Entry(info_frame, textvariable=origin_var, font=("Arial", 12))
origin_entry.grid(row=5, column=1, sticky="we", pady=2)

tk.Label(info_frame, text="Примітка:", font=("Arial", 12, "bold")).grid(row=6, column=0, sticky="nw")
note_text = scrolledtext.ScrolledText(info_frame, font=("Arial", 11), height=4, wrap=tk.WORD)
note_text.grid(row=6, column=1, sticky="we", pady=2)

# ------------------------ Тип і OptionMenu ------------------------
type_label = tk.Label(info_frame, text="Тип:", font=("Arial", 12, "bold"), fg="black")
type_label.grid(row=7, column=0, sticky="w", pady=(6,2))

type_var = tk.StringVar()
type_var.set("")

types_list = ["Акронім", "Ініціалізм", "Усічення", "Бленд",
              "Лексичні запозичення", "Семантичний зсув",
              "Неологізм", "Фонетичні/орфографічні ігри"]

# Функція для оновлення кольору OptionMenu і верхнього слова
def update_type_color(*args):
    color = TYPE_COLORS.get(type_var.get(), "black")
    selected_word_label.config(fg=color)
    type_menu.config(fg=color)

# OptionMenu для вибору типу
type_menu = tk.OptionMenu(info_frame, type_var, *types_list, command=lambda _: update_type_color())
type_menu.config(font=("Arial", 12), anchor="w")
type_menu.grid(row=7, column=1, sticky="w", pady=(6,2))

# Tooltip для OptionMenu
tooltip_label = tk.Label(info_frame, text="", font=("Arial", 10), fg="gray")
tooltip_label.grid(row=8, column=1, sticky="w")

def show_type_tooltip(event):
    tooltip_label.config(text=TYPE_HELP.get(type_var.get(), ""))

def hide_type_tooltip(event):
    tooltip_label.config(text="")

type_menu.bind("<Enter>", show_type_tooltip)
type_menu.bind("<Leave>", hide_type_tooltip)

# ------------------------ Відображення вибраного слова ------------------------
def show_word(event=None):
    sel = listbox.curselection()
    if not sel:
        return
    idx = sel[0]
    entry = current_list[idx]

    word_var.set(entry.get("word", ""))
    transcription_var.set(entry.get("transcription", ""))
    meaning_var.set(entry.get("meaning", ""))
    translation_text.delete("1.0", tk.END)
    translation_text.insert(tk.END, entry.get("translation", ""))
    origin_var.set(entry.get("origin", ""))
    note_text.delete("1.0", tk.END)
    note_text.insert(tk.END, entry.get("note", ""))
    type_var.set(entry.get("type", ""))

    # Оновлення кольору верхнього слова та OptionMenu
    typ = entry.get("type", "")
    color = TYPE_COLORS.get(typ, "black")
    selected_word_label.config(text=entry.get("word", ""), fg=color)
    type_menu.config(fg=color)

    # Зберігаємо поточну вибрану запис
    root.selected_entry = entry

listbox.bind("<<ListboxSelect>>", show_word)

# ------------------------ Аудіо ------------------------
def play_audio_for_entry(entry):
    if not entry:
        messagebox.showwarning("Увага", "Спочатку виберіть слово.")
        return
    word = entry.get("word", "").strip()
    if not word:
        messagebox.showwarning("Увага", "Слово пусте.")
        return
    fname = safe_filename(word) + ".mp3"
    path = os.path.join(AUDIO_DIR, fname)
    entry["audio"] = fname
    if not os.path.exists(path):
        try:
            tts = gTTS(word, lang="en")
            tts.save(path)
        except Exception as e:
            messagebox.showwarning("TTS помилка", f"Не вдалося згенерувати аудіо: {e}")
            return
    if pygame_inited:
        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()
        except Exception as e:
            messagebox.showwarning("Audio помилка", f"Помилка відтворення: {e}")
    else:
        messagebox.showinfo("Аудіо", f"Аудіофайл збережено: {path}")

# ------------------------ Збереження / Додавання / Видалення ------------------------
def save_current_word():
    word_text = word_var.get().strip()
    if not word_text:
        messagebox.showwarning("Помилка", "Поле 'Слово' не може бути пустим.")
        return
    transcription = transcription_var.get().strip()
    meaning = meaning_var.get().strip()
    translation = translation_text.get("1.0", tk.END).strip()
    origin = origin_var.get().strip()
    note = note_text.get("1.0", tk.END).strip()
    typ = type_var.get().strip()
    audio_name = safe_filename(word_text) + ".mp3"

    existing = next((w for w in slang_words if w.get("word", "") == word_text), None)
    if existing:
        existing.update({
            "transcription": transcription,
            "meaning": meaning,
            "translation": translation,
            "origin": origin,
            "note": note,
            "type": typ,
            "audio": audio_name
        })
    else:
        new_entry = {
            "word": word_text,
            "transcription": transcription,
            "meaning": meaning,
            "translation": translation,
            "origin": origin,
            "note": note,
            "type": typ,
            "audio": audio_name
        }
        slang_words.append(new_entry)
        current_list.append(new_entry)
        listbox.insert(tk.END, new_entry["word"])

    save_json(JSON_FILE, slang_words)
    audio_path = os.path.join(AUDIO_DIR, audio_name)
    if not os.path.exists(audio_path):
        try:
            tts = gTTS(word_text, lang="en")
            tts.save(audio_path)
        except Exception as e:
            print("TTS save error:", e, file=sys.stderr)

    populate_listbox(search_var.get().strip())
    idx = next((i for i, w in enumerate(current_list) if w.get("word","") == word_text), None)
    if idx is not None:
        listbox.selection_clear(0, tk.END)
        listbox.selection_set(idx)
        listbox.see(idx)
    messagebox.showinfo("Збережено", f"Слово '{word_text}' збережено.")

def add_new_word_prompt():
    res = simpledialog.askstring("Нове слово", "Введіть нове слово (латиницею):")
    if not res:
        return
    word_var.set(res.strip())
    transcription_var.set("")
    meaning_var.set("")
    translation_text.delete("1.0", tk.END)
    origin_var.set("")
    note_text.delete("1.0", tk.END)
    type_var.set("")
    selected_word_label.config(text=res.strip(), fg="black")

# ------------------------ Видалення ------------------------
def delete_selected_word():
    sel = listbox.curselection()
    if not sel:
        messagebox.showwarning("Увага", "Спочатку виберіть слово для видалення.")
        return
    idx = sel[0]
    entry = current_list[idx]
    word_text = entry.get("word", "")
    if not messagebox.askyesno("Підтвердження", f"Видалити слово '{word_text}'?"):
        return
    slang_words[:] = [w for w in slang_words if w.get("word","") != word_text]
    populate_listbox(search_var.get().strip())
    save_json(JSON_FILE, slang_words)
    audio_fname = entry.get("audio", safe_filename(word_text) + ".mp3")
    audio_path = os.path.join(AUDIO_DIR, audio_fname)
    try:
        if os.path.exists(audio_path):
            os.remove(audio_path)
    except Exception:
        pass
    word_var.set("")
    transcription_var.set("")
    meaning_var.set("")
    translation_text.delete("1.0", tk.END)
    origin_var.set("")
    note_text.delete("1.0", tk.END)
    type_var.set("")
    selected_word_label.config(text="", fg="black")
    messagebox.showinfo("Готово", f"Слово '{word_text}' видалено.")

# ------------------------ Сортування та резервні копії ------------------------
def backup_json():
    try:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        backup_name = f"{os.path.splitext(JSON_FILE)[0]}_backup_{timestamp}.json"
        shutil.copy2(JSON_FILE, backup_name)
        messagebox.showinfo("Backup", f"Резервна копія створена:\n{backup_name}")
    except Exception as e:
        messagebox.showwarning("Backup error", f"Не вдалося створити резервну копію: {e}")

def clean_text(s: str) -> str:
    """Удаляет символы, которые не поддерживаются PDF-шрифтом."""
    if not s:
        return ""
    # Удаляем управляющие символы и слишком экзотические юникоды
    s = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F]", "", s)
    s = s.replace("\u200b", "")  # zero-width space
    return s.strip()

def export_to_pdf():
    data = load_json(JSON_FILE)
    if not data:
        messagebox.showwarning("Увага", "Словник порожній, немає чого експортувати.")
        return

    file_path = os.path.join(os.path.dirname(JSON_FILE), "slang_export.pdf")

    pdf = FPDF()
    pdf.add_page()

    # Добавляем шрифты
    pdf.add_font("DejaVu", "", "DejaVuSans.ttf")
    pdf.add_font("DejaVu", "B", "DejaVuSans-Bold.ttf")

    # Заголовок документа
    pdf.set_font("DejaVu", "B", size=14)
    pdf.cell(0, 10, "Словник інтернет-сленгу", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(6)

    page_width = pdf.w - 2 * pdf.l_margin  # рабочая ширина страницы
    left_indent = pdf.l_margin + 4         # небольшой внутренний отступ

    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    for entry in data:
        word = clean_text(entry.get("word", ""))
        transcription = clean_text(entry.get("transcription", ""))
        meaning = clean_text(entry.get("meaning", ""))
        translation = clean_text(entry.get("translation", ""))
        origin = clean_text(entry.get("origin", ""))
        note = clean_text(entry.get("note", ""))
        type_ = clean_text(entry.get("type", ""))
        audio = clean_text(entry.get("audio", ""))

        # 🔹 Цвет слова и типа по TYPE_COLORS
        word_color = TYPE_COLORS.get(type_, "#000000")
        r, g, b = hex_to_rgb(word_color)
        pdf.set_text_color(r, g, b)

        # 🔹 Слово + транскрипция
        pdf.set_font("DejaVu", "B", size=12)
        pdf.set_x(left_indent)
        pdf.multi_cell(page_width - 8, 8, f"{word} {transcription}")

        # 🔹 Тип того же цвета
        if type_:
            pdf.set_font("DejaVu", "B", size=11)
            pdf.set_x(left_indent)
            pdf.multi_cell(page_width - 8, 7, f"Тип: {type_}")

        # 🔹 Возврат цвета к черному для остальных полей
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("DejaVu", size=11)

        # 🔹 Значення
        if meaning:
            pdf.set_font("DejaVu", "B", size=11)
            pdf.set_x(left_indent)
            pdf.multi_cell(page_width - 8, 7, "Значення:")
            pdf.set_font("DejaVu", size=11)
            pdf.set_x(left_indent)
            pdf.multi_cell(page_width - 8, 7, meaning)

        # 🔹 Переклад
        if translation:
            pdf.set_font("DejaVu", "B", size=11)
            pdf.set_x(left_indent)
            pdf.multi_cell(page_width - 8, 7, "Переклад:")
            pdf.set_font("DejaVu", size=11)
            pdf.set_x(left_indent)
            pdf.multi_cell(page_width - 8, 7, translation)

        # 🔹 Походження
        if origin:
            pdf.set_font("DejaVu", "B", size=11)
            pdf.set_x(left_indent)
            pdf.multi_cell(page_width - 8, 7, "Походження:")
            pdf.set_font("DejaVu", size=11)
            pdf.set_x(left_indent)
            pdf.multi_cell(page_width - 8, 7, origin)

        # 🔹 Примітка
        if note:
            pdf.set_font("DejaVu", "B", size=11)
            pdf.set_x(left_indent)
            pdf.multi_cell(page_width - 8, 7, "Примітка:")
            pdf.set_font("DejaVu", size=11)
            pdf.set_x(left_indent)
            pdf.multi_cell(page_width - 8, 7, note)

        # 🔹 Аудіо
        if audio:
            pdf.set_font("DejaVu", "B", size=11)
            pdf.set_x(left_indent)
            pdf.multi_cell(page_width - 8, 7, "Аудіо:")
            pdf.set_font("DejaVu", size=11)
            pdf.set_x(left_indent)
            pdf.multi_cell(page_width - 8, 7, audio)

        # 🔹 Отступ и разделительная линия
        pdf.ln(3)
        y = pdf.get_y()
        pdf.set_draw_color(210, 210, 210)
        pdf.line(pdf.l_margin, y, pdf.w - pdf.r_margin, y)
        pdf.ln(6)

    # Сохраняем PDF
    pdf.output(file_path)
    messagebox.showinfo("Успіх", f"PDF збережено: {file_path}")

def sort_and_dedupe():
    seen = set()
    unique = []
    for w in slang_words:
        key = w.get("word", "").strip()
        if key and key not in seen:
            seen.add(key)
            unique.append(w)
    unique.sort(key=lambda x: x.get("word","").lower())
    slang_words[:] = unique
    save_json(JSON_FILE, slang_words)
    populate_listbox(search_var.get().strip())
    messagebox.showinfo("Сортування", "Словник відсортовано та дублікати видалено.")

# ------------------------ Кнопки ------------------------
buttons_frame = tk.Frame(root)
buttons_frame.grid(row=2, column=0, columnspan=2, sticky="we", padx=10, pady=(0,10))

btn_play = tk.Button(buttons_frame, text="▶ Відтворити аудіо", width=18,
                     command=lambda: play_audio_for_entry(getattr(root, "selected_entry", None)))
btn_play.pack(side="left", padx=6)

btn_test = tk.Button(buttons_frame, text="🎯 Пройти тест", width=14,
                     command=lambda: open_test_window(root, slang_words))
btn_test.pack(side="left", padx=6)


btn_save = tk.Button(buttons_frame, text="💾 Зберегти слово", width=14, command=save_current_word)
btn_save.pack(side="left", padx=6)

btn_add = tk.Button(buttons_frame, text="✚ Додати нове", width=14, command=add_new_word_prompt)
btn_add.pack(side="left", padx=6)

btn_delete = tk.Button(buttons_frame, text="🗑 Видалити", width=12, command=delete_selected_word)
btn_delete.pack(side="left", padx=6)

btn_sort = tk.Button(buttons_frame, text="⇅ Сортувати", width=10, command=sort_and_dedupe)
btn_sort.pack(side="left", padx=6)

btn_backup = tk.Button(buttons_frame, text="Backup JSON", width=12, command=backup_json)
btn_backup.pack(side="left", padx=6)

btn_export_pdf = tk.Button(buttons_frame, text="Експорт у PDF", width=14, command=export_to_pdf)
btn_export_pdf.pack(side="left", padx=6)


btn_exit = tk.Button(buttons_frame, text="Вихід", width=10, command=root.quit)
btn_exit.pack(side="right", padx=6)

# ------------------------ Подвійний клік на елемент ------------------------
def on_double_click(event):
    sel = listbox.curselection()
    if not sel:
        return
    idx = sel[0]
    entry = current_list[idx]
    show_word()
    play_audio_for_entry(entry)

listbox.bind("<Double-Button-1>", on_double_click)

# ------------------------ Ініціалізація ------------------------
if current_list:
    listbox.selection_set(0)
    listbox.event_generate("<<ListboxSelect>>")

# ------------------------ Запуск головного циклу ------------------------
root.mainloop()
