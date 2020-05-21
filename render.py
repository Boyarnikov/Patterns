import time


class Render:
    def __init__(self):
        self.data_base = list()
        self.renders = list()

    def append_data(self, log_data):
        self.data_base.extend(log_data.copy())

    def render_data(self):
        for data in self.data_base:
            print(data.__dict__)
            time.sleep(data.time)
        self.data_base = list()

