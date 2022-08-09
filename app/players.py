from __future__ import annotations
from abc import ABC, abstractmethod
from app.equipment import Weapon, Armor
from app.characters import UnitClass
from random import randint
from typing import Optional


class BaseUnit(ABC):
    """Base UnitClass"""
    def __init__(self, name: str, unit_class: UnitClass, weapon: Weapon, armor: Armor) -> None:
        """UnitClass is used for initializing Unit"""
        self.name = name
        self.unit_class = unit_class
        self.hp = unit_class.max_health
        self.stamina = unit_class.max_stamina
        self.weapon = weapon
        self.armor = armor
        self._is_skill_used = False

    @property
    def health_points(self) -> float:
        """Returns players' remaining health points rounded off to 1 digit"""
        return round(self.hp, 1)

    @property
    def stamina_points(self) -> float:
        """Returns players' remaining stamina points rounded off to 1 digit"""
        return round(self.stamina, 1)

    def is_enough_stamina_per_hit(self) -> bool:
        """Checks if player has enough stamina points to hit"""
        return self.stamina >= self.weapon.stamina_per_hit

    def is_enough_stamina_per_turn(self) -> bool:
        """Checks if player has enough stamina points to use armor"""
        return self.stamina >= self.armor.stamina_per_turn

    def _count_damage(self, target: BaseUnit) -> int:
        """Calculates attacking player's damage inflicted on target player"""
        attacker_damage = self.weapon.damage * self.unit_class.attack_mod
        self.stamina -= self.weapon.stamina_per_hit
        if target.is_enough_stamina_per_turn():
            target.stamina -= target.armor.stamina_per_turn
            target_armor = target.armor.defence * target.unit_class.armor_mod
        else:
            target_armor = 0
        damage = attacker_damage - target_armor
        if damage > 0:
            target.get_damage(damage)
            return round(damage, 1)
        return 0

    def get_damage(self, damage: int) -> float:
        """Adjust player's health points according to calculated damage (self._count_damage())"""
        self.hp -= damage
        return self.health_points

    @abstractmethod
    def hit(self, target: BaseUnit) -> Optional[str]:
        pass

    def use_skill(self, target: BaseUnit) -> Optional[str]:
        """Returns player's skill effect if skill is not used (can only be used once)"""
        if not self._is_skill_used:
            self._is_skill_used = True
            return self.unit_class.skill.use(user=self, target=target)
        return None


class PlayerUnit(BaseUnit):
    """User's Player Class"""

    def hit(self, target: BaseUnit) -> str:
        """Returns the result of player's hit"""
        if not self.is_enough_stamina_per_hit():
            return f"Ваш герой {self.name.upper()} попытался использовать {self.weapon.name.upper()}, но у него не " \
                   f"хватило выносливости.<br> "
        else:
            damage = self._count_damage(target)
            if damage:
                return f"Ваш герой {self.name.upper()}, используя {self.weapon.name.upper()}, " \
                       f"пробивает защиту {target.armor.name.upper()} соперника и наносит {damage} урона.<br>"
            else:
                return f"Ваш герой {self.name.upper()}, используя {self.weapon.name.upper()}, наносит удар, " \
                       f"но защита {target.armor.name.upper()} cоперника его останавливает.<br>"


class EnemyUnit(BaseUnit):
    """Computer PLayer Class"""

    def hit(self, target: BaseUnit) -> Optional[str]:
        """Returns the result of computer's hit. Computer player has a 10% chance of using skill (once)"""
        if not self.is_enough_stamina_per_hit():
            return f"Соперник {self.name.upper()} попытался использовать {self.weapon.name.upper()}, но у него не хватило " \
                   f"выносливости.  "
        else:
            if not self._is_skill_used:
                # one-in-ten chance to use skill
                one_in_ten_chance = randint(0, 9)
                if one_in_ten_chance == 0:
                    res = self.use_skill(target=target)
                    return res
            damage = self._count_damage(target)
            if damage:
                return f"Соперник {self.name.upper()}, используя {self.weapon.name.upper()} " \
                       f"пробивает Вашу защиту {target.armor.name.upper()}  и наносит {damage} урона.  "
            else:
                return f"Соперник {self.name.upper()}, используя {self.weapon.name.upper()}, наносит удар, " \
                       f"но Ваша защита {target.armor.name.upper()} его останавливает."