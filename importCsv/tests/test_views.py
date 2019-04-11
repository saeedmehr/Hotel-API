import pytest
from django.test import RequestFactory
from django.urls import reverse
from mixer.backend.django import mixer
from django.contrib.auth.models import User, AnonymousUser
from importCsv.views import csv_import, index, csv_setting
from django.test.client import Client


@pytest.mark.django_db
class TestView:
    """tests the provided views"""

    def test_csv_import_auth(self):
        """
        Checks only authenticated users can see the page
        """
        path = reverse("import-csv")
        request = RequestFactory().get(path)
        request.user = mixer.blend(User)
        response = csv_import(request)
        assert response.status_code == 200

    def test_csv_import_unauth(self):
        """
        Checks unauthenticated users can not see the page
        """
        path = reverse("import-csv")
        request = RequestFactory().get(path)
        request.user = AnonymousUser()
        response = csv_import(request)
        assert response.status_code == 302

    def test_setting_csv_auth(self):
        """
        Checks only authenticated users can see the page
        """
        path = reverse("setting-csv")
        request = RequestFactory().get(path)
        request.user = mixer.blend(User)
        response = csv_setting(request)
        assert response.status_code == 200

    def test_setting_csv_unauth(self):
        """
        Checks unauthenticated users can not see the page
        """
        path = reverse("setting-csv")
        request = RequestFactory().get(path)
        request.user = AnonymousUser()
        response = csv_setting(request)
        assert response.status_code == 302

    def test_csv_import_city(self):
        """
        Tests the import from local file for cities works fine
        """
        from django.contrib.messages import get_messages
        path = reverse("import-csv")
        user = mixer.blend(User, is_staff=True, is_superuser=True)
        file = open("city.csv")
        client = Client()
        client.force_login(user)
        r = client.post(path, {"title": "city", "csv_file": file})
        messages = list(get_messages(r.wsgi_request))
        assert r.status_code == 200
        assert len(messages) == 1
        assert str(messages[0]) == "Successfully Uploaded!"

    def test_csv_import_hotel_success(self):
        """
        Tests the import from local file for hotels works fine
        """
        from django.contrib.messages import get_messages
        path = reverse("import-csv")
        user = mixer.blend(User, is_staff=True, is_superuser=True)
        file = open("city.csv")
        client = Client()
        client.force_login(user)
        client.post(path, {"title": "city", "csv_file": file})
        file = open("hotel.csv")
        r = client.post(path, {"title": "hotel", "csv_file": file})
        messages = list(get_messages(r.wsgi_request))
        assert r.status_code == 200
        assert len(messages) == 1
        assert str(messages[0]) == "Successfully Uploaded!"

    def test_csv_import_hotel_fail(self):
        """
        Tests hotels which their cities aren't in database can not get imported form local file
        """
        from django.contrib.messages import get_messages
        path = reverse("import-csv")
        user = mixer.blend(User, is_staff=True, is_superuser=True)
        client = Client()
        client.force_login(user)
        file = open("hotel.csv")
        r = client.post(path, {"title": "hotel", "csv_file": file})
        messages = list(get_messages(r.wsgi_request))
        assert r.status_code == 200
        assert len(messages) >= 1
        for message in messages:
            assert "can not import" in str(message)

    def test_setting_csv_city(self):
        """
        Tests the import from remote file for cities works fine
        """
        from django.contrib.messages import get_messages
        path = reverse("setting-csv")
        user = mixer.blend(User, is_staff=True, is_superuser=True)
        client = Client()
        client.force_login(user)
        r = client.post(path, {"title": "city", "url": "http://rachel.maykinmedia.nl/djangocase/city.csv",
                               "username": "python-demo", "password": "claw30_bumps", "save": "on"})
        messages = list(get_messages(r.wsgi_request))
        assert r.status_code == 200
        assert len(messages) == 1
        assert str(messages[0]) == "Successfully Uploaded!"

    def test_setting_csv_hotel_success(self):
        """
        Tests the import from remote file for hotels works fine
        """
        from django.contrib.messages import get_messages
        path = reverse("setting-csv")
        user = mixer.blend(User, is_staff=True, is_superuser=True)
        client = Client()
        client.force_login(user)
        client.post(path, {"title": "city", "url": "http://rachel.maykinmedia.nl/djangocase/city.csv",
                           "username": "python-demo", "password": "claw30_bumps", "save": "on"})
        r = client.post(path, {"title": "hotel", "url": "http://rachel.maykinmedia.nl/djangocase/hotel.csv",
                               "username": "python-demo", "password": "claw30_bumps", "save": "on"})
        messages = list(get_messages(r.wsgi_request))
        assert r.status_code == 200
        assert len(messages) == 1
        assert str(messages[0]) == "Successfully Uploaded!"

    def test_setting_csv_hotel_fail(self):
        """
        Tests hotels which their cities aren't in database can not get imported form remote file
        """
        from django.contrib.messages import get_messages
        path = reverse("setting-csv")
        user = mixer.blend(User, is_staff=True, is_superuser=True)
        client = Client()
        client.force_login(user)
        r = client.post(path, {"title": "hotel", "url": "http://rachel.maykinmedia.nl/djangocase/hotel.csv",
                               "username": "python-demo", "password": "claw30_bumps", "save": "on"})
        messages = list(get_messages(r.wsgi_request))
        assert r.status_code == 200
        assert len(messages) > 1

    def test_search(self):
        """
        Checks whether the search functionality works fine
        """
        from importCsv.models import City, Hotel
        path = reverse("search")
        user = mixer.blend(User, is_staff=True, is_superuser=True)
        city = mixer.blend(City, abbrev="tes", name="test")
        mixer.blend(Hotel, city=city, data="testData", name="test hotel")
        client = Client()
        client.force_login(user)
        r = client.post(path, {"tes": "on"})
        assert r.status_code == 200
        assert r.content.find(b'test hotel')

    def test_logout(self):
        """
        Validates the functionality of logout
        """
        from django.contrib.messages import get_messages
        path = reverse("logout")
        user = mixer.blend(User, is_staff=True, is_superuser=True)
        client = Client()
        client.force_login(user)
        client.post('/admin/')
        r = client.post(path)
        messages = list(get_messages(r.wsgi_request))
        assert str(messages[0]) == "Successfully logged out"

    def test_main(self):
        """
        Checks the main page is Ok
        """
        path = reverse("main")
        request = RequestFactory().get(path)
        response = index(request)
        assert response.status_code == 200

    def test_get_file_fail(self):
        """
        Checks getting file from remote url works fine
        """
        from django.contrib.messages import get_messages
        path = reverse("setting-csv")
        user = mixer.blend(User, is_staff=True, is_superuser=True)
        client = Client()
        client.force_login(user)
        r = client.post(path, {"title": "hotel", "url": "http://rachel.wrongurltofetchdata.nl/djangocase/hotel.csv",
                               "username": "py", "password": "30_bumps", "save": "on"})
        messages = list(get_messages(r.wsgi_request))
        assert r.status_code == 200
        assert len(messages) == 1
        assert "Received an error" in str(messages[0])
