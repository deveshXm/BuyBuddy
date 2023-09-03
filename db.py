import json

class FileDatabase:
    def __init__(self, filename):
        self.filename = filename

    def create(self, data):
        with open(self.filename, 'w') as file:
            json.dump(data, file)

    def read(self):
        try:
            with open(self.filename, 'r') as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            return []

    def add(self, new_data):
        existing_data = self.read()
        for item in existing_data:
            if item['ID'] == new_data['ID']:
                item['Data'] = new_data['Data']
                self.create(existing_data)
                return "Updated"
        existing_data.append(new_data)
        self.create(existing_data)
        return "Appended"

    def delete(self, id_to_delete):
        existing_data = self.read()
        updated_data = [item for item in existing_data if item['ID'] != id_to_delete]
        self.create(updated_data)
        
    def find(self, id_to_find):
        existing_data = self.read()
        for item in existing_data:
            if item['ID'] == id_to_find:
                return item
        return None