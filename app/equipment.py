from dataclasses import dataclass, field
from typing import List, Optional
from random import uniform
import marshmallow_dataclass
import marshmallow
import json


@dataclass
class Armor:
    id: int
    name: str
    defence: float
    stamina_per_turn: float


@dataclass
class Weapon:
    id: int
    name: str
    min_damage: float
    max_damage: float
    stamina_per_hit: float

    @property
    def damage(self):
        return round(uniform(self.min_damage, self.max_damage), 1)


@dataclass
class EquipmentData:
    weapons: list = field(default_factory=List[Weapon])
    armors: list = field(default_factory=List[Armor])


class Equipment:
    """Player's Equipment class"""
    def __init__(self):
        self.equipment = self._get_equipment_data()

    def get_weapon(self, weapon_name: str) -> Optional[Weapon]:
        """Returns Weapon class instance by weapon name"""
        for weapon in self.get_weapons_names():
            if weapon.name == weapon_name:
                return weapon

    def get_armor(self, armor_name: str) -> Optional[Armor]:
        """Returns Armor class instance by armor name"""
        for armor in self.get_armors_names():
            if armor.name == armor_name:
                return armor

    def get_weapons_names(self) -> List[Weapon]:
        """Returns list of Weapon class instances"""
        weapons_schema = marshmallow_dataclass.class_schema(Weapon)
        weapons = list(map(lambda weapon: weapons_schema().load(weapon), self.equipment.weapons))
        return weapons

    def get_armors_names(self) -> List[Armor]:
        """Returns list of Armor class instances"""
        armor_schema = marshmallow_dataclass.class_schema(Armor)
        armors = list(map(lambda armor: armor_schema().load(armor), self.equipment.armors))
        return armors

    @staticmethod
    def _get_equipment_data() -> EquipmentData | list:
        """Loads data from json file and returns EquipmentData instance """
        try:
            with open("./data/equipment.json", 'r', encoding='utf-8') as file:
                data = json.load(file)
                equipment_schema = marshmallow_dataclass.class_schema(EquipmentData)
                return equipment_schema().load(data)
        except (FileNotFoundError, json.JSONDecodeError, marshmallow.exceptions.ValidationError):
            raise