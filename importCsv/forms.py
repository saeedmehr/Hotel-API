from django import forms


class uploadForm(forms.Form):
    """Upload form for uploading local files"""
    title = forms.CharField(max_length=50)
    csv_file = forms.FileField(required=True, label='upload csv file')


class upload_url(forms.Form):
    """Url form for getting files form could"""
    title = forms.CharField(max_length=50)
    url = forms.CharField(max_length=1000)
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)
    save = forms.BooleanField(required=False)


class searchForm(forms.Form):
    """Search form for searching hotels based on available cities"""

    def __init__(self, *args, **kwargs):
        '''
        overwrites default __init__ function
        :param kwargs: cities list passed by the key of 'cities'
        '''
        cities = kwargs.pop('cities', None)
        super().__init__(*args, **kwargs)
        for i, city in enumerate(cities):
            self.fields['%s' % city.abbrev] = forms.CharField(label=city, required=False)
