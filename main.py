from utility import *

lista = read_asm()
labels = create_labels(lista)

print(lista)
print(labels)

transforming_instruction(lista, labels)
to_read()
