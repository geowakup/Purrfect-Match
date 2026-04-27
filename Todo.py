from PySide6.QtWidgets import (
    QWidget, QVBoxLayout,
    QPushButton, QListWidget, QInputDialog
)
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QListWidgetItem

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
        self.task_list.itemChanged.connect(self.handle_item_change)
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
            item = QListWidgetItem(text)

            # add checkbox
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)

            self.task_list.addItem(item)

    def delete_task(self):
        for i in reversed(range(self.task_list.count())):
            item = self.task_list.item(i)
            if item.checkState() == Qt.Checked:
                self.task_list.takeItem(i)

    def handle_item_change(self, item):
        if item.checkState() == Qt.Checked:
            font = item.font()
            font.setStrikeOut(True)
            item.setFont(font)
            item.setForeground(Qt.gray)
            
        else:
            font = item.font()
            font.setStrikeOut(False)
            item.setFont(font)
            item.setForeground(Qt.black)
    
