import json
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPixmap, QPainter, QPainterPath
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
    QSizePolicy,
)


class CardWidget(QFrame):
    def __init__(self, title: str, value: str):
        super().__init__()
        self.setObjectName("card")
        self.setMinimumHeight(120)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(8)

        self.title_label = QLabel(title)
        self.title_label.setObjectName("cardTitle")

        self.value_label = QLabel(value)
        self.value_label.setObjectName("cardValue")

        layout.addWidget(self.title_label)
        layout.addWidget(self.value_label)
        layout.addStretch()

    def set_value(self, value: str) -> None:
        self.value_label.setText(value)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GESTOR DE TAREAS")
        self.resize(1280, 800)

        self.base_path = Path(__file__).resolve().parent.parent
        self.tareas_path = self.base_path / "tareas.json"
        self.avatar_path = self.base_path / "assets" / "user.png"
        self.background_path = self.base_path / "assets" / "fondo.png"

        self.tareas = []

        self._build_ui()
        self._apply_content_background()
        self._load_tareas()
        self._refresh_lista()
        self._update_cards()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._apply_content_background()

    def _build_ui(self) -> None:
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        root_layout = QHBoxLayout(central_widget)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        sidebar = self._create_sidebar()
        content = self._create_content()

        root_layout.addWidget(sidebar)
        root_layout.addWidget(content, 1)

    def _create_sidebar(self) -> QFrame:
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(250)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(20, 24, 20, 24)
        layout.setSpacing(14)

        logo = QLabel("Gestor de\nTareas")
        logo.setObjectName("logo")
        logo.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        layout.addWidget(logo)
        layout.addSpacing(10)

        self.btn_inicio = QPushButton("Inicio")
        self.btn_inicio.setCursor(Qt.PointingHandCursor)
        self.btn_inicio.setProperty("active", True)
        self.btn_inicio.clicked.connect(self.show_inicio)

        self.btn_tareas = QPushButton("Tareas")
        self.btn_tareas.setCursor(Qt.PointingHandCursor)
        self.btn_tareas.clicked.connect(self.show_tareas)

        self.btn_salir = QPushButton("Salir")
        self.btn_salir.setCursor(Qt.PointingHandCursor)
        self.btn_salir.clicked.connect(self.close)

        layout.addWidget(self.btn_inicio)
        layout.addWidget(self.btn_tareas)

        layout.addStretch()
        layout.addWidget(self.btn_salir)

        return sidebar

    def _create_content(self) -> QWidget:
        self.content_area = QWidget()
        self.content_area.setObjectName("contentArea")

        layout = QVBoxLayout(self.content_area)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(24)

        header = self._create_header()

        self.stack = QStackedWidget()
        self.stack.setObjectName("contentStack")

        self.page_inicio = self._create_inicio_page()
        self.page_tareas = self._create_tareas_page()

        self.stack.addWidget(self.page_inicio)
        self.stack.addWidget(self.page_tareas)

        layout.addWidget(header)
        layout.addWidget(self.stack, 1)

        return self.content_area

    def _apply_content_background(self) -> None:
        if not hasattr(self, "content_area"):
            return

        if not self.background_path.exists():
            return

        image_path = self.background_path.as_posix()

        self.content_area.setStyleSheet(
            f"""
            QWidget#contentArea {{
                background-image: url("{image_path}");
                background-position: center;
                background-repeat: no-repeat;
            }}
            """
        )

    def _create_header(self) -> QFrame:
        header = QFrame()
        header.setObjectName("header")

        layout = QHBoxLayout(header)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(12)

        title_box = QVBoxLayout()
        title_box.setSpacing(4)

        self.title = QLabel("PANEL PRINCIPAL")
        self.title.setObjectName("mainTitle")

        self.subtitle = QLabel("Organizá tus tareas de forma simple")
        self.subtitle.setObjectName("subTitle")

        title_box.addWidget(self.title)
        title_box.addWidget(self.subtitle)

        layout.addLayout(title_box)
        layout.addStretch()

        self.profile = QLabel()
        self.profile.setObjectName("profileBadge")
        self.profile.setAlignment(Qt.AlignCenter)
        self.profile.setFixedSize(52, 52)

        self._set_avatar()

        layout.addWidget(self.profile)

        return header

    def _set_avatar(self) -> None:
        if self.avatar_path.exists():
            circular = self._create_circular_pixmap(str(self.avatar_path), 40)
            self.profile.setPixmap(circular)
            return

        self.profile.setText("J")

    def _create_circular_pixmap(self, image_path: str, size: int) -> QPixmap:
        original = QPixmap(image_path)
        if original.isNull():
            fallback = QPixmap(size, size)
            fallback.fill(Qt.transparent)
            return fallback

        scaled = original.scaled(
            size,
            size,
            Qt.KeepAspectRatioByExpanding,
            Qt.SmoothTransformation,
        )

        circular = QPixmap(size, size)
        circular.fill(Qt.transparent)

        painter = QPainter(circular)
        painter.setRenderHint(QPainter.Antialiasing)

        path = QPainterPath()
        path.addEllipse(0, 0, size, size)
        painter.setClipPath(path)

        x = (scaled.width() - size) // 2
        y = (scaled.height() - size) // 2
        painter.drawPixmap(-x, -y, scaled)
        painter.end()

        return circular

    def _create_inicio_page(self) -> QWidget:
        page = QWidget()
        page.setObjectName("pageInicio")

        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(24)

        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(18)

        self.card_total = CardWidget("Total de tareas", "0")
        self.card_pendientes = CardWidget("Pendientes", "0")
        self.card_completadas = CardWidget("Completadas", "0")

        cards_layout.addWidget(self.card_total)
        cards_layout.addWidget(self.card_pendientes)
        cards_layout.addWidget(self.card_completadas)

        panel = QFrame()
        panel.setObjectName("mainPanel")

        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(24, 24, 24, 24)
        panel_layout.setSpacing(12)

        title = QLabel("Versión 20.00")
        title.setObjectName("panelTitle")

        text = QLabel(
            "Este sistema fue diseñado para que puedas agregar, ver, editar, completar y eliminar tareas.\n"
            "Con más de diez pruebas de diseño, organización y código esta es la versión número 20.\n"
            "Para conocer más información sobre este proyecto creado por mí Joaquin Gonzalez"
            "Podes visitar mi portfolio de Github github.com/joagonzalez26/"
        )
        text.setObjectName("panelText")
        text.setWordWrap(True)

        button = QPushButton("Ir a Tareas")
        button.setCursor(Qt.PointingHandCursor)
        button.clicked.connect(self.show_tareas)

        panel_layout.addWidget(title)
        panel_layout.addWidget(text)
        panel_layout.addSpacing(10)
        panel_layout.addWidget(button, alignment=Qt.AlignLeft)
        panel_layout.addStretch()

        layout.addLayout(cards_layout)
        layout.addWidget(panel, 1)

        return page

    def _create_tareas_page(self) -> QWidget:
        page = QWidget()
        page.setObjectName("pageTareas")

        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)

        top_panel = QFrame()
        top_panel.setObjectName("mainPanel")

        top_layout = QVBoxLayout(top_panel)
        top_layout.setContentsMargins(24, 24, 24, 24)
        top_layout.setSpacing(14)

        form_title = QLabel("Administrar tareas")
        form_title.setObjectName("panelTitle")

        self.input_tarea = QLineEdit()
        self.input_tarea.setPlaceholderText("Escribí una tarea...")

        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(12)

        btn_agregar = QPushButton("Agregar")
        btn_agregar.clicked.connect(self.agregar_tarea)

        btn_editar = QPushButton("Editar")
        btn_editar.clicked.connect(self.editar_tarea)

        btn_eliminar = QPushButton("Eliminar")
        btn_eliminar.clicked.connect(self.eliminar_tarea)

        btn_completar = QPushButton("Completar")
        btn_completar.clicked.connect(self.completar_tarea)

        buttons_layout.addWidget(btn_agregar)
        buttons_layout.addWidget(btn_editar)
        buttons_layout.addWidget(btn_eliminar)
        buttons_layout.addWidget(btn_completar)
        buttons_layout.addStretch()

        top_layout.addWidget(form_title)
        top_layout.addWidget(self.input_tarea)
        top_layout.addLayout(buttons_layout)

        list_panel = QFrame()
        list_panel.setObjectName("mainPanel")

        list_layout = QVBoxLayout(list_panel)
        list_layout.setContentsMargins(24, 24, 24, 24)
        list_layout.setSpacing(12)

        list_title = QLabel("Lista de tareas")
        list_title.setObjectName("panelTitle")

        self.lista_tareas = QListWidget()
        self.lista_tareas.setObjectName("taskList")
        self.lista_tareas.itemClicked.connect(self.cargar_tarea_seleccionada)

        list_layout.addWidget(list_title)
        list_layout.addWidget(self.lista_tareas)

        layout.addWidget(top_panel)
        layout.addWidget(list_panel, 1)

        return page

    def show_inicio(self) -> None:
        self.stack.setCurrentWidget(self.page_inicio)
        self.title.setText("Panel de inicio")
        self.subtitle.setText("Organizá tus tareas de forma simple")
        self._set_active_button(self.btn_inicio)

    def show_tareas(self) -> None:
        self.stack.setCurrentWidget(self.page_tareas)
        self.title.setText("Gestión de tareas")
        self.subtitle.setText("Agregá, editá, completá y eliminá tus tareas")
        self._set_active_button(self.btn_tareas)

    def _set_active_button(self, active_button: QPushButton) -> None:
        for button in [self.btn_inicio, self.btn_tareas]:
            button.setProperty("active", button == active_button)
            button.style().unpolish(button)
            button.style().polish(button)

    def _load_tareas(self) -> None:
        if not self.tareas_path.exists():
            self._save_tareas()
            return

        try:
            with open(self.tareas_path, "r", encoding="utf-8") as archivo:
                data = json.load(archivo)

            if isinstance(data, list):
                self.tareas = data
            else:
                self.tareas = []

        except (json.JSONDecodeError, OSError):
            self.tareas = []

    def _save_tareas(self) -> None:
        try:
            with open(self.tareas_path, "w", encoding="utf-8") as archivo:
                json.dump(self.tareas, archivo, indent=4, ensure_ascii=False)
        except OSError:
            QMessageBox.critical(self, "Error", "No se pudieron guardar las tareas.")

    def _refresh_lista(self) -> None:
        self.lista_tareas.clear()

        for tarea in self.tareas:
            texto = tarea["texto"]
            item = QListWidgetItem()

            if tarea["completada"]:
                item.setText(f"✔ {texto}")
                item.setForeground(QColor("#7f8ca3"))
                font = item.font()
                font.setStrikeOut(True)
                item.setFont(font)
            else:
                item.setText(texto)
                item.setForeground(QColor("#e8eef8"))

            self.lista_tareas.addItem(item)

    def agregar_tarea(self) -> None:
        texto = self.input_tarea.text().strip()

        if not texto:
            QMessageBox.warning(self, "Atención", "Escribí una tarea antes de agregar.")
            return

        self.tareas.append({"texto": texto, "completada": False})
        self._save_tareas()
        self._refresh_lista()
        self._update_cards()
        self.input_tarea.clear()

    def editar_tarea(self) -> None:
        fila = self.lista_tareas.currentRow()
        nuevo_texto = self.input_tarea.text().strip()

        if fila < 0:
            QMessageBox.warning(self, "Atención", "Seleccioná una tarea para editar.")
            return

        if not nuevo_texto:
            QMessageBox.warning(self, "Atención", "Escribí el nuevo texto de la tarea.")
            return

        self.tareas[fila]["texto"] = nuevo_texto
        self._save_tareas()
        self._refresh_lista()
        self._update_cards()
        self.input_tarea.clear()

    def eliminar_tarea(self) -> None:
        fila = self.lista_tareas.currentRow()

        if fila < 0:
            QMessageBox.warning(self, "Atención", "Seleccioná una tarea para eliminar.")
            return

        self.tareas.pop(fila)
        self._save_tareas()
        self._refresh_lista()
        self._update_cards()
        self.input_tarea.clear()

    def completar_tarea(self) -> None:
        fila = self.lista_tareas.currentRow()

        if fila < 0:
            QMessageBox.warning(self, "Atención", "Seleccioná una tarea.")
            return

        self.tareas[fila]["completada"] = not self.tareas[fila]["completada"]
        self._save_tareas()
        self._refresh_lista()
        self._update_cards()
        self.input_tarea.clear()

    def cargar_tarea_seleccionada(self, _item=None) -> None:
        fila = self.lista_tareas.currentRow()
        if fila >= 0:
            self.input_tarea.setText(self.tareas[fila]["texto"])

    def _update_cards(self) -> None:
        total = len(self.tareas)
        completadas = sum(1 for tarea in self.tareas if tarea["completada"])
        pendientes = total - completadas

        self.card_total.set_value(str(total))
        self.card_pendientes.set_value(str(pendientes))
        self.card_completadas.set_value(str(completadas))