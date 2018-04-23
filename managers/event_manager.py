"""Simple event manager"""
# List of all listeners
_listeners = {}


def register_listener(name, func):
    """
    Register listener in event manager
    :param name: name of the listener
    :param func: function corresponding to listener
    :return: None
    """
    listeners = _listeners.get(name, None)
    if listeners:
        _listeners[name].append(func)
    else:
        _listeners[name] = [func]


def send_event(name, *args):
    """
    Send event to registered listeners
    :param name: name of the listener
    :param args: arguments for the listener, if any
    :return: None
    """
    listeners = _listeners.get(name, None)
    if listeners:
        if args:
            for listener in listeners:
                listener(*args)
        else:
            for listener in listeners:
                listener()
