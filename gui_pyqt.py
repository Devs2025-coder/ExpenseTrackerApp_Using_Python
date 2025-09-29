import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox, QTextEdit, QHeaderView
)
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt
from storage import Storage
from datetime import datetime
from collections import defaultdict
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class ExpenseTrackerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Expense Tracker")
        self.setMinimumSize(900, 700)
        Storage.initialize_db()
        self.init_ui()
        self.load_expenses()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)

        # Input fields
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Amount")
        self.category_input = QLineEdit()
        self.category_input.setPlaceholderText("Category")
        self.description_input = QLineEdit()
        self.description_input.setPlaceholderText("Description")
        self.date_input = QLineEdit()
        self.date_input.setPlaceholderText("Date (YYYY-MM-DD)")

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.amount_input)
        input_layout.addWidget(self.category_input)
        input_layout.addWidget(self.description_input)
        input_layout.addWidget(self.date_input)
        layout.addLayout(input_layout)

        # Buttons
        button_layout = QHBoxLayout()
        add_btn = QPushButton("Add Expense")
        add_btn.clicked.connect(self.add_expense)
        add_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        edit_btn = QPushButton("Edit Selected")
        edit_btn.clicked.connect(self.edit_expense)
        edit_btn.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold;")
        delete_btn = QPushButton("Delete Selected")
        delete_btn.clicked.connect(self.delete_expense)
        delete_btn.setStyleSheet("background-color: #f44336; color: white; font-weight: bold;")
        button_layout.addWidget(add_btn)
        button_layout.addWidget(edit_btn)
        button_layout.addWidget(delete_btn)
        layout.addLayout(button_layout)

        # Search
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by category or date")
        search_btn = QPushButton("Search")
        search_btn.clicked.connect(self.search_expenses)
        search_btn.setStyleSheet("background-color: #FF9800; color: white; font-weight: bold;")
        search_layout = QHBoxLayout()
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_btn)
        layout.addLayout(search_layout)

        # Expense table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Amount", "Category", "Description", "Date"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setFont(QFont("Arial", 10, QFont.Bold))
        self.table.setAlternatingRowColors(True)
        layout.addWidget(self.table)

        # Summary report
        summary_label = QLabel("Summary Report:")
        summary_label.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(summary_label)
        self.summary_text = QTextEdit()
        self.summary_text.setReadOnly(True)
        self.summary_text.setStyleSheet("background-color: #f0f0f0;")
        layout.addWidget(self.summary_text)

        # Pie Chart
        chart_label = QLabel("Category-wise Expenses:")
        chart_label.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(chart_label)
        self.figure = Figure(figsize=(4, 4))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.setLayout(layout)

    def load_expenses(self, data=None):
        if data is None:
            data = Storage.load_expenses()
        self.table.setRowCount(0)
        for row_data in data:
            row_idx = self.table.rowCount()
            self.table.insertRow(row_idx)
            for col_idx, item in enumerate(row_data):
                cell = QTableWidgetItem(str(item))
                cell.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.table.setItem(row_idx, col_idx, cell)
        self.update_summary(data)
        self.update_pie_chart(data)

    def add_expense(self):
        try:
            amount = float(self.amount_input.text())
            category = self.category_input.text()
            description = self.description_input.text()
            date_str = self.date_input.text()
            datetime.strptime(date_str, "%Y-%m-%d")
            Storage.save_expense(amount, category, description, date_str)
            QMessageBox.information(self, "Success", "Expense added successfully!")
            self.clear_inputs()
            self.load_expenses()
        except ValueError:
            QMessageBox.warning(self, "Error", "Invalid input. Check amount and date format.")

    def edit_expense(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Error", "Select a row to edit.")
            return
        expense_id = int(self.table.item(selected, 0).text())
        amount = self.amount_input.text()
        category = self.category_input.text()
        description = self.description_input.text()
        date_str = self.date_input.text()
        kwargs = {}
        if amount: kwargs["amount"] = float(amount)
        if category: kwargs["category"] = category
        if description: kwargs["description"] = description
        if date_str: kwargs["date_str"] = date_str
        Storage.update_expense(expense_id, **kwargs)
        QMessageBox.information(self, "Success", "Expense updated successfully!")
        self.clear_inputs()
        self.load_expenses()

    def delete_expense(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Error", "Select a row to delete.")
            return
        expense_id = int(self.table.item(selected, 0).text())
        Storage.delete_expense(expense_id)
        QMessageBox.information(self, "Deleted", "Expense deleted successfully!")
        self.load_expenses()

    def search_expenses(self):
        query = self.search_input.text()
        if not query:
            self.load_expenses()
            return
        try:
            datetime.strptime(query, "%Y-%m-%d")
            data = Storage.search_by_date(query)
        except ValueError:
            data = Storage.search_by_category(query)
        self.load_expenses(data)

    def clear_inputs(self):
        self.amount_input.clear()
        self.category_input.clear()
        self.description_input.clear()
        self.date_input.clear()

    def update_summary(self, data=None):
        if data is None:
            data = Storage.load_expenses()
        total = sum([row[1] for row in data])
        category_summary = defaultdict(float)
        for row in data:
            category_summary[row[2]] += row[1]
        summary_text = f"Total Expenses: {total:.2f}\n\nBy Category:\n"
        for cat, amt in category_summary.items():
            summary_text += f"{cat}: {amt:.2f}\n"
        self.summary_text.setText(summary_text)

    def update_pie_chart(self, data=None):
        if data is None:
            data = Storage.load_expenses()
        category_summary = defaultdict(float)
        for row in data:
            category_summary[row[2]] += row[1]
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        if category_summary:
            ax.pie(category_summary.values(), labels=category_summary.keys(),
                   autopct='%1.1f%%', startangle=140, shadow=True)
        ax.set_title("Category-wise Expenses")
        self.canvas.draw()
