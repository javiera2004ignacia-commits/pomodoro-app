import sys
import os
import ctypes
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QGridLayout, QPushButton, QLineEdit, QMessageBox, QSizePolicy,
    QStackedLayout, QFrame, QCheckBox, QSystemTrayIcon
)
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtMultimedia import QSound


# ----------------- CONFIG -----------------
PINK = "#ff8991"
RED = "#740118"
GREEN = "#8dffaa"
YELLOW = "#fcf49d"
FONT_NAME = "Arial Rounded MT Bold"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 15
CYCLES_BEFORE_LONG_BREAK = 4


def resource_path(relative_path):
    """Acceso seguro a recursos (compatible con PyInstaller)."""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)

    return os.path.join(os.path.dirname(__file__), relative_path)


# ----------------- VENTANA -----------------
class PomodoroWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Icono principal
        icon_path = resource_path("tomato.ico")
        self.setWindowIcon(QIcon(icon_path))

        # Icono de bandeja del sistema
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(icon_path))
        self.tray_icon.setVisible(True)

        self.setStyleSheet("background-color: #fcf49d;")

        # Estado
        self.reps = 0
        self.time_left = 0
        self.total_cycles = CYCLES_BEFORE_LONG_BREAK
        self.remaining_cycles = self.total_cycles

        # Timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.count_down)

        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)

        # Título
        self.title_label = QLabel("Pomodoro")
        self.title_label.setFont(QFont(FONT_NAME, 40, QFont.Bold))
        self.title_label.setStyleSheet(f"color:{RED};")
        self.title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.title_label)

        # Imagen y timer
        tomato_frame = QFrame()
        tomato_frame.setFixedSize(400, 400)

        self.tomato_label = QLabel(tomato_frame)
        self.tomato_label.setGeometry(0, 0, 400, 400)
        pixmap = QPixmap(resource_path("tomato.png")).scaled(
            400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        self.tomato_label.setPixmap(pixmap)
        self.tomato_label.setAlignment(Qt.AlignCenter)

        self.timer_label = QLabel(tomato_frame)
        self.timer_label.setGeometry(0, 40, 400, 400)
        self.timer_label.setFont(QFont(FONT_NAME, 35, QFont.Bold))
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setStyleSheet("color: #740118; background: transparent;")
        self.timer_label.setVisible(False)

        tomato_container = QHBoxLayout()
        tomato_container.addWidget(tomato_frame, alignment=Qt.AlignCenter)
        main_layout.addLayout(tomato_container)

        # Entradas
        self.create_entries(main_layout)

        # Botones
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(20)

        self.start_btn = self.make_button("Start", "button_icons/start.png", self.start_timer)
        self.apply_btn = self.make_button("Aplicar", "button_icons/apply.png", self.apply_times)
        self.reset_btn = self.make_button("Reset", "button_icons/reset.png", self.reset_timer)

        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(self.apply_btn)
        btn_layout.addWidget(self.reset_btn)

        # Ciclos visuales
        self.check_label = QLabel("🍅" * self.remaining_cycles)
        self.check_label.setFont(QFont(FONT_NAME, 18, QFont.Bold))
        self.check_label.setStyleSheet(f"color:{GREEN}; background:{YELLOW};")
        self.check_label.setAlignment(Qt.AlignCenter)

        # Checkbox auto-ciclo
        self.auto_next_checkbox = QCheckBox("Auto ciclo")
        self.auto_next_checkbox.setFont(QFont(FONT_NAME, 14))
        self.auto_next_checkbox.setStyleSheet(f"color:{RED}; background:{YELLOW};")

        cycle_layout = QHBoxLayout()
        cycle_layout.addWidget(self.check_label)
        cycle_layout.addWidget(self.auto_next_checkbox)

        main_layout.addLayout(cycle_layout)
        main_layout.addLayout(btn_layout)

        self.setLayout(main_layout)

    # ---------- FUNCIONES ----------
    def create_entries(self, layout):
        label_font = QFont(FONT_NAME, 12, QFont.Bold)
        entry_font = QFont(FONT_NAME, 14, QFont.Bold)

        grid = QGridLayout()

        self.work_entry = QLineEdit(str(WORK_MIN))
        self.short_break_entry = QLineEdit(str(SHORT_BREAK_MIN))
        self.long_break_entry = QLineEdit(str(LONG_BREAK_MIN))
        self.cycles_entry = QLineEdit(str(CYCLES_BEFORE_LONG_BREAK))

        entries = [self.work_entry, self.short_break_entry, self.long_break_entry, self.cycles_entry]

        for e in entries:
            e.setFont(entry_font)
            e.setAlignment(Qt.AlignCenter)
            e.setFixedSize(200, 50)
            e.setStyleSheet(f"background:{PINK}; color:{RED}; border:none; border-radius:10px;")

        labels = ["Trabajo", "Un Ratito", "Un Rato", "Ciclos"]
        for i, text in enumerate(labels):
            label = QLabel(text)
            label.setFont(label_font)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet(f"color:{RED}; background:{YELLOW};")
            grid.addWidget(label, (i // 2) * 2, i % 2)

        grid.addWidget(self.work_entry, 1, 0)
        grid.addWidget(self.short_break_entry, 1, 1)
        grid.addWidget(self.long_break_entry, 3, 0)
        grid.addWidget(self.cycles_entry, 3, 1)

        layout.addLayout(grid)

    def make_button(self, text, icon_rel, callback):
        btn = QPushButton(text)
        btn.setFont(QFont(FONT_NAME, 16, QFont.Bold))
        btn.setFixedSize(200, 80)

        icon_path = resource_path(icon_rel)
        if os.path.exists(icon_path):
            btn.setIcon(QIcon(icon_path))
            btn.setIconSize(QSize(40, 40))

        btn.clicked.connect(callback)

        btn.setStyleSheet(f"""
        QPushButton {{
            background-color: {GREEN};
            color: {RED};
            border: none;
            border-radius: 15px;
        }}
        QPushButton:hover {{
            background-color: {YELLOW};
        }}
        """)

        return btn

    def update_tomatoes(self):
        self.check_label.setText("🍅" * self.remaining_cycles)

    def apply_times(self):
        try:
            self.work_min = int(self.work_entry.text())
            self.short_break_min = int(self.short_break_entry.text())
            self.long_break_min = int(self.long_break_entry.text())
            self.cycles_before_long_break = int(self.cycles_entry.text())
            self.total_cycles = self.cycles_before_long_break
            self.remaining_cycles = self.total_cycles
            self.update_tomatoes()
        except ValueError:
            QMessageBox.warning(self, "Error", "Por favor ingresa solo números enteros.")

    def reset_timer(self):
        self.timer.stop()
        self.reps = 0
        self.time_left = 0
        self.timer_label.setText("00:00")
        self.title_label.setText("Pomodoro")
        self.remaining_cycles = self.total_cycles
        self.update_tomatoes()
        self.start_btn.setEnabled(True)
        self.timer_label.setVisible(False)

    def start_timer(self):
        self.apply_times()
        self.reps += 1

        work_sec = self.work_min * 60
        short_break_sec = self.short_break_min * 60
        long_break_sec = self.long_break_min * 60

        # Ciclos
        if self.reps % 4 == 0:
            self.time_left = long_break_sec
            self.title_label.setText("Un Rato")
            self.notify("⏰ Descanso largo", "Tómate un buen descanso 🍵")
            QSound.play(resource_path("descanso.mp3"))
        elif self.reps % 2 == 0:
            self.time_left = short_break_sec
            self.title_label.setText("Un Ratito")
            self.notify("☕ Descanso corto", "Tómate un ratito ✨")
            QSound.play(resource_path("descanso.mp3"))
        else:
            self.time_left = work_sec
            self.title_label.setText("Trabajo")
            self.notify("🍅 Pomodoro", "¡Enfócate en la tarea!")

        self.start_btn.setEnabled(False)
        self.timer_label.setVisible(True)
        self.count_down()

    def count_down(self):
        minutes = self.time_left // 60
        seconds = self.time_left % 60
        self.timer_label.setText(f"{minutes:02d}:{seconds:02d}")

        if self.time_left > 0:
            self.time_left -= 1
            self.timer.start(1000)
            return

        # Tiempo terminado
        self.timer.stop()
        self.remaining_cycles = max(0, self.remaining_cycles - 1)
        self.update_tomatoes()

        # Auto-siguiente
        if self.auto_next_checkbox.isChecked():
            self.start_timer()
        else:
            self.start_btn.setEnabled(True)
            self.timer_label.setVisible(False)

    def notify(self, title, message):
        self.tray_icon.showMessage(title, message, QIcon(resource_path("tomato.ico")), 4000)


# ----------------- EJECUTAR -----------------
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Icono barra de tareas Windows
    if sys.platform.startswith("win"):
        myappid = "pomodoro.timer.2025"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    window = PomodoroWindow()
    window.show()

    sys.exit(app.exec_())
