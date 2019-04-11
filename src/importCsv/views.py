from django.contrib.auth import logout
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from io import TextIOWrapper, StringIO
from importCsv.forms import uploadForm, upload_url, searchForm
from django.views.decorators.csrf import ensure_csrf_cookie


@login_required
@ensure_csrf_cookie
def csv_import(request):
    """
    Cvs importing view for local file
    :param request: incoming request
    :return: sends local file uploading page
    """
    form = uploadForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            errors = handle_uploaded_file(TextIOWrapper(request.FILES['csv_file'], encoding="utf-8"),
                                          request.POST["title"])
            if len(errors) == 0:
                messages.success(request, "Successfully Uploaded!")
            else:
                for err in errors:
                    messages.add_message(request, messages.WARNING, "can not import " + ' '.join(err))
            return render(request, 'post_form.html')
    return render(request, 'post_form.html', {'form': form})


def handle_uploaded_file(file, title):
    """
    Receives file and its type (city or hotel) and updates model base on it
    :param file: file to read data from
    :param title: the type of file (city or hotel)
    :return: a list of encountered errors while inserting data
    """
    import csv
    from .models import City, Hotel
    errors = []
    csv_data = csv.reader(file, delimiter=';')
    if title == "city":
        for row in csv_data:
            try:
                if row[0] != "":
                    rec = City.objects.get(abbrev=row[0])
                    errors.append(row)
                continue
            except:
                if len(row) == 2:
                    rec = City(abbrev=row[0], name=row[1])
                    rec.save()
    elif title == "hotel":
        for row in csv_data:
            try:
                if row[1] != "":
                    rec = Hotel.objects.get(data=row[1])
                continue
            except:
                if len(row) == 3:
                    try:
                        hasCity = City.objects.get(abbrev=row[0])
                        rec = Hotel(city=hasCity, data=row[1], name=row[2])
                        rec.save()
                    except:
                        errors.append(row)
                        continue
    return errors


def logoutUser(request):
    """
    Logout the current user
    :param request: incoming request
    :return: redirects to home page
    """
    logout(request)
    messages.add_message(request, messages.SUCCESS, "Successfully logged out")
    return HttpResponseRedirect('/')


def index(request):
    """
    Shows the index page
    :param request:incoming request
    :return: sends index page
    """
    return render(request, 'main.html')


@login_required
@ensure_csrf_cookie
def csv_setting(request):
    """
    Csv importing view for cloud-based files
    :param request: incoming request
    :return: sends remote file downloading page
    """
    from .models import Url
    form = upload_url(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            if not request.POST["url"].startswith("http://"):
                request.POST = request.POST.copy()
                request.POST["url"] = "http://" + request.POST["url"]
            file = get_file(request)
            if len(file) != 0 and "save" in request.POST.keys() and request.POST["save"] == "on":
                Url.objects.get_or_create(url=request.POST["url"], defaults={'title': request.POST["title"],
                                                                             'username': request.POST["username"],
                                                                             'password': request.POST["password"]})
            elif len(file) == 0:
                return render(request, 'settings.html')
            errors = handle_uploaded_file(StringIO(file), request.POST["title"])
            if len(errors) == 0:
                messages.success(request, "Successfully Uploaded!")
            else:
                for err in errors:
                    messages.add_message(request, messages.WARNING, "can not import " + ' '.join(err))
            return render(request, 'settings.html')
    return render(request, 'settings.html', {'form': form})


def get_file(request):
    """
    Gets file from remote address
    :param request: incoming request which has 'url', 'username' and 'password'
    :return: data which is located at the remote address or an empty string in case of error
    """
    import requests
    try:
        data = requests.get(request.POST["url"], auth=(request.POST["username"], request.POST["password"]))
        return data.text
    except:
        messages.add_message(request, messages.WARNING, "Received an error while downloading file")
        return ""


def search(request):
    """
    Search hotels based on the imported cities
    :param request: incoming request
    :return: sends search page with/without results
    """
    from .models import City, Hotel
    cities = City.objects.all()
    if cities.model.DoesNotExist:
        form = searchForm(request.POST or None, cities= [])
    else:
        form = searchForm(request.POST or None, cities=cities)
    if request.method == 'POST':
        if form.is_valid():
            hotels = []
            checkedCity = []
            for c in request.POST:
                if c == 'csrfmiddlewaretoken':
                    continue
                city = City.objects.get(abbrev=c)
                checkedCity.append(city.abbrev)
                hotels.extend(Hotel.objects.filter(city=city))
            return render(request, 'search.html', {'cities': cities, 'hotels': hotels, 'checkedCity': checkedCity})
    else:
        return render(request, 'search.html', {'form': form, 'cities': cities})
