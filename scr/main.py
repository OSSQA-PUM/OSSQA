import os
import numpy as np

def do_something():
    print("Goodbye Wolrd!")
    print("Hello Wolrd!")
    print(os.path.dirname(os.path.abspath(__file__)))

    a = np.arange(15).reshape(3, 5)

    print(a)

def main():
    do_something()

if __name__ == "__main__":
    main()