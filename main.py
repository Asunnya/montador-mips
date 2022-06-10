from utility import *
from sys import argv

lista = read_asm()
labels = create_labels(lista)

transforming_instruction(lista, labels)
if "-v" in argv:
    to_read()
