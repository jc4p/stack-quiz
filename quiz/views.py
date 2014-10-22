from django.http        import HttpResponse
from django.shortcuts   import render_to_response
from django.template    import RequestContext

from django.views.decorators.cache import cache_page

import os
import requests
import json


def home(request):
    return render_to_response("home.html", {}, context_instance=RequestContext(request))


def quiz(request):
    return render_to_response("quiz.html", {}, context_instance=RequestContext(request))


@cache_page(24 * 60 * 60)
def get_employees(request):
    """
    Retrieves a JSON list of employees fro the server and caches it for 1 day
    """

    BAMBOO_URL = "https://api.bamboohr.com/api/gateway.php/stackexchange/v1/reports/1931?format=json"
    BAMBOO_API_KEY = os.environ.get("BAMBOO_API_KEY", None)
    if not BAMBOO_API_KEY:
        raise ValueError("No Bamboo API Key")

    bamboo_auth = (BAMBOO_API_KEY, "x")

    page = requests.get(BAMBOO_URL, auth=bamboo_auth)
    emps = page.json()['employees']

    employees = []
    for emp in emps:
        # Required fields
        employee = {'name': emp['fullName1'], 'photo': emp['photoUrl'], 'position': emp['jobTitle'],
                    'location': emp['location'], 'gender': emp['gender'], 'department': emp['division']}
        # If they have a nickname, add it in.
        if emp['nickname']:
            employee['nickname'] = emp['nickname']
        # Trim gender to M/F
        if employee['gender']:
            employee['gender'] = employee['gender'][0]
        # I don't want people without pictures.
        if not "placeholder" in employee['photo']:
            employees.append(employee)

    return HttpResponse(json.dumps(employees), content_type='application/json')
