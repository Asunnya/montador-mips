from utility import *
from sys import argv

reserved = {
    "-v",
    "-t",
}

flags = {
    "-v": "verbose",
    "-t": "txt",
}

options = {
    "verbose": False,
    "txt": False,
}

for flag in reserved:
    if flag in argv:
        options[flags[flag]] = True
        argv.remove(flag)

lista = read_asm()
labels = create_labels(lista)

transforming_instruction(lista, labels, options["txt"])
if options["verbose"]:
    to_read(options["txt"])
