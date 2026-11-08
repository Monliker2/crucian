# Карась-1 (crucian_one.py)

Реализация исследовательского судна «Карась-1» по `SPEC.md` и `TEST_CASES.md`.

Файл: `crucian_one.py` (класс `CrucianOne` и исключения `CrazyVehicleError`, `KarasError`, `KarasNoEnergy`, `KarasCannotMoveOnLand`).

## Как запустить тесты

Положите `crucian_one.py` в корень репозитория (рядом с папкой `tests/`) и выполните:

```
PYTHONPATH=. python -m unittest discover -s tests -v
```

В Windows PowerShell: `$env:PYTHONPATH="."; python -m unittest discover -s tests -v`.

Нужен Python 3.9+. Внешние библиотеки не нужны.

## Пример

```python
from crucian_one import CrucianOne

fish = CrucianOne("Карась-1", 0.4, 25.0, 4.0, 3.0)
fish.start_recording()
print(fish.move(2, "east"))   # 0.5 часа
print(fish.get_status())
```
