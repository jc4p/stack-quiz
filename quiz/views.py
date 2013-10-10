from django.http        import HttpResponse
from django.shortcuts   import render_to_response
from django.template    import RequestContext

from django.views.decorators.cache import cache_page

import json


def home(request):
    return render_to_response("home.html", {}, context_instance=RequestContext(request))


@cache_page(24 * 60 * 60)
def get_employees(request):
    """
    Retrieves a JSON list of employees fro the server and caches it for 1 day
    """
    from bs4 import BeautifulSoup
    import requests

    page = requests.get("http://stackexchange.com/about/team")
    soup = BeautifulSoup(page.content)
    containers = soup.find_all("div", class_="employee-photo-container")

    employees = [_get_from_container(x) for x in containers]

    return HttpResponse(json.dumps(employees), content_type='application/json')


def _get_from_container(container):
    name = container.find("div", "employee-name").string
    photo = container.find("img", "employee-photo")['src']
    position = container.find("div", "employee-position").string
    location = container.find("div", "employee-location").string
    return {"name": name, "photo": photo, "position": position, "location": location}
