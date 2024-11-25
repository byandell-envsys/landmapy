# example.py
# https://packaging.python.org/en/latest/tutorials/packaging-projects/

def add_one(number):
    return number + 1

def div_two(number):
    print(number / 2)

def mod_name():
    val = __name__
    print(val)

def mod_path():
    val = __path__
    print(val)