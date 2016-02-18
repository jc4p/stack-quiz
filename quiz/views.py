from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from django.views.decorators.cache import cache_page

import os
import requests
import json
import logging


def health_check(request):
    return HttpResponse('{"Status": "OK"}', content_type='application/json')


def home(request):
    return render_to_response("home.html", {}, context_instance=RequestContext(request))


def camp(request):
    return render_to_response("home.html", {"camp_only": True}, context_instance=RequestContext(request))


def quiz(request):
    return render_to_response("quiz.html", {}, context_instance=RequestContext(request))


@cache_page(24 * 60 * 60)
def get_employees(request):
    """
    Retrieves a JSON list of employees fro the server and caches it for 1 day
    """

    BAMBOO_URL = "https://api.bamboohr.com/api/gateway.php/stackexchange/v1/reports/1931?format=json"

    try:
        keyfile_path = os.path.join(os.path.sep, 'opt', 'quiz', 'quiz', 'key.json')
        with open(keyfile_path, 'r') as f:
            creds = json.loads(f.read())
        BAMBOO_API_KEY = creds['BAMBOO_API_KEY']
        logging.info("Received bamboo key from key.json file.")
    except Exception:
        logging.error("Could not find keyfile, so trying the environment variable instead.")
        BAMBOO_API_KEY = os.environ.get('BAMBOO_API_KEY')

    if not BAMBOO_API_KEY:
        raise ValueError("No Bamboo API Key")

    bamboo_auth = (BAMBOO_API_KEY, "x")

    page = requests.get(BAMBOO_URL, auth=bamboo_auth)
    emps = page.json()['employees']
    camp_only = request.GET.get("camp", "false") == "true"
    employees = []
    for emp in emps:
        # Required fields
        name = emp['nickname'] if emp.get('nickname') else emp['firstName']
        name += " " + emp['lastName']
        camp = emp['customCompanyEvents'] and '2015 Product Meetup' in emp['customCompanyEvents']
        employee = {'name': name, 'photo': emp['photoUrl'], 'position': emp['jobTitle'],
                    'location': emp['location'], 'gender': emp['gender'], 'department': emp['division']}
        # Trim gender to M/F
        if employee['gender']:
            employee['gender'] = employee['gender'][0]
        if camp_only and not camp:
                continue
        # I don't want people without pictures or people without a location set
        if "placeholder" not in employee['photo'] and employee['location']:
            employees.append(employee)

    return HttpResponse(json.dumps(employees), content_type='application/json')
