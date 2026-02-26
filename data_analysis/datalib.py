import importlib.metadata
import subprocess
import sys



def check_libs(required_libs):
    installed_packages = {pkg.metadata['Name'] for pkg in importlib.metadata.distributions()}
    missing = required_libs - installed_packages

    if missing:
        print(f'Missing {missing}')
        print('Installing...')
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', *missing])
        print('Installation complete.')


check_libs({'matplotlib'})



import matplotlib as mp
import matplotlib.pyplot as plt

import csv
import os

from datetime import datetime
from pathlib import Path



class DataHandler:
    def __init__(self, csv_path: Path):
        self._csv_path = csv_path
        self._plots_path = None
        self._meta_path = None
        self._data_dict = {}
        self._header = []

        self.format_data()
        self.setup_dirs()


    def data(self):
        return self._data_dict


    def header(self):
        return self._header


    def column_type(self, column: str):
        return type(self._data_dict[column][0])


    def clean_item(self, item: str):
        for e in [int, float]:
            try:
                item = e(item)
            except ValueError:
                continue
            else:
                break

        return item
        

    def format_data(self):
        with open(self._csv_path, 'r') as f:
            reader = csv.reader(f)

            for row in reader:
                self._header = row
                break

            for col in self._header:
                self._data_dict[col] = []

            for row in reader:
                if row == self._header or len(row) == 0:
                    continue

                for i in range(len(row)):
                    col_val = row[i]
                    col_val = self.clean_item(col_val)
                    
                    self._data_dict[self._header[i]].append(col_val)


    def setup_dirs(self):
        parent = self._csv_path.parent
        self._plots_path = parent / Path('plots')
        self._meta_path = parent / Path('metadata')

        if not self._plots_path.is_dir():
            os.mkdir(self._plots_path)

        if not self._meta_path.is_dir():
            os.mkdir(self._meta_path)

        if not self._meta_path.is_file():
            with open(self._meta_path / 'log.txt', 'w') as f:
                f.write('')
            


    def log(self, text: str):
        with open(self._meta_path, 'a') as f:
            f.write(text)


    def timestamp(self):
        return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


    def display(self, x_label: str, y_label: str, filename: str, window: bool):
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.savefig(self._plots_path / Path(f'{filename}_{self.timestamp()}.png'))
        if window:
            plt.show(block = False)
        else:
            plt.close()


    def scatter(self, x_column: str, y_column: str, limit: int = -1, window: bool = True):
        x = self._data_dict[x_column][:limit]
        y = self._data_dict[y_column][:limit]

        plt.scatter(x, y)
        self.display(x_column, y_column, 'scatter', window)


    def format_categorical(self, column_vals: list) -> tuple[list, list[int]]:
        categories = list(dict.fromkeys(column_vals))
        categories.sort()
        counts = []

        for e in categories:
            counts.append(column_vals.count(e))

        return categories, counts


    def bar_count_categorical(self, column: str, limit: int = -1, window: bool = True):
        raw = self._data_dict[column][:limit]
        categories, counts = self.format_categorical(raw)

        print(categories, counts)

        plt.barh([str(x) for x in categories], counts)
        self.display(column, 'count', 'bar_count', window)


    def bar_average_categorical(self, categorical_x: str, numerical_y: str, limit: int = -1, window: bool = True):
        pass
    


    def pie_count_categorical(self, column: str, limit: int = -1, window: bool = True):
        raw = self._data_dict[column][:limit]
        categories, counts = self.format_categorical(raw)

        print(categories, counts)

        plt.pie(counts, labels = categories)
        self.display(column, '', 'pie_count', window)


    def scatter_all_nums(self):
        plotted = []
        
        for col in self._data_dict:
            if self.column_type(col) != float:
                continue
            
            for nested_col in self._data_dict:
                if col == nested_col or self.column_type(nested_col) not in [float, int] or (nested_col, col) in plotted:
                    continue

                self.scatter(col, nested_col)
                plt.close()
                plotted.append((col, nested_col))


def help():
    text = ['Here is a reference of the functions in this module.',
            'start: Initializes the data handler.\nFormat: start(csv_file_path)',
            'The remaining functions require the existence of a data handler.',
            'scatter: Creates a scatterplot of the relationship between two number variables.\nFormat: handler.scatter(x_column, y_column)',
            'bar_count_categorical: Creates a bar plot that counts each value of a categorical variable.\nFormat: handler.bar_count_categorical(column)']
    
    for line in text:
        print(line)
        print()


def format_list(val: list) -> str:
    formatted = ''

    for e in val:
        formatted += f'{e}\n'

    return formatted


def start(csv_path: str):
    global handler
    handler = DataHandler(Path(csv_path))
    print()
    print('HEADERS:')
    print(format_list(handler.header()))
    print()

    

def welcome():
    print(f'Matplot v{mp.__version__}')
    print('Welcome to datalib.')

    if __name__ == '__main__':
        func = 'help()'
    else:
        func = 'datalib.help()'

    print(f'Enter {func} into the console for a list of functions in this module.')


welcome()

