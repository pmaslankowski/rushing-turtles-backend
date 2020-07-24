
class Person(object):
    id: int
    name: str

    def __init__(self, id, name, websocket=None):
        self.id = id
        self.name = name
        self.websocket = websocket

    def is_connected(self):
        return self.websocket is not None

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return f'{self.name}({self.id})'
