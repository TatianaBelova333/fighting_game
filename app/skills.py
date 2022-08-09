from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from app.players import BaseUnit


class Skill(ABC):
    """Base Skill Class"""
    user = None
    target = None

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def stamina_per_use(self):
        pass

    @property
    @abstractmethod
    def damage(self):
        pass

    def _is_stamina_enough(self) -> Optional[bool]:
        """Checks player's stamina points for using skill"""
        if self.user is not None:
            return self.user.stamina >= self.stamina_per_use
        return None

    def use(self, user: BaseUnit, target: BaseUnit) -> str:
        """returns the result of skill used by BaseUnit class"""
        self.user = user
        self.target = target
        if self._is_stamina_enough():
            self.target.hp -= self.damage
            self.user.stamina -= self.stamina_per_use
            return f'{self.user.name.upper()} использует {self.name.upper()} и наносит {self.damage} очков урона ' \
                   f'сопернику {self.target.name.upper()}.<br>'
        return f"{self.user.name.upper()} попытался использовать {self.name.upper()}, но у него не хватило " \
               f"выносливости.<br>"


class FuryPunch(Skill):
    name = "Свирепый пинок"
    stamina_per_use = 6
    damage = 12


class HardShot(Skill):
    name = "Мощный укол"
    stamina_per_use = 5
    damage = 12

