import tkinter as tk
import math
from plyer import notification

# ---------------------------- CONSTANTES ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 1          # cambia a 25 cuando ya no estés probando
SHORT_BREAK_MIN = 1   # cambia a 5
LONG_BREAK_MIN = 2    # cambia a 15
reps = 0
timer = None

# ---------------------------- FUNCIONES DE NOTIFICACIÓN ------------------------------- #
def notificar(titulo, mensaje):
    """Muestra una notificación en el escritorio"""
    notification.notify(
        title=titulo,
        message=mensaje,
        timeout=5
    )

# ---------------------------- RESET ------------------------------- #
def reset_timer():
    global reps
    window.after_cancel(timer)
    reps = 0
    canvas.itemconfig(timer_text, text="00:00")
    title_label.config(text="Pomodoro", fg=GREEN)
    check_marks.config(text="")

# ---------------------------- INICIO DEL TIMER ------------------------------- #
def start_timer():
    global reps
    reps += 1

    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if reps % 8 == 0:
        count_down(long_break_sec)
        title_label.config(text="Un Rato", fg=RED)
        notificar("Pomodoro 🍅", "¡Hora de un descanso!<3")
    elif reps % 2 == 0:
        count_down(short_break_sec)
        title_label.config(text="Un Ratito", fg=PINK)
        notificar("Pomodoro 🍅", "Tómate un descanso!<3")
    else:
        count_down(work_sec)
        title_label.config(text="Trabajo", fg=GREEN)
        notificar("Pomodoro 🍅", "¡Es hora de concentrarse!")

# ---------------------------- CUENTA REGRESIVA ------------------------------- #
def count_down(count):
    minutes = math.floor(count / 60)
    seconds = count % 60
    if seconds < 10:
        seconds = f"0{seconds}"
    canvas.itemconfig(timer_text, text=f"{minutes}:{seconds}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        start_timer()
        marks = ""
        work_sessions = math.floor(reps/2)
        for _ in range(work_sessions):
            marks += "✔"
        check_marks.config(text=marks)

# ---------------------------- UI ------------------------------- #
window = tk.Tk()
window.title("Pomodoro Timer 🍅")
window.config(padx=100, pady=50, bg=YELLOW)

title_label = tk.Label(text="Pomodoro", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 40, "bold"))
title_label.grid(column=1, row=0)

canvas = tk.Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = tk.PhotoImage(file="tomato.png")  # Necesitas un archivo tomato.png
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

start_button = tk.Button(text="Start", command=start_timer)
start_button.grid(column=0, row=2)

reset_button = tk.Button(text="Reset", command=reset_timer)
reset_button.grid(column=2, row=2)

check_marks = tk.Label(fg=GREEN, bg=YELLOW, font=(FONT_NAME, 14))
check_marks.grid(column=1, row=3)

window.mainloop()