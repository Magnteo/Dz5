def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            return "Not enough arguments."
        except ValueError:
            return "Invalid value."
        except KeyError:
            return "No such contact."
        except AttributeError:
             return "Attribute not found. Maybe contact is missing or incomplete"
    return wrapper
