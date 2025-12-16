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
