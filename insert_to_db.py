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


def insert_owner(owner, poke_id):
    try:
        with connection.cursor() as cursor:
            query = f'''INSERT into owners  values ('{owner["name"]}', '{owner["town"]}');'''
            cursor.execute(query)
            connection.commit()
            query = f'''insert into pokemon_ownes_by values( {poke_id}, '{owner["name"]}') '''
            cursor.execute(query)
            connection.commit()
    except pymysql.err.IntegrityError:
        with connection.cursor() as cursor:
            query = f'''insert into pokemon_ownes_by values( {poke_id}, '{owner["name"]}') '''
            cursor.execute(query)
            connection.commit()


def insert_owners(pokemon):
    for owner in pokemon["ownedBy"]:
        insert_owner(owner, pokemon["id"])


def insert_poke(pokemon):
    with connection.cursor() as cursor:
        query = f'''INSERT into pokemons values ({pokemon["id"]}, '{pokemon["name"]}',  {pokemon["height"]}, {pokemon["weight"]});'''
        cursor.execute(query)
        connection.commit()
        query = f'''INSERT into type_of_poke values ({pokemon["id"]}, '{pokemon["type"]}');'''
        cursor.execute(query)
        connection.commit()
        insert_owners(pokemon)


def insert_data(poke_data):
    for pokemon in poke_data:
        insert_poke(pokemon)


if __name__ == "__main__":
    json_file = open("poke_data.json")
    poke_data = json.load(json_file)
    insert_data(poke_data)
