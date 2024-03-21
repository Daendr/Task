import csv


class CsvManager:
    @staticmethod
    def write_csv(file_path, headers, rows):
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            for row in rows:
                writer.writerow(row)

    @staticmethod
    def read_csv_data(csv_path):
        with open(csv_path, mode='r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            next(csv_reader, None)
            return list(csv_reader)
