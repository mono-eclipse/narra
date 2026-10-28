from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QTextEdit,
    QSpinBox,
    QFormLayout,
    QDialogButtonBox,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QStackedWidget,
    QFrame,
    QHeaderView,
    QComboBox,
    QAbstractItemView,
)


class ProjectDialog(QDialog):
    def __init__(self, parent=None, project=None):
        super().__init__(parent)

        self.project = project
        self.setWindowTitle(
            "Редактирование проекта"
            if project else "Новый проект"
        )
        self.setMinimumWidth(420)

        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.name_input = QLineEdit()
        self.type_input = QLineEdit()
        self.genre_input = QLineEdit()
        self.status_input = QLineEdit()

        self.name_input.setPlaceholderText(
            "Название проекта"
        )
        self.type_input.setPlaceholderText(
            "Например, Видеоигра"
        )
        self.genre_input.setPlaceholderText(
            "Например, Детектив"
        )
        self.status_input.setPlaceholderText(
            "Например, В процессе"
        )

        form.addRow("Название:", self.name_input)
        form.addRow("Тип проекта:", self.type_input)
        form.addRow("Жанр:", self.genre_input)
        form.addRow("Статус:", self.status_input)

        layout.addLayout(form)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.validate_and_accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        if project:
            self.name_input.setText(project[1] or "")
            self.type_input.setText(project[2] or "")
            self.genre_input.setText(project[3] or "")
            self.status_input.setText(project[4] or "")

    def validate_and_accept(self):
        if not self.name_input.text().strip():
            QMessageBox.warning(
                self,
                "Не заполнено название",
                "Введи название проекта."
            )
            return

        self.accept()

    def get_data(self):
        return (
            self.name_input.text().strip(),
            self.type_input.text().strip() or None,
            self.genre_input.text().strip() or None,
            self.status_input.text().strip() or None,
        )


class MaterialDialog(QDialog):
    """Форма добавления материала."""

    def __init__(self, projects, material_types, parent=None, initial_data=None):
        super().__init__(parent)

        self.initial_data = initial_data
        self.setWindowTitle("Редактировать материал" if initial_data else "Добавить материал")
        self.setMinimumWidth(460)

        self.fields = {}
        self.form = QFormLayout(self)

        self.project_box = QComboBox()
        for project_id, project_name in projects:
            self.project_box.addItem(
                f"{project_name} (ID: {project_id})",
                project_id
            )
        self.form.addRow("Проект:", self.project_box)

        self.type_box = QComboBox()
        for type_id, type_name in material_types:
            self.type_box.addItem(type_name, type_id)
        self.form.addRow("Тип материала:", self.type_box)

        self._add_text("title", "Название:")
        self._add_text("author", "Автор / исполнитель:")
        self._add_text("year", "Год:")
        self._add_text("genre", "Жанр:")

        self.description = QTextEdit()
        self.description.setMaximumHeight(90)
        self.form.addRow("Описание:", self.description)

        self.type_fields = {
            1: [
                ("Исполнитель", "artist"),
                ("Автор текста", "lyric_author"),
                ("Альбом", "album"),
                ("Направление музыки", "direction"),
            ],
            2: [
                ("Режиссер", "director"),
                ("Сценарист", "screenwriter"),
                ("Продюсер", "producer"),
                ("Статус просмотра", "watch_status"),
            ],
            3: [
                ("Режиссер", "director"),
                ("Сценарист", "screenwriter"),
                ("Продюсер", "producer"),
                ("Статус сериала", "series_status"),
                ("Статус просмотра", "watch_status"),
            ],
            4: [
                ("Статус книги", "book_status"),
            ],
            5: [
                ("Студия-разработчик", "studio"),
                ("Ведущий сценарист", "lead_writer"),
                ("Нарративный дизайнер", "narrative_designer"),
                ("Статус игры", "game_status"),
            ],
        }

        self.extra_widgets = {}

        self.type_box.currentIndexChanged.connect(
            self._update_type_fields
        )

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.form.addRow(self.buttons)

        self._update_type_fields()

        if initial_data:
            self.project_box.setCurrentIndex(
                max(0, self.project_box.findData(initial_data.get("project_id")))
            )
            self.type_box.setCurrentIndex(
                max(0, self.type_box.findData(initial_data.get("type_id")))
            )
            self.type_box.setEnabled(False)
            self._update_type_fields()

            self.fields["title"].setText(initial_data.get("title") or "")
            self.fields["author"].setText(initial_data.get("author") or "")
            self.fields["year"].setText(
                "" if initial_data.get("year") is None else str(initial_data.get("year"))
            )
            self.fields["genre"].setText(initial_data.get("genre") or "")
            self.description.setPlainText(initial_data.get("description") or "")

            for key, value in initial_data.get("extra", {}).items():
                widget = self.extra_widgets.get(key)
                if isinstance(widget, QSpinBox):
                    widget.setValue(int(value or 0))
                elif widget is not None:
                    widget.setText("" if value is None else str(value))

    def _add_text(self, key, label):
        widget = QLineEdit()
        self.fields[key] = widget
        self.form.addRow(label, widget)

    def _update_type_fields(self, *_):
        # Удаляем ранее показанные дополнительные поля.
        for widget in list(self.extra_widgets.values()):
            self.form.removeRow(widget)

        self.extra_widgets.clear()
        type_id = self.type_box.currentData()

        for label, key in self.type_fields.get(type_id, []):
            widget = QLineEdit()
            self.extra_widgets[key] = widget
            self.form.insertRow(
                self.form.rowCount() - 1,
                label,
                widget
            )

        if type_id == 3:
            widget = QSpinBox()
            widget.setRange(0, 999)
            self.extra_widgets["seasons"] = widget
            self.form.insertRow(
                self.form.rowCount() - 1,
                "Количество сезонов:",
                widget
            )

    def get_data(self):
        year_text = self.fields["year"].text().strip()
        year = int(year_text) if year_text else None

        extra = {}
        for key, widget in self.extra_widgets.items():
            if isinstance(widget, QSpinBox):
                extra[key] = widget.value()
            else:
                extra[key] = widget.text().strip() or None

        return {
            "project_id": self.project_box.currentData(),
            "type_id": self.type_box.currentData(),
            "title": self.fields["title"].text().strip(),
            "author": self.fields["author"].text().strip() or None,
            "year": year,
            "genre": self.fields["genre"].text().strip() or None,
            "description": self.description.toPlainText().strip() or None,
            "extra": extra,
        }


