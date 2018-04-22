_listeners = {}


def register_listener(name, func):
    listeners = _listeners.get(name, None)
    if listeners:
        _listeners[name].append(func)
    else:
        _listeners[name] = [func]


def send_event(name, *args):
    listeners = _listeners.get(name, None)
    if listeners:
        if args:
            for listener in listeners:
                result = listener(*args)
        else:
            for listener in listeners:
                result = listener()
