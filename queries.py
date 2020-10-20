import pymysql
import json

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    db="mysql",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)

if connection.open:
    print("the connection is opened")


def heaviest_poke():
    res = None
    with connection.cursor() as cursor:
        query = f'''select * from pokemons where weight = (select max(weight) from pokemons);'''
        cursor.execute(query)
        res = cursor.fetchone()
    return res


def findByType(type):
    res = []
    with connection.cursor() as cursor:
        query = f'''select name from pokemons join type_of_poke on id = pokemon_id where type_name = '{type}';'''
        cursor.execute(query)
        res = cursor.fetchall()
    return [i["name"] for i in res]


def findOwners(poke_name):
    res = []
    with connection.cursor() as cursor:
        query = f"select owner from pokemons join pokemon_ownes_by on id = pokemon  where name = '{poke_name}';"
        cursor.execute(query)
        res = cursor.fetchall()

    return [i["owner"] for i in res]


def findRoster(owner):
    res = []
    with connection.cursor() as cursor:
        query = f"select pokemons.name from pokemons join pokemon_ownes_by join owners on id = pokemon and owner = owners.name where owners.name = '{owner}';"
        cursor.execute(query)
        res = cursor.fetchall()

    return [i["name"] for i in res]


def insert_types(pokemon):
    for type_poke in pokemon["types"]:
        try:
            with connection.cursor() as cursor:
                query = f'''INSERT into type_of_poke values ({pokemon["id"]}, '{type_poke}');'''
                cursor.execute(query)
                connection.commit()
        except pymysql.err.IntegrityError:
            pass


def insert_pokemon(pokemon):
    with connection.cursor() as cursor:
        query = f'''INSERT into pokemons values ({pokemon["id"]}, '{pokemon["name"]}',  {pokemon["height"]}, {pokemon["weight"]});'''
        cursor.execute(query)
        connection.commit()
    insert_types(pokemon)


def get_id(poke_name):
    with connection.cursor() as cursor:
        query = f'''select id from pokemons where name = '{poke_name}';'''
        cursor.execute(query)
        id = cursor.fetchone()
    return id


def insert_poke_to_trainer(poke_name, trainer_name):
    id = get_id(poke_name)
    with connection.cursor() as cursor:
        query = f'''INSERT into pokemon_ownes_by values ({id["id"]}, '{trainer_name}');'''
        cursor.execute(query)
        connection.commit()


def update_types(poke_name, types):
    poke = get_id(poke_name)
    poke["types"] = types
    insert_types(poke)


def delete_poke_trainer(poke_name, trainer_name):
    id = get_id(poke_name)
    with connection.cursor() as cursor:
        query = f'''delete from pokemon_ownes_by where owner = '{trainer_name}' and pokemon = {id["id"]};'''
        cursor.execute(query)
        connection.commit()

def insert_trainer(name,town=""):
        with connection.cursor() as cursor:
            query = f'''INSERT into owners  values ('{name}', '{town}');'''
            cursor.execute(query)
            connection.commit()
print(findByType("grass"))
