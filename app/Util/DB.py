import json


class DB:
    def __init__(self):
        self.Database = {}
        self.load()

    def load(self):
        try:
            with open('DB.json', 'r') as f:
                self.Database = json.load(f)
        except Exception as e:
            print(e)
        else:
            f.close()

    def save(self):
        try:
            with open('DB.json', 'w') as f:
                f.write(json.dumps(self.Database, indent=4))
        except Exception as e:
            print(e)
        else:
            f.close()

    def saveToDB(self, id, longurl):
        self.Database[id] = longurl
        self.save()

    def readFromDB(self, id):
        return self.Database[id]
