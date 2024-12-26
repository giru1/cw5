from functools import wraps
from typing import Dict
from flask import Flask, render_template, request, url_for
from werkzeug.utils import redirect

from controller import Game
from equipment import EquipmentData
from hero import Player, Hero, Enemy
from personages import personage_classes
from utils import load_equipment

EQUIPMENT: EquipmentData = load_equipment()

game = Game()


app = Flask(__name__)
app.url_map.strict_slashes = False

heroes: Dict[str, Hero] = dict()


def game_processing(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if game.game_processing:
            return func(*args, **kwargs)
        if game.game_results:
            return render_template("fight.html", heroes=heroes, result=game.game_results)
        return redirect(url_for("index"))
    return wrapper


def render_choose_template(*args, **kwargs) -> str:
    return render_template(
        "hero_choosing.html",
        classes=personage_classes.values(),
        equipment=EQUIPMENT,
        **kwargs,
    )


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/choose-hero", methods=["GET", "POST"])
def choose_hero():
    if request.method == "GET":
        return render_choose_template(header="Выберите героя")
    heroes["player"] = Player(
        class_=personage_classes[request.form["unit_class"]],
        weapon=EQUIPMENT.get_weapon(request.form["weapon"]),
        armor=EQUIPMENT.get_armor(request.form["armor"]),
        name=request.form["name"]
    )
    return redirect(url_for("choose_enemy"))


@app.route("/choose-enemy", methods=["GET", "POST"])
def choose_enemy():
    if request.method == "GET":
        return render_choose_template(header="Выберите врага")
    heroes["enemy"] = Enemy(
        class_=personage_classes[request.form["unit_class"]],
        weapon=EQUIPMENT.get_weapon(request.form["weapon"]),
        armor=EQUIPMENT.get_armor(request.form["armor"]),
        name=request.form["name"]
    )
    return redirect(url_for("fight"))


@app.route("/fight")
def fight():
    if "player" in heroes and "enemy" in heroes:
        game.run(**heroes)
        return render_template("fight.html", heroes=heroes, result="Fight!")
    return redirect(url_for("index"))


@app.route("/fight/hit")
@game_processing
def hit():
    return render_template("fight.html", heroes=heroes, result=game.player_hit())


@app.route("/fight/use-skill")
@game_processing
def use_skill():
    return render_template("fight.html", heroes=heroes, result=game.player_use_skill())


@app.route("/fight/pass-turn")
@game_processing
def pass_turn():
    return render_template("fight.html", heroes=heroes, result=game.next_turn())


@app.route("/fight/end-fight")
def end_fight():
    return redirect(url_for("index"))


if __name__ == '__main__':
    app.run()
