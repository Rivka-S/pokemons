from flask import Flask, request, render_template, Response
import pymysql
import json
import queries
from server import connect_to_pokeapi

app = Flask(__name__, static_url_path='',
            static_folder='static',
            template_folder='templates')
port_number = 3000


@app.route('/')
def root(): return render_template('index.html')


@app.route('/trainer')
def trainer():
    name = request.args.get("name")
    #if name == "":
     #   return render_template('new_trainer.html')
    return render_template('trainer.html', name=name)


@app.route('/trainer/new_trainer/<name>',methods=["POST"])
def new_trainer(name):
    #town = request.args.get("town")
    try:
        queries.insert_trainer(name, "town")
    except pymysql.err.IntegrityError:
        return render_template('massage.html', text="this name is already exist")
    return render_template('trainer.html', name=name)


@app.route('/types/<poke_name>', methods=["PATCH"])
def update_types(poke_name):
    types = connect_to_pokeapi.get_types(poke_name)
    queries.update_types(poke_name, types)
    return json.dumps({"updated": poke_name})


@app.route('/pokemons/trainer/<trainer>')
def get_pokemon_by_trainer(trainer):
    return json.dumps(queries.findRoster(trainer))


@app.route('/trainers/<pokemon>')
def get_trainer_by_pokemon(pokemon):
    return json.dumps(queries.findOwners(pokemon))


@app.route('/pokemons/types/<type_name>')
def get_poke_by_type(type_name):
    pokes = queries.findByType(type_name)
    return json.dumps(pokes)


@app.route('/pokemons', methods=["POST"])
def add():
    pokemon = request.get_json()

    try:
        queries.insert_pokemon(pokemon)
    except pymysql.err.IntegrityError:
        return json.dumps({"exist": pokemon["name"]}), 201
    return json.dumps({"created": pokemon["name"]}), 201


@app.route('/pokemon/<trainer_name>/<poke_name>', methods=["DELETE"])
def delete_poke_from_trainer(trainer_name, poke_name):
    queries.delete_poke_trainer(poke_name, trainer_name)
    return json.dumps({"deleted": poke_name}), 204


@app.route('/pokemone/<trainer_name>/<poke_name>', methods=["POST"])
def add_poke_to_trainer(trainer_name, poke_name):
    try:
        queries.insert_poke_to_trainer(poke_name, trainer_name)
    except pymysql.err.IntegrityError:
        return {"exist": poke_name}, 201
    # except pymysql.err.NoneType:
    #    return {"aaaaaaaaaaaaaaa":poke_name},201
    res = {"created": poke_name + "owens by" + trainer_name}
    print(type(res))
    return res, 201


@app.route('/trainer/add_poke/<trainer_name>')
def add_poke(trainer_name):
    print()
    poke_name = request.args.get("poke_name")
    if not poke_name:
        return render_template('add_poke.html', text="oops you didn't enter pokemon name")
    res = add_poke_to_trainer(trainer_name, poke_name)
    print(type(res[0]))
    if res[0].get('exist'):
        text = poke_name + " is almost exist!"
    else:
        text = "add " + poke_name + " to " + trainer_name
    return render_template('add_poke.html', text=text)


@app.route('/trainer/del_poke/<trainer_name>')
def del_poke(trainer_name):
    poke_name = request.args.get("poke_name")
    if not poke_name:
        return render_template('del_poke.html', text="oops you didn't enter pokemon name!", name=trainer_name,
                               poke_name=poke_name)
    delete_poke_from_trainer(trainer_name, poke_name)
    text = "delete " + poke_name + " from " + trainer_name
    return render_template('del_poke.html', text=text, name=trainer_name, poke_name=poke_name)


@app.route('/trainer/get_pokemon/<train_name>')
def poke_of_trainer(train_name):
    pokes = queries.findRoster(train_name)
    return render_template('pokemon_by_trainer.html', name=train_name, pokes=pokes)


if __name__ == '__main__':
    app.run(port=port_number)


    