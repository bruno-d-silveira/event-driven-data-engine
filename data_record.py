class DataRecord:
    def __init__(self, payload):
        self.payload = payload
        self.features = {}
        self.meta = {}

    def __repr__(self):
        return f"<DataRecord payload_keys={list(self.payload.keys())}>"
