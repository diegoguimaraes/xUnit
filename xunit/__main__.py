import sys
from xunit import MainProgram

if __name__ == '__main__':
    main = MainProgram(sys.argv)
    result = main.run()
    print(result)
