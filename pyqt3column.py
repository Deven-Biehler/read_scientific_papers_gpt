import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QFrame, QListWidget, QListWidgetItem, QTreeWidget, QTreeWidgetItem, QPushButton, QFileDialog, QTextEdit, QVBoxLayout
from PyQt5.QtCore import Qt

import json

class ThreeColumnApp(QWidget):
    layout = None

    def __init__(self):
        super().__init__()
        self.layout = QGridLayout()
        self.file_data = {}
        self.selected_file = 0
        self.selected_category = ""

        self.initUI()

    def initUI(self):
        # Initialize Window
        self.setWindowTitle('Three Column Application')
        self.setGeometry(100, 100, 1200, 400)

        # Initialize widgets for each column
        self.file_widget = QListWidget()
        self.category_widget = QListWidget()
        self.data_widget = QListWidget()
        self.file_widget.itemClicked.connect(self.on_file_click)

        # Add widgets to columns
        self.layout.addWidget(self.file_widget, 0, 0)
        self.layout.addWidget(self.category_widget, 0, 2)
        self.layout.addWidget(self.data_widget, 0, 4)



        # Line creation:
        # Create vertical lines to separate the columns
        line1 = QFrame()
        line1.setFrameShape(QFrame.VLine)
        line2 = QFrame()
        line2.setFrameShape(QFrame.VLine)

        # Add line widgets to the layout
        self.layout.addWidget(line1, 0, 1)
        self.layout.addWidget(line2, 0, 3)

        # Add a button
        button = QPushButton('Load File')
        button.clicked.connect(self.on_button_click)
        self.layout.addWidget(button, 1, 0, 1, 5)  # Add the button to the second row, spanning all columns


        self.setLayout(self.layout)

    def on_button_click(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, "Open JSON File", "", "JSON Files (*.json);;All Files (*)", options=options)
        if file_name:
            self.input_file_name = file_name
            with open(self.input_file_name, 'r') as file:
                self.data = json.load(file)
            # Refresh the file widget with the new file data
            self.file_widget = self.get_file_widget(self.input_file_name, 'paperFileName')
            self.layout.addWidget(self.file_widget, 0, 0)
            self.file_widget.itemClicked.connect(self.on_file_click)

    def get_file_data(self, index):
        # Initialize the files category data dictionary
        self.file_data = {}
        self.selected_file = index

        # for each query in the file data
        for query_data in self.data[index]["extractData"]:
            # Get the main category
            main_data_group = query_data["dataType"]
            # If a sub category exists
            if "dataType2" in query_data.keys():
                # Get sub category
                sub_data_group = query_data["dataType2"]
            else:
                # If no sub category exists, tag as null
                sub_data_group = "null"
            # Get the actual data from the category
            data = query_data["data"]

            # If chatGPT did not fail to get data
            if data != None:
                # if the main category is already in the file dictionary
                if main_data_group not in self.file_data.keys():
                    # if it is not already in the category dictionary, then initialize it with its sub category
                    self.file_data[main_data_group] = {}

                # if the main category does not have the subcategory in its dictionary, add it
                if sub_data_group not in self.file_data[main_data_group].keys():
                    self.file_data[main_data_group][sub_data_group] = []
                
                # Add data found to the subcategory
                for datapoint in data:
                    self.file_data[main_data_group][sub_data_group].append(str(datapoint))

    def on_file_click(self, item):
        item_text = item.text()
        print(f'Item Clicked: {item_text}')

        self.get_file_data(int(item_text[0]))
        category_widget = self.get_category_widget(self.file_data)
        self.update_category_column(category_widget)

    def on_category_click(self, item):
        data_widget = self.get_data_widget(self.file_data[item.text()])
        self.update_data_column(data_widget)

    def get_file_widget(self, filename, key):
        with open(filename, 'r') as file:
            data = json.load(file)

        file_names = QListWidget()
        for i, dict in enumerate(data):
            file_names.addItem(str(i) + ": " + dict[key])

        return file_names

    def get_category_widget(self, file_data):

        categories = QListWidget()
        for main_category in file_data.keys():
            categories.addItem(main_category)

        return categories

    def get_data_widget(self, category_data):
        data_widget = QTextEdit()
        data_widget.setAcceptRichText(True)
        data_widget.setPlaceholderText("Edit your data here...")

        data_widget.setReadOnly(False)

        for subcategory, data_list in category_data.items():
            data_widget.append(f"{subcategory}")

            if data_list:
                for datapoint in data_list:
                    for key, value in eval(datapoint).items():
                        data_widget.append(f" {key}: {value}")
                    data_widget.append("")
            data_widget.append("")

        data_widget.textChanged.connect(self.on_data_widget_changed)

        return data_widget

    def on_data_widget_changed(self):
        new_text = self.data_widget.toPlainText()
        print(f"Data widget content changed to: {new_text}")
    
    def update_category_column(self, column_widget):
        # update data column
        self.update_data_column(QListWidget())
        
        # Remove old category widget
        self.layout.removeWidget(self.category_widget)
        self.category_widget.deleteLater()
        # Add new category widget
        self.category_widget = column_widget
        self.layout.addWidget(self.category_widget, 0, 2)
        self.category_widget.itemClicked.connect(self.on_category_click)
    
    def update_data_column(self, data_widget):
        # Remove old data widget
        self.layout.removeWidget(self.data_widget)
        self.data_widget.deleteLater()

        # Add new data widget
        self.data_widget = data_widget
        self.layout.addWidget(self.data_widget, 0, 4)
    
    def parse_data(self, data_widget):
        lines = data_widget.split("\n")
        parsed_data = []
        current_entry = {}
        current_key = ""
        for line in lines:
            if line == "":
                # If new line found, append the current entry and initialize new entry.
                if current_entry != {"dataType": self.selected_category}:
                    parsed_data.append(current_entry)
                    current_entry = {"dataType": self.selected_category}
            elif line[0] != " ":
                # If new sub category found, add to dictionary
                current_entry["dataType2"] = [line]
            elif line[0] == " ":
                key, value = line.split(":")
                current_entry["data"][key] = value
        print()

    # Removes the data to be replaced by updated data.
    def remove_old_data(self):
        for datapoint in self.data[self.selected_file]["extractData"]:
            if datapoint["dataType"] == self.selected_category:
                self.data[self.selected_file]["extractData"].remove(datapoint)
                


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ThreeColumnApp()
    window.show()
    sys.exit(app.exec_())