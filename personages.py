from abc import ABC
from typing import Type, Dict
from skills import Skill, ferocious_kick, powerful_thrust


class Personage(ABC):
    name: str = NotImplemented
    max_health: float = NotImplemented
    max_stamina: float = NotImplemented
    stamina: float = NotImplemented
    attack: float = NotImplemented
    armor: float = NotImplemented
    skill: Skill = NotImplemented


class Warrior(Personage):
    name = "Воин"
    max_health: float = 60.0
    max_stamina: float = 30.0
    stamina: float = 0.9
    attack: float = 0.8
    armor: float = 1.2
    skill: Skill = ferocious_kick


class Robber(Personage):
    name = "Вор"
    max_health: float = 50.0
    max_stamina: float = 25.0
    stamina: float = 1.2
    attack: float = 1.5
    armor: float = 1.0
    skill: Skill = powerful_thrust


personage_classes: Dict[str, Type[Personage]] = {
    Warrior.name: Warrior,
    Robber.name: Robber
}