class MainWindow(QMainWindow):
    def __init__(self, connection, username):
        super().__init__()

        self.connection = connection
        self.username = username
        self.current_material_project_id = None

        self.setWindowTitle("Мои проекты")
        self.resize(1200, 750)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #f4f6fa;
            }
            QLabel {
                color: #202633;
            }
            QPushButton {
                padding: 8px 14px;
                border: 1px solid #d7dce5;
                border-radius: 6px;
                background-color: white;
            }
            QPushButton:hover {
                background-color: #e9edf5;
            }
            QLineEdit, QComboBox {
                padding: 9px;
                border: 1px solid #d7dce5;
                border-radius: 6px;
                background-color: white;
            }
            QTableWidget {
                background-color: white;
                alternate-background-color: #f6f8fc;
                border: 1px solid #e0e5ed;
                border-radius: 6px;
                gridline-color: #e8ebf1;
            }
            QHeaderView::section {
                background-color: #e9edf5;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """)

        central = QWidget()
        self.setCentralWidget(central)

        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Боковое меню
        sidebar = QFrame()
        sidebar.setFixedWidth(210)
        sidebar.setStyleSheet("""
            QFrame {
                background-color: #202633;
            }
            QLabel {
                color: white;
            }
            QPushButton {
                color: white;
                text-align: left;
                padding: 12px;
                border: none;
                border-radius: 6px;
                background-color: transparent;
            }
            QPushButton:hover {
                background-color: #343e50;
            }
        """)

        side_layout = QVBoxLayout(sidebar)

        title = QLabel("МОИ ПРОЕКТЫ")
        title.setStyleSheet(
            "font-size: 19px; font-weight: bold; padding: 16px;"
        )
        side_layout.addWidget(title)

        self.projects_button = QPushButton("  Проекты")
        self.materials_button = QPushButton("  Материалы")

        side_layout.addWidget(self.projects_button)
        side_layout.addWidget(self.materials_button)
        side_layout.addStretch()

        self.user_label = QLabel(f"Вход: {username}")
        self.user_label.setWordWrap(True)
        self.user_label.setStyleSheet("padding: 12px;")
        side_layout.addWidget(self.user_label)

        root.addWidget(sidebar)

        # Страницы приложения
        self.pages = QStackedWidget()
        root.addWidget(self.pages, 1)

        self._create_projects_page()
        self._create_materials_page()

        self.projects_button.clicked.connect(
            lambda: self.pages.setCurrentIndex(0)
        )
        self.materials_button.clicked.connect(
            self.show_all_materials
        )

        self.load_projects()
        self.load_material_types()
        self.load_materials()

    def _create_projects_page(self):
        self.projects_page = QWidget()
        layout = QVBoxLayout(self.projects_page)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(14)

        heading = QLabel("Проекты")
        heading.setStyleSheet(
            "font-size: 27px; font-weight: bold;"
        )
        layout.addWidget(heading)

        toolbar = QHBoxLayout()

        self.project_search = QLineEdit()
        self.project_search.setPlaceholderText(
            "Поиск проектов..."
        )
        self.project_search.textChanged.connect(
            self.filter_projects
        )

        refresh_button = QPushButton("Обновить")
        refresh_button.clicked.connect(self.load_projects)

        add_button = QPushButton("Добавить проект")
        add_button.clicked.connect(self.add_project)

        edit_button = QPushButton("Редактировать")
        edit_button.clicked.connect(self.edit_project)

        delete_project_button = QPushButton("Удалить проект")
        delete_project_button.clicked.connect(self.delete_project)

        self.project_materials_button = QPushButton(
            "Материалы проекта"
        )
        self.project_materials_button.clicked.connect(
            self.show_selected_project_materials
        )

        toolbar.addWidget(self.project_search, 1)
        toolbar.addWidget(add_button)
        toolbar.addWidget(edit_button)
        toolbar.addWidget(delete_project_button)
        toolbar.addWidget(self.project_materials_button)
        toolbar.addWidget(refresh_button)
        layout.addLayout(toolbar)

        self.projects_table = QTableWidget()
        self._configure_table(self.projects_table)
        self.projects_table.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )
        self.projects_table.itemDoubleClicked.connect(
            lambda item: self.show_selected_project_materials()
        )

        layout.addWidget(self.projects_table, 1)

        self.projects_status = QLabel("Готово")
        layout.addWidget(self.projects_status)

        self.pages.addWidget(self.projects_page)

    def _create_materials_page(self):
        self.materials_page = QWidget()
        layout = QVBoxLayout(self.materials_page)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(14)

        self.materials_heading = QLabel("Материалы")
        self.materials_heading.setStyleSheet(
            "font-size: 27px; font-weight: bold;"
        )
        layout.addWidget(self.materials_heading)

        toolbar = QHBoxLayout()

        self.material_search = QLineEdit()
        self.material_search.setPlaceholderText(
            "Поиск по названию, автору, жанру..."
        )
        self.material_search.textChanged.connect(
            self.filter_materials
        )

        self.material_type_filter = QComboBox()
        self.material_type_filter.addItem("Все типы", None)
        self.material_type_filter.currentIndexChanged.connect(
            self.filter_materials
        )

        self.add_material_button = QPushButton("Добавить материал")
        self.add_material_button.clicked.connect(self.add_material)

        self.edit_material_button = QPushButton("Редактировать")
        self.edit_material_button.clicked.connect(self.edit_material)

        self.delete_material_button = QPushButton("Удалить")
        self.delete_material_button.clicked.connect(self.delete_material)

        refresh_button = QPushButton("Обновить")
        refresh_button.clicked.connect(
            self.refresh_materials
        )

        self.all_materials_button = QPushButton(
            "Все материалы"
        )
        self.all_materials_button.clicked.connect(
            self.show_all_materials
        )

        toolbar.addWidget(self.material_search, 1)
        toolbar.addWidget(self.material_type_filter)
        toolbar.addWidget(self.all_materials_button)
        toolbar.addWidget(self.add_material_button)
        toolbar.addWidget(self.edit_material_button)
        toolbar.addWidget(self.delete_material_button)
        toolbar.addWidget(refresh_button)

        layout.addLayout(toolbar)

        self.materials_table = QTableWidget()
        self._configure_table(self.materials_table)

        layout.addWidget(self.materials_table, 1)

        self.materials_status = QLabel("Готово")
        layout.addWidget(self.materials_status)


        self.pages.addWidget(self.materials_page)

    @staticmethod
    def _configure_table(table):
        table.setAlternatingRowColors(True)
        table.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )
        table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        table.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )
        table.setSortingEnabled(False)
        table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )
        table.horizontalHeader().setStretchLastSection(True)

    @staticmethod
    def _fill_table(table, columns, rows):
        table.setSortingEnabled(False)
        table.clear()
        table.setColumnCount(len(columns))
        table.setHorizontalHeaderLabels(columns)
        table.setRowCount(len(rows))

        for row_index, row in enumerate(rows):
            for column_index, value in enumerate(row):
                text = "" if value is None else str(value)
                item = QTableWidgetItem(text)
                item.setFlags(
                    item.flags() & ~Qt.ItemFlag.ItemIsEditable
                )
                table.setItem(row_index, column_index, item)

        table.setSortingEnabled(True)

    def load_projects(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT
                    [ID проекта],
                    [Наименование проекта],
                    [Тип проекта],
                    [Жанр],
                    [Статус проектов]
                FROM dbo.[Проекты]
                ORDER BY [Порядковый номер]
            """)

            columns = [
                column[0] for column in cursor.description
            ]
            rows = cursor.fetchall()

            self._fill_table(
                self.projects_table, columns, rows
            )
            self.filter_projects(self.project_search.text())

            self.projects_status.setText(
                f"Загружено проектов: {len(rows)}"
            )

        except Exception as error:
            QMessageBox.warning(
                self,
                "Ошибка загрузки проектов",
                f"Не удалось загрузить проекты:\n{error}",
            )

    def filter_projects(self, text=""):
        query = text.casefold().strip()

        for row in range(self.projects_table.rowCount()):
            matches = any(
                query in (
                    self.projects_table.item(row, column).text()
                    if self.projects_table.item(row, column)
                    else ""
                ).casefold()
                for column in range(
                    self.projects_table.columnCount()
                )
            )
            self.projects_table.setRowHidden(row, not matches)


    def add_project(self):
        dialog = ProjectDialog(self)

        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        name, project_type, genre, status = dialog.get_data()

        try:
            cursor = self.connection.cursor()

            # Блокируем таблицу на время получения ID
            # и вставки записи, чтобы избежать гонки ID.
            cursor.execute("""
                SELECT ISNULL(MAX([ID проекта]), 101124) + 1
                FROM dbo.[Проекты] WITH (TABLOCKX, HOLDLOCK)
            """)

            project_id = cursor.fetchone()[0]

            cursor.execute("""
                INSERT INTO dbo.[Проекты]
                    ([ID проекта], [Наименование проекта],
                     [Тип проекта], [Жанр], [Статус проектов])
                VALUES (?, ?, ?, ?, ?)
            """, (
                project_id,
                name,
                project_type,
                genre,
                status,
            ))

            self.connection.commit()
            self.load_projects()

            QMessageBox.information(
                self,
                "Проект добавлен",
                f"Проект «{name}» создан.\nID проекта: {project_id}"
            )

        except Exception as error:
            self.connection.rollback()
            QMessageBox.critical(
                self,
                "Ошибка сохранения",
                f"Не удалось добавить проект:\n{error}"
            )

    def add_material(self):
        """Добавляет материал и запись в соответствующую таблицу."""

        cursor = self.connection.cursor()

        try:
            # Загружаем проекты для выпадающего списка.
            cursor.execute("""
                SELECT [ID проекта], [Наименование проекта]
                FROM dbo.[Проекты]
                ORDER BY [ID проекта]
            """)
            projects = [
                (row[0], row[1] or "Без названия")
                for row in cursor.fetchall()
            ]

            # Загружаем типы материалов.
            cursor.execute("""
                SELECT [ID типа материала], [Наименование материала]
                FROM dbo.[Типы материалов]
                ORDER BY [ID типа материала]
            """)
            material_types = [
                (row[0], row[1])
                for row in cursor.fetchall()
            ]

            if not projects or not material_types:
                QMessageBox.warning(
                    self,
                    "Недостаточно данных",
                    "В базе нет проектов или типов материалов."
                )
                return

            dialog = MaterialDialog(projects, material_types, self)

            if dialog.exec() != QDialog.DialogCode.Accepted:
                return

            data = dialog.get_data()

            if not data["title"]:
                QMessageBox.warning(
                    self, "Проверка данных", "Введите название материала."
                )
                return

            if data["year"] is not None and not (
                    0 <= data["year"] <= 9999
            ):
                QMessageBox.warning(
                    self,
                    "Проверка данных",
                    "Год должен быть числом от 0 до 9999."
                )
                return

            type_id = data["type_id"]

            # Таблица, связанная с выбранным типом материала.
            related_tables = {
                1: "Музыка",
                2: "Фильмы",
                3: "Сериалы",
                4: "Книги",
                5: "Игры",
            }

            related_table = related_tables.get(type_id)
            if related_table is None:
                raise ValueError("Неизвестный тип материала.")

            # Выбираем свободный ID в диапазоне типа.
            # TABLOCKX + HOLDLOCK защищают подбор ID в транзакции.
            base_id = type_id * 10000

            cursor.execute("""
                SELECT ISNULL(MAX([ID материала]), ? - 1)
                FROM dbo.[Материалы] WITH (TABLOCKX, HOLDLOCK)
                WHERE [ID материала] >= ?
                  AND [ID материала] < ?
            """, base_id, base_id, base_id + 10000)

            material_id = cursor.fetchone()[0] + 1

            # Проверяем, что выбранный ID ещё не занят.
            cursor.execute("""
                SELECT COUNT(*)
                FROM dbo.[Материалы]
                WHERE [ID материала] = ?
            """, material_id)

            if cursor.fetchone()[0]:
                raise ValueError(
                    f"ID материала {material_id} уже занят. "
                    "Обнови данные и повтори попытку."
                )

            # 1. Общая запись в Материалы.
            cursor.execute("""
                INSERT INTO dbo.[Материалы]
                    ([ID материала], [ID проекта], [Название],
                     [ID типа материала], [Автор], [Год],
                     [Описание], [Жанр])
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
                           material_id,
                           data["project_id"],
                           data["title"],
                           type_id,
                           data["author"],
                           str(data["year"]) if data["year"] is not None else None,
                           data["description"],
                           data["genre"],
                           )

            extra = data["extra"]
            year = data["year"]

            # 2. Связанная запись в специализированной таблице.
            if type_id == 1:  # Музыка
                cursor.execute("""
                    INSERT INTO dbo.[Музыка]
                        ([ID материала], [Наименование музыки],
                         [Исполнитель], [Автор текста], [Альбом],
                         [Год выпуска], [Направление музыки], [Жанр])
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                               material_id,
                               data["title"],
                               extra.get("artist") or data["author"],
                               extra.get("lyric_author"),
                               extra.get("album"),
                               year,
                               extra.get("direction"),
                               data["genre"],
                               )

            elif type_id == 2:  # Фильм
                cursor.execute("""
                    INSERT INTO dbo.[Фильмы]
                        ([ID материала], [Наименование фильма],
                         [Режиссер], [Сценарист], [Продюсер],
                         [Год выпуска], [Жанр], [Статус просмотра])
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                               material_id,
                               data["title"],
                               extra.get("director"),
                               extra.get("screenwriter"),
                               extra.get("producer"),
                               year,
                               data["genre"],
                               extra.get("watch_status"),
                               )

            elif type_id == 3:  # Сериал
                cursor.execute("""
                    INSERT INTO dbo.[Сериалы]
                        ([ID материала], [Наименование сериала],
                         [Режиссер], [Сценарист], [Продюсер],
                         [Год выпуска], [Жанр], [Количество сезонов],
                         [Статус сериала], [Статус просмотра])
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                               material_id,
                               data["title"],
                               extra.get("director"),
                               extra.get("screenwriter"),
                               extra.get("producer"),
                               year,
                               data["genre"],
                               extra.get("seasons"),
                               extra.get("series_status"),
                               extra.get("watch_status"),
                               )

            elif type_id == 4:  # Книга
                cursor.execute("""
                    INSERT INTO dbo.[Книги]
                        ([ID материала], [Наименование книги],
                         [Автор], [Год написания], [Жанр], [Статус])
                    VALUES (?, ?, ?, ?, ?, ?)
                """,
                               material_id,
                               data["title"],
                               data["author"],
                               year,
                               data["genre"],
                               extra.get("book_status"),
                               )

            elif type_id == 5:  # Игра
                cursor.execute("""
                    INSERT INTO dbo.[Игры]
                        ([ID материала], [Наименование игры],
                         [Студия разработчик], [Ведущий сценарист],
                         [Нарративный дизайнер], [Жанр],
                         [Год выхода], [Статус])
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                               material_id,
                               data["title"],
                               extra.get("studio"),
                               extra.get("lead_writer"),
                               extra.get("narrative_designer"),
                               data["genre"],
                               year,
                               extra.get("game_status"),
                               )

            self.connection.commit()

            QMessageBox.information(
                self,
                "Готово",
                f"Материал «{data['title']}» добавлен.\n"
                f"ID материала: {material_id}"
            )

            self.load_materials()

        except Exception as error:
            self.connection.rollback()
            QMessageBox.critical(
                self,
                "Ошибка добавления материала",
                f"Не удалось сохранить материал.\n\n{error}"
            )

    def edit_project(self):
        row = self.projects_table.currentRow()

        if row < 0:
            QMessageBox.information(
                self,
                "Проект не выбран",
                "Выбери проект в таблице."
            )
            return

        try:
            project = tuple(
                self.projects_table.item(row, column).text()
                if self.projects_table.item(row, column)
                else ""
                for column in range(5)
            )
            project_id = int(project[0])

        except (ValueError, AttributeError) as error:
            QMessageBox.warning(
                self,
                "Ошибка",
                f"Не удалось прочитать выбранный проект:\n{error}"
            )
            return

        dialog = ProjectDialog(self, project)

        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        name, project_type, genre, status = dialog.get_data()

        try:
            cursor = self.connection.cursor()

            cursor.execute("""
                UPDATE dbo.[Проекты]
                SET
                    [Наименование проекта] = ?,
                    [Тип проекта] = ?,
                    [Жанр] = ?,
                    [Статус проектов] = ?
                WHERE [ID проекта] = ?
            """, (
                name,
                project_type,
                genre,
                status,
                project_id,
            ))

            if cursor.rowcount == 0:
                self.connection.rollback()
                QMessageBox.warning(
                    self,
                    "Проект не найден",
                    "Запись не найдена. Обнови таблицу."
                )
                self.load_projects()
                return

            self.connection.commit()
            self.load_projects()

            QMessageBox.information(
                self,
                "Изменения сохранены",
                f"Проект «{name}» обновлён."
            )

        except Exception as error:
            self.connection.rollback()
            QMessageBox.critical(
                self,
                "Ошибка сохранения",
                f"Не удалось изменить проект:\n{error}"
            )

    def _selected_material_id(self):
        row = self.materials_table.currentRow()
        if row < 0:
            QMessageBox.information(self, "Материал не выбран", "Сначала выбери материал в таблице.")
            return None
        item = self.materials_table.item(row, 0)
        if item is None:
            return None
        try:
            return int(item.text())
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Не удалось определить ID материала.")
            return None

    def _load_material_for_edit(self, material_id):
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT [ID материала], [ID проекта], [Название],
                   [ID типа материала], [Автор], [Год], [Описание], [Жанр]
            FROM dbo.[Материалы]
            WHERE [ID материала] = ?
        """, material_id)
        row = cursor.fetchone()
        if row is None:
            return None

        data = {
            "material_id": row[0],
            "project_id": row[1],
            "title": row[2],
            "type_id": row[3],
            "author": row[4],
            "year": row[5],
            "description": row[6],
            "genre": row[7],
            "extra": {},
        }

        related_queries = {
            1: ("SELECT [Исполнитель], [Автор текста], [Альбом], [Направление музыки] FROM dbo.[Музыка] WHERE [ID материала] = ?", ["artist", "lyric_author", "album", "direction"]),
            2: ("SELECT [Режиссер], [Сценарист], [Продюсер], [Статус просмотра] FROM dbo.[Фильмы] WHERE [ID материала] = ?", ["director", "screenwriter", "producer", "watch_status"]),
            3: ("SELECT [Режиссер], [Сценарист], [Продюсер], [Количество сезонов], [Статус сериала], [Статус просмотра] FROM dbo.[Сериалы] WHERE [ID материала] = ?", ["director", "screenwriter", "producer", "seasons", "series_status", "watch_status"]),
            4: ("SELECT [Статус] FROM dbo.[Книги] WHERE [ID материала] = ?", ["book_status"]),
            5: ("SELECT [Студия разработчик], [Ведущий сценарист], [Нарративный дизайнер], [Статус] FROM dbo.[Игры] WHERE [ID материала] = ?", ["studio", "lead_writer", "narrative_designer", "game_status"]),
        }
        query_info = related_queries.get(data["type_id"])
        if query_info:
            query, keys = query_info
            cursor.execute(query, material_id)
            related = cursor.fetchone()
            if related:
                data["extra"] = dict(zip(keys, related))
        return data

    def edit_material(self):
        material_id = self._selected_material_id()
        if material_id is None:
            return

        try:
            initial = self._load_material_for_edit(material_id)
            if initial is None:
                QMessageBox.warning(self, "Материал не найден", "Обнови список материалов.")
                self.refresh_materials()
                return

            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT [ID проекта], [Наименование проекта]
                FROM dbo.[Проекты]
                ORDER BY [ID проекта]
            """)
            projects = [(r[0], r[1] or "Без названия") for r in cursor.fetchall()]
            cursor.execute("""
                SELECT [ID типа материала], [Наименование материала]
                FROM dbo.[Типы материалов]
                ORDER BY [ID типа материала]
            """)
            material_types = [(r[0], r[1]) for r in cursor.fetchall()]

            dialog = MaterialDialog(projects, material_types, self, initial_data=initial)
            if dialog.exec() != QDialog.DialogCode.Accepted:
                return

            data = dialog.get_data()
            if not data["title"]:
                QMessageBox.warning(self, "Проверка данных", "Название материала не может быть пустым.")
                return

            extra = data["extra"]
            year = data["year"]
            cursor.execute("""
                UPDATE dbo.[Материалы]
                SET [ID проекта] = ?, [Название] = ?, [Автор] = ?,
                    [Год] = ?, [Описание] = ?, [Жанр] = ?
                WHERE [ID материала] = ?
            """, (
                data["project_id"], data["title"], data["author"],
                str(year) if year is not None else None,
                data["description"], data["genre"], material_id
            ))

            type_id = data["type_id"]
            update_sql = {
                1: ("""UPDATE dbo.[Музыка] SET [Наименование музыки]=?, [Исполнитель]=?, [Автор текста]=?, [Альбом]=?, [Год выпуска]=?, [Направление музыки]=?, [Жанр]=? WHERE [ID материала]=?""",
                    (data["title"], extra.get("artist") or data["author"], extra.get("lyric_author"), extra.get("album"), year, extra.get("direction"), data["genre"], material_id)),
                2: ("""UPDATE dbo.[Фильмы] SET [Наименование фильма]=?, [Режиссер]=?, [Сценарист]=?, [Продюсер]=?, [Год выпуска]=?, [Жанр]=?, [Статус просмотра]=? WHERE [ID материала]=?""",
                    (data["title"], extra.get("director"), extra.get("screenwriter"), extra.get("producer"), year, data["genre"], extra.get("watch_status"), material_id)),
                3: ("""UPDATE dbo.[Сериалы] SET [Наименование сериала]=?, [Режиссер]=?, [Сценарист]=?, [Продюсер]=?, [Год выпуска]=?, [Жанр]=?, [Количество сезонов]=?, [Статус сериала]=?, [Статус просмотра]=? WHERE [ID материала]=?""",
                    (data["title"], extra.get("director"), extra.get("screenwriter"), extra.get("producer"), year, data["genre"], extra.get("seasons"), extra.get("series_status"), extra.get("watch_status"), material_id)),
                4: ("""UPDATE dbo.[Книги] SET [Наименование книги]=?, [Автор]=?, [Год написания]=?, [Жанр]=?, [Статус]=? WHERE [ID материала]=?""",
                    (data["title"], data["author"], year, data["genre"], extra.get("book_status"), material_id)),
                5: ("""UPDATE dbo.[Игры] SET [Наименование игры]=?, [Студия разработчик]=?, [Ведущий сценарист]=?, [Нарративный дизайнер]=?, [Жанр]=?, [Год выхода]=?, [Статус]=? WHERE [ID материала]=?""",
                    (data["title"], extra.get("studio"), extra.get("lead_writer"), extra.get("narrative_designer"), data["genre"], year, extra.get("game_status"), material_id)),
            }
            if type_id not in update_sql:
                raise ValueError(f"Неизвестный тип материала: {type_id}")
            sql, params = update_sql[type_id]
            cursor.execute(sql, params)

            self.connection.commit()
            self.load_materials(self.current_material_project_id)
            QMessageBox.information(self, "Изменения сохранены", f"Материал «{data['title']}» обновлён.")

        except Exception as error:
            self.connection.rollback()
            QMessageBox.critical(self, "Ошибка редактирования", f"Не удалось изменить материал:\\n{error}")

    def delete_material(self):
        material_id = self._selected_material_id()
        if material_id is None:
            return

        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT [Название], [ID типа материала]
                FROM dbo.[Материалы]
                WHERE [ID материала] = ?
            """, material_id)
            row = cursor.fetchone()
            if row is None:
                QMessageBox.warning(self, "Материал не найден", "Обнови список материалов.")
                self.refresh_materials()
                return

            title, type_id = row[0] or f"ID {material_id}", row[1]
            answer = QMessageBox.question(
                self,
                "Подтверждение удаления",
                f"Удалить материал «{title}»? Связанная запись тоже будет удалена. Это действие нельзя отменить.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )
            if answer != QMessageBox.StandardButton.Yes:
                return

            related_tables = {1: "Музыка", 2: "Фильмы", 3: "Сериалы", 4: "Книги", 5: "Игры"}
            related_table = related_tables.get(type_id)
            if related_table:
                cursor.execute(
                    f"DELETE FROM dbo.[{related_table}] WHERE [ID материала] = ?",
                    material_id
                )
            cursor.execute("DELETE FROM dbo.[Материалы] WHERE [ID материала] = ?", material_id)
            self.connection.commit()
            self.load_materials(self.current_material_project_id)
            QMessageBox.information(self, "Материал удалён", f"Материал «{title}» удалён.")
        except Exception as error:
            self.connection.rollback()
            QMessageBox.critical(self, "Ошибка удаления", f"Не удалось удалить материал:\\n{error}")

    def delete_project(self):
        row = self.projects_table.currentRow()
        if row < 0:
            QMessageBox.information(self, "Проект не выбран", "Сначала выбери проект в таблице.")
            return

        item = self.projects_table.item(row, 0)
        if item is None:
            return

        try:
            project_id = int(item.text())
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT [Наименование проекта]
                FROM dbo.[Проекты]
                WHERE [ID проекта] = ?
            """, project_id)
            project_row = cursor.fetchone()
            if project_row is None:
                QMessageBox.warning(self, "Проект не найден", "Обнови таблицу и попробуй снова.")
                self.load_projects()
                return

            project_name = project_row[0] or f"ID {project_id}"

            cursor.execute("""
                SELECT COUNT(*)
                FROM dbo.[Материалы]
                WHERE [ID проекта] = ?
            """, project_id)
            material_count = cursor.fetchone()[0]

            if material_count:
                QMessageBox.warning(
                    self,
                    "Нельзя удалить проект",
                    f"Проект «{project_name}» содержит {material_count} связанных материалов. "
                    "Сначала перенеси или удали эти материалы."
                )
                return

            answer = QMessageBox.question(
                self,
                "Подтверждение удаления",
                f"Удалить проект «{project_name}»? Это действие нельзя отменить.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )
            if answer != QMessageBox.StandardButton.Yes:
                return

            cursor.execute("DELETE FROM dbo.[Проекты] WHERE [ID проекта] = ?", project_id)
            if cursor.rowcount == 0:
                self.connection.rollback()
                QMessageBox.warning(self, "Проект не найден", "Проект уже удалён или недоступен.")
                self.load_projects()
                return

            self.connection.commit()
            self.load_projects()
            QMessageBox.information(self, "Проект удалён", f"Проект «{project_name}» удалён.")

        except Exception as error:
            self.connection.rollback()
            QMessageBox.critical(self, "Ошибка удаления", f"Не удалось удалить проект:\\n{error}")

    def load_material_types(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT
                    [ID типа материала],
                    [Наименование материала]
                FROM dbo.[Типы материалов]
                ORDER BY [ID типа материала]
            """)

            types = cursor.fetchall()

            self.material_type_filter.blockSignals(True)
            self.material_type_filter.clear()
            self.material_type_filter.addItem("Все типы", None)

            for type_id, type_name in types:
                self.material_type_filter.addItem(
                    str(type_name), type_id
                )

            self.material_type_filter.blockSignals(False)

        except Exception as error:
            self.material_type_filter.blockSignals(False)
            QMessageBox.warning(
                self,
                "Ошибка загрузки типов",
                f"Не удалось загрузить типы материалов:\n{error}",
            )

    def load_materials(self, project_id=None):
        try:
            cursor = self.connection.cursor()

            query = """
                SELECT
                    m.[ID материала],
                    m.[Название],
                    m.[Автор],
                    m.[Год],
                    m.[Жанр],
                    t.[Наименование материала] AS [Тип материала],
                    p.[Наименование проекта] AS [Проект]
                FROM dbo.[Материалы] AS m
                LEFT JOIN dbo.[Типы материалов] AS t
                    ON m.[ID типа материала] =
                       t.[ID типа материала]
                LEFT JOIN dbo.[Проекты] AS p
                    ON m.[ID проекта] = p.[ID проекта]
            """

            params = []

            if project_id is not None:
                query += " WHERE m.[ID проекта] = ?"
                params.append(project_id)

            query += " ORDER BY m.[Порядковый номер]"

            cursor.execute(query, params)
            columns = [
                column[0] for column in cursor.description
            ]
            rows = cursor.fetchall()

            self.current_material_project_id = project_id

            self._fill_table(
                self.materials_table, columns, rows
            )

            self.material_search.clear()
            self.filter_materials()

            if project_id is None:
                self.materials_heading.setText("Материалы")
                self.materials_status.setText(
                    f"Загружено материалов: {len(rows)}"
                )
            else:
                self.materials_heading.setText(
                    f"Материалы проекта {project_id}"
                )
                self.materials_status.setText(
                    f"Материалов проекта: {len(rows)}"
                )

        except Exception as error:
            QMessageBox.warning(
                self,
                "Ошибка загрузки материалов",
                f"Не удалось загрузить материалы:\n{error}",
            )

    def filter_materials(self, *_):
        query = self.material_search.text().casefold().strip()
        selected_type = self.material_type_filter.currentData()

        for row in range(self.materials_table.rowCount()):
            matches_text = any(
                query in (
                    self.materials_table.item(row, column).text()
                    if self.materials_table.item(row, column)
                    else ""
                ).casefold()
                for column in range(
                    self.materials_table.columnCount()
                )
            )

            type_item = self.materials_table.item(row, 5)
            row_type = type_item.text() if type_item else ""

            selected_type_name = self.material_type_filter.currentText()
            matches_type = (
                selected_type is None
                or row_type == selected_type_name
            )

            self.materials_table.setRowHidden(
                row, not (matches_text and matches_type)
            )

    def show_selected_project_materials(self):
        row = self.projects_table.currentRow()

        if row < 0:
            QMessageBox.information(
                self,
                "Проект не выбран",
                "Сначала выбери проект в таблице.",
            )
            return

        item = self.projects_table.item(row, 0)

        if item is None:
            return

        try:
            project_id = int(item.text())
        except ValueError:
            QMessageBox.warning(
                self,
                "Ошибка",
                "Не удалось определить ID проекта.",
            )
            return

        self.load_materials(project_id)
        self.pages.setCurrentIndex(1)

    def show_all_materials(self):
        self.load_materials()
        self.pages.setCurrentIndex(1)

    def refresh_materials(self):
        self.load_material_types()
        self.load_materials(
            self.current_material_project_id
        )

