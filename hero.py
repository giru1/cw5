from __future__ import annotations
from abc import ABC, abstractmethod
from random import randint
from typing import Type, Optional

from equipment import Weapon, Armor
from personages import Personage

BASE_STAMINA_PER_ROUND = 0.4


class Hero(ABC):
    def __init__(self, class_: Type[Personage], weapon: Weapon, armor: Armor, name: str):
        self.class_ = class_
        self.weapon = weapon
        self.armor = armor
        self._stamina = self.class_.max_stamina
        self._health = self.class_.max_health
        self.skill_used: bool = False
        self.name = name

    @property
    def health(self):
        """Возвращает значение здоровья, округленное до десятых долей"""
        return round(self._health, 1)

    @health.setter
    def health(self, value):
        self._health = value

    @property
    def stamina(self):
        return round(self._stamina, 1)

    @stamina.setter
    def stamina(self, value) :
        self._stamina = value

    @property
    def _total_armor(self) -> float:
        """Если у игрока достаточно выносливости, чтобы применить защиту,
        функция вернет итоговую броню, которая равна броне умноженной на коэффициент брони класса.
        Если выносливости не достаточно - вернет 0.
        И если броня применена, то выносливость уменьшается на величину выносливости брони.
        """
        if self.stamina >= self.armor.stamina_per_turn:
            self.stamina -= self.armor.stamina_per_turn
            return self.armor.defence * self.class_.armor
        return 0

    def _hit(self, target: Hero) -> Optional[float]:
        """Если у игрока достаточно выносливости, чтобы применить оружие,
        функция вернет итоговый урон, который равен урону оружия умноженному на коэффициент атаки класса
        минус защита противника.
        Если выносливости не достаточно - вернет 0.
        И если оружие применено, то выносливость уменьшается на величину выносливости оружия.
        """
        if self.stamina < self.weapon.stamina_per_hit:
            return None
        hero_damage = self.weapon.damage * self.class_.attack
        delta_damage = hero_damage - target._total_armor
        if delta_damage < 0:
            return 0
        self.stamina -= self.weapon.stamina_per_hit
        return round(delta_damage, 1)

    def take_damage(self, damage: float):
        """
        Уменьшает здоровье на величину урона.
        """
        self.health -= damage
        if self.health < 0:
            self.health = 0

    def use_skill(self) -> Optional[float]:
        """Если умение еще не применялось и у игрока достаточно выносливости, чтобы применить умение,
        функция вернет урон умения.
        Если выносливости не достаточно - вернет None.
        И если умение применено, то выносливость уменьшается на величину выносливости умения.
        """
        if self.stamina >= self.class_.skill.stamina and not self.skill_used:
            self.stamina -= self.class_.skill.stamina
            self.skill_used = True
            return self.class_.skill.damage
        return None

    def regenerate_stamina(self):
        """Увеличивает выносливость на произведение коэффициента выносливости класса
        и константы выносливости раунда.
        """
        delta_stamina = BASE_STAMINA_PER_ROUND * self.class_.stamina
        self.stamina += delta_stamina
        if self.stamina > self.class_.max_stamina:
            self.stamina = self.class_.max_stamina

    @abstractmethod
    def hit(self, target: Hero) -> Optional[float]:
        pass


class Player(Hero):
    """
    Возвращает величину урона
    """
    def hit(self, target: Hero) -> Optional[float]:
        return self._hit(target)


class Enemy(Hero):
    """
    Возвращает величину урона от применения оружия или умения.
    Вероятность использования умения у врага равна 10%.
    """
    def hit(self, target: Hero) -> Optional[float]:
        if randint(1, 100) < 11 and self.stamina >= self.class_.skill.stamina and not self.skill_used:
            self.use_skill()
        return self._hit(target)
