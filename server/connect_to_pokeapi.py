import requests


def get_from_server(my_url):
    return requests.get(url=my_url, verify=False)


def get_types(poke_name):
    url = f'https://pokeapi.co/api/v2/type/?name={poke_name}'
    types = get_from_server(url).json()["results"]
    return [i["name"] for i in types]


