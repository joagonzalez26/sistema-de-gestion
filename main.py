import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow


def load_stylesheet(app: QApplication) -> None:
    style_path = Path(__file__).parent / "styles" / "style.qss"

    if style_path.exists():
        with open(style_path, "r", encoding="utf-8") as file:
            app.setStyleSheet(file.read())


def main() -> None:
    app = QApplication(sys.argv)
    app.setApplicationName("Gestor de tareas V.20")

    load_stylesheet(app)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()