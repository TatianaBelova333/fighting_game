from typing import Dict, Optional

from app.players import PlayerUnit, EnemyUnit


class BaseSingleton(type):
    _instances: Dict[type, type] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Arena(metaclass=BaseSingleton):
    """Game Arena Class"""
    STAMINA_PER_ROUND = 1
    player: Optional[PlayerUnit] = None
    enemy: Optional[EnemyUnit] = None
    game_is_running = False
    battle_result = None

    def start_game(self, player: PlayerUnit, enemy: EnemyUnit) -> None:
        """Called once before a new game"""
        self.player = player
        self.enemy = enemy
        self.game_is_running = True
        self.battle_result = 'Ваш ход!'

    def _check_players_hp(self) -> Optional[str]:
        """Checks players' health points and returns the result of the game"""
        if self.player is not None and self.enemy is not None:
            if self.player.health_points <= 0 and self.enemy.health_points <= 0:
                self.battle_result = 'Ничья.'
            elif self.player.health_points <= 0:
                self.battle_result = f'Вы проиграли:('
            elif self.enemy.health_points <= 0:
                self.battle_result = f'Вы выиграли!'
        return self.battle_result

    def _stamina_regeneration(self) -> None:
        """Recovers players' stamina after each game round"""
        if self.player is not None and self.enemy is not None:
            self.player.stamina += self.STAMINA_PER_ROUND * self.player.unit_class.stamina_mod
            self.enemy.stamina += self.STAMINA_PER_ROUND * self.enemy.unit_class.stamina_mod
            if self.player.stamina > self.player.unit_class.max_stamina:
                self.player.stamina = self.player.unit_class.max_stamina
            if self.enemy.stamina > self.enemy.unit_class.max_stamina:
                self.enemy.stamina = self.enemy.unit_class.max_stamina


    def next_turn(self):
        """Returns the result of computer player's move"""
        res = self.enemy.hit(target=self.player)
        self._check_players_hp()
        return res

    def _end_game(self) -> None:
        """Sets default values"""
        self.game_is_running = False
        self._instances: Dict[type, type] = {}
        self.player = None
        self.enemy = None

    def player_hit(self):
        """Returns the result of both players"""
        res = self.player.hit(target=self.enemy)
        battle_result = self._check_players_hp()
        if battle_result == 'Ваш ход!':
            res += self.next_turn()
            self._stamina_regeneration()
        else:
            self._end_game()
        return res

    def player_use_skill(self) -> Optional[str]:
        """Returns the result of player's skill move and the computer's move"""
        if self.player is not None and self.enemy is not None:
            res = self.player.use_skill(target=self.enemy)
            if res is None:
                return 'Навык уже использован. Попробуйте другой вариант. '
            battle_result = self._check_players_hp()
            if battle_result == 'Ваш ход!':
                res += self.next_turn()
                self._stamina_regeneration()
            else:
                self._end_game()
            return res
        return None

