from typing import Type

from flask import Flask, render_template, request, redirect, url_for

from app.base import Arena
from app.characters import unit_classes
from app.equipment import Equipment
from app.players import PlayerUnit, EnemyUnit


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


heroes = {
    "player": PlayerUnit,
    "enemy": EnemyUnit,
}


arena = Arena()


@app.route("/")
def menu_page():
    return render_template('index.html')


@app.route("/choose-hero/", methods=['POST', 'GET'])
def choose_hero():
    result = {
        'header': 'Выберите героя',
        'classes': unit_classes,
        'weapons': Equipment().get_weapons_names(),
        'armors': Equipment().get_armors_names(),
    }
    if request.method == 'GET':
        return render_template('hero_choosing.html', result=result)
    if request.method == 'POST':

        name = request.form.get('name')
        unit_class = request.values.get('unit_class')
        weapon_name = request.values.get('weapon')
        armor_name = request.values.get('armor')

        heroes['player'] = heroes['player'](
            name=name,
            unit_class=unit_classes[unit_class],
            weapon=Equipment().get_weapon(weapon_name=weapon_name),
            armor=Equipment().get_armor(armor_name=armor_name),
        )
        return redirect(url_for("choose_enemy"))


@app.route("/choose-enemy/", methods=['POST', 'GET'])
def choose_enemy():
    result = {
        'header': 'Выберите врага',
        'classes': unit_classes,
        'weapons': Equipment().get_weapons_names(),
        'armors': Equipment().get_armors_names()
    }

    if request.method == 'GET':
        return render_template('hero_choosing.html', result=result)

    if request.method == 'POST':
        name = request.values.get('name')
        unit_class = request.values.get('unit_class')
        weapon_name = request.values.get('weapon')
        armor_name = request.values.get('armor')

        heroes['enemy'] = heroes.get('enemy')(
            name=name,
            unit_class=unit_classes[unit_class],
            weapon=Equipment().get_weapon(weapon_name=weapon_name),
            armor=Equipment().get_armor(armor_name=armor_name),
            )
        return redirect(url_for("start_fight"))


@app.route("/fight/")
def start_fight():
    arena.start_game(player=heroes['player'], enemy=heroes['enemy'])
    return render_template('fight.html', heroes=heroes, battle_result='Бой начался!')


@app.route("/fight/hit")
def hit():
    if arena.battle_result != 'Ваш ход!':
        arena.battle_result = None
        return render_template('fight.html', heroes=heroes, battle_result='Игра окончена.')
    result = arena.player_hit()
    battle_result = arena.battle_result
    return render_template('fight.html', heroes=heroes, result=result, battle_result=battle_result)


@app.route("/fight/use-skill")
def use_skill():
    if arena.battle_result != 'Ваш ход!':
        arena.battle_result = None
        return render_template('fight.html', heroes=heroes, battle_result='Игра окончена.')
    result = arena.player_use_skill()
    battle_result = arena.battle_result
    return render_template('fight.html', heroes=heroes, result=result, battle_result=battle_result)


@app.route("/fight/pass-turn")
def pass_turn():
    if arena.battle_result != 'Ваш ход!':
        arena.battle_result = None
        return render_template('fight.html', heroes=heroes, battle_result='Игра окончена.')
    result = arena.next_turn()
    battle_result = arena.battle_result
    return render_template('fight.html', heroes=heroes, result=result, battle_result=battle_result)


@app.route("/fight/end-fight")
def end_fight():
    global heroes
    heroes = {
        "player": PlayerUnit,
        "enemy": EnemyUnit,
    }
    return render_template("index.html")


if __name__ == "__main__":
    app.run()
