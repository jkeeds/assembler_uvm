# Конфигурационное управление ИКБО-70-24

## Описание
Проект реализует ассемблер и интерпретатор для учебной виртуальной машины (УВМ). Программа включает три завершённых этапа разработки, каждый из которых добавляет новую функциональность.

## Вариант 12
Структура репозитория:
stage1/
├── README.md
├── main.py
└── test_program.asm

# stage 1
## Язык ассемблера
Поддерживаются следующие инструкции:
- `LOADC CONST, REG` - загрузить константу в регистр
- `LOAD REG_DST, REG_PTR` - загрузить значение из памяти в регистр
- `STORE REG_SRC, REG_PTR, OFFSET` - сохранить значение регистра в память
- `ROR REG, MEM` - циклический сдвиг вправо
Синтаксис:  
INSTRUCTION ARG1, ARG2, ...
; комментарий

## Запуск
```bash
python3 main.py asm <source.asm> <output.bin> test
```
# stage 2
## Структура
stage2/
├── README.md
├── main.py
├── test_program.asm
└── all_instructions.asm
## Запуск
Сборка программы в бинарный файл:
```bash
python3 main.py asm <source.asm> <output.bin>
```
test — режим тестирования промежуточного представления
Если test не указан, создается бинарный файл <output.bin>.

## Проверка бинарного файла
После сборки можно вывести размер:
```bash
ls -l output.bin   # Linux/macOS
dir output.bin     # Windows
```
## Пример вывода для test_program
54 00 00 A4 20 00 06 A1 00 0B 00 00 00

# stage3
## структура
stage3/
├── README.md
├── main.py
├── test_program.asm
└── copy_array.asm
после запуска программы добавляется:
├── dump.csv
└── output.bin
## запуск
python main.py asm copy_array.asm output.bin
python main.py run output.bin dump.csv 0:20
## пример dump.csv на output.bin от all_instructions.asm
address,value
0,42
1,100
2,0
3,0
4,0
5,0
6,0
7,0
8,0
9,0
10,0
11,0
12,0
13,0
14,0
15,0
16,0
17,0
18,0
19,0
## вывод
73
*количество байт для copy_array.asm