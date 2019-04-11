from mixer.backend.django import mixer
from importCsv.models import Hotel, City, Url
import pytest


@pytest.mark.django_db
class TestModels:
    """tests the city,hotel and url models and their ___str__ methods"""

    def test_city(self):
        city_name = "test city"
        city = mixer.blend(City, name=city_name)
        assert str(city) == city_name

    def test_hotel(self):
        hotel_name = "test hotel"
        hotel = mixer.blend(Hotel, name=hotel_name)
        assert str(hotel) == hotel_name

    def test_url(self):
        url_url = "test url"
        test_url = mixer.blend(Url, url=url_url, title="city")
        assert str(test_url) == "city " + url_url
