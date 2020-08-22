
class Counter:
    def __init__(self, url_name, latest_id):
        # self.random()
        self.name = url_name
        self.id = latest_id

class Counter_Manager:
  def __init__(self):
    self.first_ID = 1
    self.url_list = []

  def count_url(self):
    
    latest_id = self.first_ID
    new_url = Counter(url_name, latest_id)
    self.url_list.append(new_url)
    print(f"Your url ID is: {latest_id}")
    self.first_ID += 1
    return(latest_id)

