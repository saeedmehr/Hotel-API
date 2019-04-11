from importCsv.models import Url
from io import StringIO
from django.core.management import call_command
import pytest


@pytest.mark.django_db
class TestCommand:
    """tests the 'checkurl' custom manager command"""

    def test_check_url(self):
        """
        Checks if it can import the sample dataset form provided urls
        """
        out = StringIO()
        testurl = Url(title="city", url="http://rachel.maykinmedia.nl/djangocase/city.csv", username="python-demo",
                      password="claw30_bumps")
        testurl.save()
        testurl = Url(title="hotel", url="http://rachel.maykinmedia.nl/djangocase/hotel.csv", username="python-demo",
                      password="claw30_bumps")
        testurl.save()
        call_command('checkurl', stdout=out)
        assert out.getvalue() == ""

    def test_check_url_noUrl(self):
        """
        Checks if receives an error when there is no url in database
        """
        out = StringIO()
        call_command('checkurl', stdout=out)
        assert 'No url in database' in out.getvalue()
