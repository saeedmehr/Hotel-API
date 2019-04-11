from django.urls import reverse, resolve


class TestUrls:
    """tests whether all important urls works fine"""

    def test_main_url(self):
        path = reverse('main')
        assert resolve(path).view_name == 'main'

    def test_search_url(self):
        path = reverse('search')
        assert resolve(path).view_name == 'search'

    def test_logout_url(self):
        path = reverse('logout')
        assert resolve(path).view_name == 'logout'

    def test_setting_csv_url(self):
        path = reverse('setting-csv')
        assert resolve(path).view_name == 'setting-csv'

    def test_import_csv_url(self):
        path = reverse('import-csv')
        assert resolve(path).view_name == 'import-csv'
