import os
import csv


class Csv:
    def __init__(self, file_name, fieldnames, folder_path='./'):
        self.file_name = file_name if file_name.endswith('.csv') else file_name+'.csv'
        self.fieldnames = fieldnames
        self.folder_path = folder_path
        self.path = self.folder_path + self.file_name
        self.file = None
        self.writer = None

    def initialize(self, close_file = False):
        try:
            self.initFile(close_file=close_file)
        except FileNotFoundError:
            os.mkdir(self.folder_path)
            self.initFile(close_file=close_file)

    def initFile(self, close_file = False):
        self.open(mode='w')
        self.defWriter()
        self.writerow(self.fieldnames)
        if close_file: self.close()

    def open(self, mode='r'):
        self.file = open(self.path, mode)
        self.defWriter()
        return self.file

    def close(self):
        return self.file.close()

    def defWriter(self):
        self.writer = csv.writer(self.file)
        return self.writer

    def writerow(self, row):
        return self.writer.writerow(row)
