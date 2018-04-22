from gui.Window import Window


class EventManager:
    def __init__(self):
        self.listeners = dict()

    def register(self, listener, event: int, window: Window) -> None:
        if self.listeners.get(event) is None:
            self.listeners[event] = set()
        self.listeners[event].add((listener, window))

    def delete(self, pair, event: int) -> None:
        if self.listeners.get(event) is not None:
            if pair in self.listeners[event]:
                self.listeners[event].remove(pair)

    def delete_all(self, window: Window) -> None:
        for i in self.listeners:
            for j in self.listeners[i]:
                if j[1] == window:
                    self.delete(j, i)
                    break

    def fire(self, event: int, param: dict) -> None:
        if self.listeners.get(event) is not None:
            for i in self.listeners[event]:
                i[0](**param)

    class Events:
        doc_added = 0
        doc_deletion_state_changed = 1
        doc_changed = 2
        copy_added = 3
        copy_state_changed = 4
        copy_deletion_state_changed = 5
        queue_changed = 6
