# montador-mips
Repositório para a atividade da disciplina Arquiteturas de Computadores

# O Projeto
O projeto recebe como entrada, um arquivo com a extensão ".asm" que deve conter o código no formato do ISA do MIPS 32 bits [MIPS](www.mips.com) e gera como saída um arquivo contendo o código em binário

# Versão exigida do Python
Utilize o [Python](https://www.python.org/downloads/) 3.9+
# Como instalar
``` 
git clone https://github.com/Pruzny/montador-mips/
cd montador-mips
pip install -r requirements.txt
```
# Como utilizar
```
py3 main.py
```
# Entrada

Caso queira utilizar um arquivo próprio escrito em .asm, coloque o arquivo no mesmo diretório que o "main.py" está localizado, renomeie esse arquivo como "entrada.asm"

Por padrão, é utilizado um arquivo base "base/exemplo.asm"

# Flags

| Flag | Função                     |
|------|----------------------------|
| -v   | Imprime o arquivo de saída | 
| -t   | Arquivo de saída em *  *.txt* |


# Exemplo

```
 py3 main.py -v -t
```
```
00000000000000010001000000100000
00000000011001000010100000100010
00000000110001110100000000100100
00000001001010100101100000100101
00000001110000000110011111000000
00000010010000001000011111000010
00000001000000000000000000001000
00100010110110001000000000000000
10001111001110110111111111111111
10101111100111101000000000000000
00010001111111111111111111111110
00010101010010010000000000000001
00001000000000000000000000000011
00001100000000000000000000001001
```
