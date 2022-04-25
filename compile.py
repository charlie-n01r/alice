from alice_yacc import parser
from structs import *

while True:
    try:
        file_name = input('>Insert file name: ')
        test_file = open(file_name)
        source_code = test_file.read()
        test_file.close()
    except (KeyboardInterrupt, EOFError):
        quit('')
    except FileNotFoundError:
        print('Error! Wrong file name!')
        continue
    parser.parse(source_code)
    print(f"Successfully parsed '{file_name}'!!")
