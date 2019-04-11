from django.core.management.base import BaseCommand, CommandError

from importCsv.models import Url, City, Hotel


class Command(BaseCommand):
    """A custom manager command for daily importing of data"""

    def handle(self, *args, **options):
        """
        Imports data from saved urls in database
        :return: prints error on stdout if there is any
        """
        from io import StringIO
        from importCsv.views import handle_uploaded_file
        urls = Url.objects.all()
        if len(urls) == 0:
            self.stdout.write('No url in database', ending='\r\n')
        for url in urls:
            file = self.get_file(url)
            if len(file) == 0:
                return
            errors = handle_uploaded_file(StringIO(file), url.title)
            for err in errors:
                self.stdout.write(str(err), ending='\r\n')

    def get_file(self, url):
        """
        Retrieves file from cloud
        :param url: given url to receive file from
        :return: data which is located at the remote address or an empty string in case of error
        """
        import requests
        try:
            data = requests.get(url.url, auth=(url.username, url.password))
            return data.text
        except:
            return ""
