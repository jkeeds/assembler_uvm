# Конфигурационное управление
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