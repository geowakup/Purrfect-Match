from PySide6.QtWidgets import (
    QWidget, QVBoxLayout,
    QPushButton, QListWidget, QInputDialog
)
# =========================
# Task (TO-DO-LIST)
# =========================
class TodoApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("To-Do List")
        self.resize(300, 400)

        layout = QVBoxLayout()

        self.task_list = QListWidget()
        layout.addWidget(self.task_list)

        self.add_button = QPushButton("Add Task")
        self.add_button.clicked.connect(self.add_task)
        layout.addWidget(self.add_button)

        self.delete_button = QPushButton("Delete Task")
        self.delete_button.clicked.connect(self.delete_task)
        layout.addWidget(self.delete_button)

        self.setLayout(layout)

    def add_task(self):
        text, ok = QInputDialog.getText(self, "Add Task", "Enter task:")
        if ok and text.strip():
            self.task_list.addItem(text)

    def delete_task(self):
        selected = self.task_list.currentRow()
        if selected >= 0:
            self.task_list.takeItem(selected)

