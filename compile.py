from alice_yacc import parser
from structs import *

try:
    file_name = input('>Insert file name: ')
    test_file = open(file_name)
    source_code = test_file.read()
    test_file.close()
except FileNotFoundError:
    print('Error! Wrong file name!')
    quit()
parser.parse(source_code)
print(f"Successfully parsed '{file_name}'!!")
