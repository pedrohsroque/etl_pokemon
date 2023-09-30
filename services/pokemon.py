"""
This module intects with pokeapi
"""
import json

import requests


class ETLPokemon:
    """
    Class to interect with pokeapi
    """
    def __init__(self) -> None:
        self.BASE_URL = "https://pokeapi.co/api/v2/"
        self.ALLOWED_OBJECTS = [
            "berry",
            "berry-firmness",
            "berry-flavor",
            "contest-type",
            "contest-effect",
            "super-contest-effect",
            "encounter-method",
            "encounter-condition",
            "encounter-condition-value",
            "evolution-chain",
            "evolution-trigger",
            "generation",
            "pokedex",
            "version",
            "version-group",
            "item-attribute",
            "item-category",
            "item-fling-effect",
            "item-pocket",
            "location",
            "location-area",
            "pal-park-area",
            "region",
            "machine",
            "move",
            "move-ailment",
            "move-battle-style",
            "move-category",
            "move-damage-class",
            "move-learn-method",
            "move-target",
            "ability",
            "characteristic",
            "egg-group",
            "gender",
            "growth-rate",
            "nature",
            "pokeathlon-stat",
            "pokemon",
            "pokemon-color",
            "pokemon-form",
            "pokemon-habitat",
            "pokemon-shape",
            "pokemon-species",
            # "pokemon-stat",
            # "pokemon-type",
        ]
        self.LIMIT = 100

    def validate_object_name(self, object_name: str):
        """
        Check if the object name is available
        """
        if object_name not in self.ALLOWED_OBJECTS:
            raise ValueError(f"Object {object_name} not available")
        return object_name

    def _get(self, url, query):
        return requests.get(url, query, timeout=100)

    def get_elements(self, object_name: str, query: dict=None):
        """
        Get one page of elements for the given element.
        """
        object_name = self.validate_object_name(object_name)
        url = f"{self.BASE_URL}{object_name}/"
        r = self._get(url=url, query=query)
        if r.status_code != 200:
            print(r.text)
            raise RuntimeError("Error during request")
        return r.json()

    def get_all_elements(self, object_name: str):
        """
        Get all elements for a given object
        """
        # initial parameters
        idx = 0
        next_url = True
        query = {
            "offset": 0,
            "limit": self.LIMIT,
        }
        # resolving pagination
        while next_url:
            json_data = self.get_elements(object_name, query)
            self.save_data(json_data, object_name, idx)
            idx += 1
            next_url = json_data["next"]
            if not next_url:
                return
            params_dict = self.extract_params_from_url_query(url=next_url)
            query.update({"offset": params_dict["offset"]})

    def extract_params_from_url_query(self, url: str):
        """
        Extract the params from a url_query:\n
        e.g.:\n
        https://www.google.com/?search=test&limit=100 -> {"search": "test","limit": "100"}
        """
        params_dict = {}
        params_list = url.split("?")[1].split("&")
        for item in params_list:
            params_dict.update({item.split("=")[0]: item.split("=")[1]})
        return params_dict

    def save_data(self, response: str, object_name: str, idx: int):
        """
        Save json data localy
        """
        with open(f"data/{object_name}_{idx}.json", "w", encoding="UTF-8") as f:
            f.writelines(json.dumps(response))


if __name__ == "__main__":
    etlpokemon = ETLPokemon()
    for object_nm in etlpokemon.ALLOWED_OBJECTS[-2:]:
        print(f"Getting data for {object_nm}")
        etlpokemon.get_all_elements(object_name=object_nm)
