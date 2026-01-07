from flask import request, jsonify
from config import app, db
from models import Hero, Power, HeroPower



@app.route('/heroes')
def get_heroes():
    heroes = Hero.query.all()
    return jsonify([
        hero.to_dict(only=('id', 'name', 'super_name'))
        for hero in heroes
    ]), 200


@app.route('/heroes/<int:id>')
def get_hero(id):
    hero = Hero.query.get(id)
    if not hero:
        return {"error": "Hero not found"}, 404
    return hero.to_dict(), 200



@app.route('/powers')
def get_powers():
    powers = Power.query.all()
    return jsonify([power.to_dict() for power in powers]), 200


@app.route('/powers/<int:id>')
def get_power(id):
    power = Power.query.get(id)
    if not power:
        return {"error": "Power not found"}, 404
    return power.to_dict(), 200


@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if not power:
        return {"error": "Power not found"}, 404

    try:
        power.description = request.json.get('description')
        db.session.commit()
        return power.to_dict(), 200
    except ValueError as e:
        return {"errors": [str(e)]}, 400



@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    try:
        hero_power = HeroPower(
            strength=request.json['strength'],
            hero_id=request.json['hero_id'],
            power_id=request.json['power_id']
        )
        db.session.add(hero_power)
        db.session.commit()
        return hero_power.to_dict(), 201
    except ValueError as e:
        return {"errors": [str(e)]}, 400


if __name__ == '__main__':
    app.run(port=5555, debug=True)

