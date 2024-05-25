from dataclasses import dataclass
from app.skills import Skill, FuryPunch, HardShot


@dataclass
class UnitClass:
    name: str
    max_health: float
    max_stamina: float
    attack_mod: float
    stamina_mod: float
    armor_mod: float
    skill: Skill


WarriorClass = UnitClass(
    name='Воин',
    max_health=60.0,
    max_stamina=30.0,
    attack_mod=0.8,
    stamina_mod=0.9,
    armor_mod=1.2,
    skill=FuryPunch()
)


ThiefClass = UnitClass(
    name='Вор',
    max_health=50.0,
    max_stamina=25.0,
    attack_mod=1.5,
    stamina_mod=1.2,
    armor_mod=1.0,
    skill=HardShot()
)

unit_classes = {
    ThiefClass.name: ThiefClass,
    WarriorClass.name: WarriorClass,
}


if __name__ == '__main__':
    pass
