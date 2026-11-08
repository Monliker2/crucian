"""Исследовательское судно «Карась-1» (water)."""

import math

DIRECTIONS = ("north", "south", "east", "west")
ENVIRONMENTS = ("water", "land")
OBSTACLES = ("open_water", "narrow_channel", "net")
ENERGY_PER_KM = 2.0
RECORDING_COST = 1.0
CHANNEL_MAX_LENGTH_CM = 30.0


class CrazyVehicleError(Exception):
    """Базовое исключение всех безумных средств передвижения."""


class KarasError(CrazyVehicleError):
    """Базовое исключение «Карася-1»."""


class KarasNoEnergy(KarasError):
    """Не хватает энергии для действия."""


class KarasCannotMoveOnLand(KarasError):
    """Карась не может двигаться по суше."""


def _number(value: object, label: str) -> float:
    """Проверить, что значение - конечное число (bool не считается числом)."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{label} должен быть числом")
    if not math.isfinite(value):
        raise ValueError(f"{label} должен быть конечным числом")
    return value


def _positive(value: object, label: str) -> float:
    """Проверить, что значение - число больше нуля."""
    number = _number(value, label)
    if number <= 0:
        raise ValueError(f"{label} должен быть больше 0")
    return number


class CrucianOne:
    """Судно «Карась-1»: плывёт, снимает на GoPro, проверяет препятствия."""

    def __init__(self, name: str, mass_kg: float, body_length_cm: float,
                 max_speed_kmh: float, max_depth_m: float,
                 energy: float = 100.0) -> None:
        """Создать судно. Нарушение контракта - TypeError или ValueError."""
        if not isinstance(name, str):
            raise TypeError("name должен быть строкой")
        _number(mass_kg, "mass_kg")
        _number(body_length_cm, "body_length_cm")
        _number(max_speed_kmh, "max_speed_kmh")
        _number(max_depth_m, "max_depth_m")
        _number(energy, "energy")

        if not name.strip():
            raise ValueError("name не должен быть пустым")
        _positive(mass_kg, "mass_kg")
        _positive(body_length_cm, "body_length_cm")
        _positive(max_speed_kmh, "max_speed_kmh")
        _positive(max_depth_m, "max_depth_m")
        if not 0 <= energy <= 100:
            raise ValueError("energy должна быть в диапазоне 0...100")

        self._name = name.strip()
        self._mass_kg = mass_kg
        self._body_length_cm = body_length_cm
        self._max_speed_kmh = max_speed_kmh
        self._max_depth_m = max_depth_m
        self._energy = energy
        self._position_km = 0.0
        self._is_swimming = True
        self._gopro_recording = False

    @property
    def name(self) -> str:
        return self._name

    @property
    def mass_kg(self) -> float:
        return self._mass_kg

    @property
    def body_length_cm(self) -> float:
        return self._body_length_cm

    @property
    def max_speed_kmh(self) -> float:
        return self._max_speed_kmh

    @property
    def max_depth_m(self) -> float:
        return self._max_depth_m

    @property
    def energy(self) -> float:
        return self._energy

    @property
    def position_km(self) -> float:
        return self._position_km

    @property
    def is_swimming(self) -> bool:
        return self._is_swimming

    @property
    def gopro_recording(self) -> bool:
        return self._gopro_recording

    def move(self, distance_km: float, direction: str, depth_m: float = 0.0,
             environment: str = "water") -> float:
        """Проплыть distance_km и вернуть время в часах."""
        # 1. типы
        _number(distance_km, "distance_km")
        if not isinstance(direction, str):
            raise TypeError("direction должен быть строкой")
        _number(depth_m, "depth_m")
        if not isinstance(environment, str):
            raise TypeError("environment должен быть строкой")

        # 2. значения
        if distance_km <= 0:
            raise ValueError("distance_km должен быть больше 0")
        if direction not in DIRECTIONS:
            raise ValueError("неизвестное направление")
        if environment not in ENVIRONMENTS:
            raise ValueError("неизвестная среда")
        if not 0 <= depth_m <= self._max_depth_m:
            raise ValueError("глубина вне диапазона 0...max_depth_m")

        # 3. ограничения судна
        if environment == "land":
            raise KarasCannotMoveOnLand("Карась не ездит по суше")
        cost = ENERGY_PER_KM * distance_km
        if cost > self._energy:
            raise KarasNoEnergy("не хватает энергии")

        self._energy -= cost
        self._position_km += distance_km
        return distance_km / self._max_speed_kmh

    def can_pass(self, obstacle: str) -> bool:
        """Может ли судно пройти препятствие."""
        if not isinstance(obstacle, str):
            raise TypeError("obstacle должен быть строкой")
        if obstacle not in OBSTACLES:
            raise ValueError("неизвестное препятствие")
        if obstacle == "open_water":
            return True
        if obstacle == "narrow_channel":
            return self._body_length_cm <= CHANNEL_MAX_LENGTH_CM
        return False

    def start_recording(self) -> None:
        """Включить GoPro (-1 энергии один раз; повтор ничего не делает)."""
        if self._gopro_recording:
            return
        if self._energy < RECORDING_COST:
            raise KarasNoEnergy("не хватает энергии для записи")
        self._energy -= RECORDING_COST
        self._gopro_recording = True

    def stop_recording(self) -> None:
        """Выключить GoPro (бесплатно, повтор безопасен)."""
        self._gopro_recording = False

    def get_status(self) -> dict:
        """Вернуть снимок состояния (копию, не связанную с объектом)."""
        return {
            "name": self._name,
            "energy": self._energy,
            "position_km": self._position_km,
            "is_swimming": self._is_swimming,
            "gopro_recording": self._gopro_recording,
        }
