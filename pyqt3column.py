import sys
import json
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QFrame, QListWidget, QListWidgetItem, QTreeWidget, QTreeWidgetItem, QPushButton, QFileDialog, QTextEdit, QVBoxLayout
from PyQt5.QtCore import Qt


class ThreeColumnApp(QWidget):
    '''
    Class creates a three column application with a 
    file column, category column, and data column.
    '''
    layout = None

    def __init__(self):
        super().__init__()
        self.layout = QGridLayout()
        self.file_widget = QListWidget()
        self.category_widget = QListWidget()
        self.data_widget = QListWidget()
        self.file_data = {}
        self.data = {}
        self.selected_file = 0
        self.selected_category = ""
        self.input_file_name = ""

        self.init_ui()

    def init_ui(self):
        """Function initializes user interface."""
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
        button.clicked.connect(self.on_load_button_click)

        # Add the button to the second row, spanning all columns
        self.layout.addWidget(button, 1, 0, 1, 5)

        # Add Save button
        new_button = QPushButton('Save')
        # Connect the button to a function
        new_button.clicked.connect(self.on_save_button_click)
        # Add the button to the layout under the data widget
        self.layout.addWidget(new_button, 1, 4, 1, 1)


        self.setLayout(self.layout)

    def on_save_button_click(self):
        '''Function to handle load button click.'''
        parsed_data = self.parse_data()
        current_item = self.category_widget.currentItem()
        if current_item is not None:
            current_item.setCheckState(Qt.Checked)
        # Label the data as human checked
        for datapoint in parsed_data:
            datapoint["Human Checked"] = True
        # Save New Data to database
        self.update_data(parsed_data)

    def on_load_button_click(self):
        '''Function opens a file dialog to select a JSON file.'''
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open JSON File", "", "JSON Files (*.json);;All Files (*)", options=options
            )
        if file_name:
            self.input_file_name = file_name
            with open(self.input_file_name, 'r', encoding='utf-8') as file:
                self.data = json.load(file)
            # Refresh the file widget with the new file data
            self.file_widget = self.get_file_widget(self.input_file_name, 'paperFileName')
            self.layout.addWidget(self.file_widget, 0, 0)
            self.file_widget.itemClicked.connect(self.on_file_click)

    def get_file_data(self, index):
        '''Function gets the data from the selected file and stores it in a dictionary.'''
        # Initialize the files category data dictionary
        self.file_data = {}
        self.selected_file = index

        time_stamp_dict = {}

        # for each query in the file data
        for query_data in self.data[index]["extractData"]:
            # Get the main category
            main_data_group = query_data["dataType"]
            # Get the time stamp
            time_stamp = query_data["timeStamp"]
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
            if data is not None:
                # if the main category is already in the file dictionary
                if main_data_group not in self.file_data:
                    # if not already in the category dictionary -> initialize it with sub category
                    self.file_data[main_data_group] = {}
                    time_stamp_dict[main_data_group] = {}

                # if the main category does not have the subcategory in its dictionary, add it
                if sub_data_group not in self.file_data[main_data_group].keys():
                    self.file_data[main_data_group][sub_data_group] = []
                    time_stamp_dict[main_data_group][sub_data_group] = []

                # Add data found to the subcategory
                for datapoint in data:
                    self.file_data[main_data_group][sub_data_group].append(str(datapoint))
                    time_stamp_dict[main_data_group][sub_data_group].append(time_stamp)



    def on_file_click(self, item):
        '''Function gets the data from the selected file and stores it in a dictionary.'''
        item_text = item.text()
        print(f'Item Clicked: {item_text}')

        self.get_file_data(int(item_text[0]))
        category_widget = self.get_category_widget(self.file_data)
        self.update_category_column(category_widget)

    def on_category_click(self, item):
        '''Function gets the data from the selected category and stores it in a dictionary.'''
        data_widget = self.get_data_widget(self.file_data[item.text()])
        self.selected_category = item.text()
        self.update_data_column(data_widget)

    def get_file_widget(self, filename, key):
        '''Function gets the file names from the input file and stores it in a QListWidget.'''
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)

        file_names = QListWidget()
        for i, data_dict in enumerate(data):
            file_names.addItem(str(i) + ": " + data_dict[key])

        return file_names

    def get_category_widget(self, file_data):
        '''Function gets the categories from the input file and stores it in a QListWidget.'''

        categories = QListWidget()
        for main_category in file_data.keys():
            item = QListWidgetItem(main_category)
            item.setCheckState(Qt.Unchecked)
            categories.addItem(item)

        return categories

    def get_data_widget(self, category_data):
        '''Function gets the data from the input file and stores it in a QListWidget.'''
        data_widget = QTextEdit()
        data_widget.setAcceptRichText(True)

        data_widget.setReadOnly(False)

        for subcategory, data_list in category_data.items():
            data_widget.append(f"{subcategory}")

            if data_list:
                for datapoint in data_list:
                    for key, value in eval(datapoint).items():
                        data_widget.append(f"    {key}: {value}")
                    data_widget.append("")
            data_widget.append("")

        return data_widget

    def update_category_column(self, column_widget):
        '''Function updates the category column with the new category widget.'''
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
        '''Function updates the data column with the new data widget.'''
        # Remove old data widget
        self.layout.removeWidget(self.data_widget)
        self.data_widget.deleteLater()

        # Add new data widget
        self.data_widget = data_widget
        self.layout.addWidget(self.data_widget, 0, 4)

    def parse_data(self):
        '''Function parses the data from the data widget and stores it in a dictionary.'''
        data_text = self.data_widget.toPlainText()
        lines = data_text.split("\n")
        parsed_data = []
        current_data_entry = {}
        current_entry = {"dataType": self.selected_category}
        for line in lines:
            if line == "":
                # If new line found and current_data_entry is not empty,
                # append it to the current_entry
                if current_data_entry != {}:
                    current_entry["data"].append(current_data_entry)
                    current_data_entry = {}
            elif line[0] != " ":
                # If new sub category found, append old one and reset current_entry
                if current_entry != {"dataType": self.selected_category}:
                    # Append current entry to parsed data
                    parsed_data.append(current_entry)
                    # Reset current_entry
                    current_entry = {"dataType": self.selected_category}
                current_entry["dataType2"] = line
                current_entry["data"] = []
            elif line[0] == " ":
                # if new data is found, add it to the current_entry_data
                parsed_line = line.split(":")
                key = parsed_line[0]
                value = ":".join(parsed_line[1:])
                key, value = key.strip(), value.strip()
                current_data_entry[key] = value
        # Append last entry
        if current_entry != {"dataType": self.selected_category}:
            if current_data_entry != {}:
                current_entry["data"].append(current_data_entry)
            parsed_data.append(current_entry)
        print(json.dumps(parsed_data, indent=4))
        return parsed_data

    # Removes the data to be replaced by updated data.
    def remove_old_data(self):
        '''Function removes the old data from the file data.'''
        for datapoint in self.data[self.selected_file]["extractData"]:
            if datapoint["dataType"] == self.selected_category:
                self.data[self.selected_file]["extractData"].remove(datapoint)
    
    def update_data(self, data):
        '''Function updates the data in the file data.'''
        self.data[self.selected_file]["extractData"] # TODO: Finish this function



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ThreeColumnApp()
    window.show()
    sys.exit(app.exec_())
