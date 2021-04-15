from django.shortcuts import render
import requests
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import datetime

# Create your views here.


# API for index page, show issue list
def index(request):
    # Obtain issue list
    url = "https://api.github.com/repos/walmartlabs/thorax/issues"
    r = requests.get(url)
    data = r.json()
    paginator = Paginator(data, 10)
    page = request.GET.get('page')
    show = paginator.get_page(page)
    return render(request, 'index.html', {'data': show})


# API for detail page, show issue detail and comments
def detail(request):
    # Obtain issue detail data
    number = request.GET['number']
    url = "https://api.github.com/repos/walmartlabs/thorax/issues/" + number
    r = requests.get(url)
    data = r.json()

    # Obtain comments data
    url = url + "/comments"
    comments = requests.get(url).json()

    # Format UTC to local time and change the style
    utc_format = "%Y-%m-%dT%H:%M:%SZ"
    utc_time = datetime.datetime.strptime(data['created_at'], utc_format)
    data['created_at'] = utc_time - datetime.timedelta(hours=8)
    utc_time = datetime.datetime.strptime(data['updated_at'], utc_format)
    data['updated_at'] = utc_time - datetime.timedelta(hours=8)

    return render(request, 'detail.html', {'data': data, 'comments': comments})
