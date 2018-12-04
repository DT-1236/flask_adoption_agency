import requests
from secrets import PET_API_KEY


class PetFinder():
    """Get pets."""

    @classmethod
    def get_random(self):
        """Get random pet."""

        resp = requests.get(
            "http://api.petfinder.com/pet.getRandom",
            params={
                "format": "json",
                "key": PET_API_KEY,
                "output": "basic"
            })

        json = resp.json()

        return {
            "name":
            json.get('petfinder').get('pet').get('name').get('$t'),
            "age":
            json.get('petfinder').get('pet').get('age').get('$t'),
            "photo_url":
            json.get('petfinder').get('pet').get('media').get(
                'photos', {}).get('photo', [{}, {}, {}])[2].get('$t')
        }
