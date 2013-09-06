from django.http        import HttpResponse
from django.shortcuts   import render_to_response
from django.template    import RequestContext

import json


def home(request):
    return render_to_response("home.html", {}, context_instance=RequestContext(request))

def get_employees(request):
    """So... this used to be get_employees_from_site() and used memcached to only ping SE.com once every 24 hours,
    but one of the first recommended changes was to discriminate possbile guesses by gender, so I had to end up
    doing it like this."""

    employees_with_gender = [
        {"gender": "M", "location": "New York, NY", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Joel Spolsky.jpg", "position": "Co-founder and CEO", "name": "Joel Spolsky"}, 
        {"gender": "M", "location": "El Cerrito, CA", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Jeff Atwood.jpg", "position": "Co-founder", "name": "Jeff Atwood"},
        {"gender": "M", "location": "New York, NY", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Michael Pryor.jpg", "position": "CFO", "name": "Michael Pryor"},
        {"gender": "M", "location": "New York, NY", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Jarrod Dixon.jpg", "position": "Developer", "name": "Jarrod Dixon"},
        {"gender": "M", "location": "Corvallis, OR", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Geoff Dalgas.jpg", "position": "Developer", "name": "Geoff Dalgas"},
        {"gender": "M", "location": "New York, NY", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/David Fullerton.jpg", "position": "VP of Engineering", "name": "David Fullerton"},
        {"gender": "M", "location": "New York, NY", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Korneel Bouman.jpg", "position": "Duct Tape", "name": "Korneel Bouman"},
        {"gender": "M", "location": "Palm Bay, FL", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Robert Cartaino.jpg", "position": "Director of Community Development", "name": "Robert Cartaino"},
        {"gender": "F", "location": "New York, NY", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Amanda Kaplowitz.jpg", "position": "Sales", "name": "Amanda Kaplowitz"},
        {"gender": "M", "location": "Berlin, Germany", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Ben Dumke-von der Ehe.jpg", "position": "Developer", "name": "Ben Dumke-von der Ehe"},
        {"gender": "M", "location": "New York, NY", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Kevin Montrose.jpg", "position": "Developer", "name": "Kevin Montrose"},
        {"gender": "M", "location": "Cinderford, UK", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Marc Gravell.jpg", "position": "Developer", "name": "Marc Gravell"},
        {"gender": "M", "location": "New York, NY", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Matt Sherman.jpg", "position": "Developer", "name": "Matt Sherman"},
        {"gender": "M", "location": "New York, NY", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Danny Miller.jpg", "position": "Sales", "name": "Danny Miller"}, 
        {"gender": "M", "location": "New York, NY", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Jason Punyon.jpg", "position": "Developer", "name": "Jason Punyon"}, 
        {"gender": "M", "location": "Denver, CO", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Nick Cardillo.jpg", "position": "Regional Sales Manager", "name": "Nick Cardillo"}, 
        {"gender": "M", "location": "Hollywood, FL", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Kyle Brandt.jpg", "position": "Director of Site Reliability", "name": "Kyle Brandt"}, 
        {"gender": "M", "location": "Raleigh, NC", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Jin Yang.jpg", "position": "Creative Director", "name": "Jin Yang"}, 
        {"gender": "M", "location": "New York, NY", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Jeff Szczepanski.jpg", "position": "VP of Products", "name": "Jeff Szczepanski"}, 
        {"gender": "F", "location": "New York, NY", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Alison Sperling.jpg", "position": "Director of Marketing", "name": "Alison Sperling"}, 
        {"gender": "M", "location": "New York, NY", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/George Beech.jpg", "position": "Site Reliability Engineer", "name": "George Beech"}, 
        {"gender": "M", "location": "Winston-Salem, NC", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Nick Craver.jpg", "position": "Developer", "name": "Nick Craver"}, 
        {"gender": "M", "location": "New York, NY", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Nick Larsen.jpg", "position": "Developer", "name": "Nick Larsen"}, 
        {"gender": "F", "location": "New York, NY", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Amanda Zompetti.jpg", "position": "Director of Office Operations", "name": "Amanda Zompetti"}, 
        {"gender": "M", "location": "New York, NY", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Greg Drinkwater.jpg", "position": "Sales", "name": "Greg Drinkwater"}, 
        {"gender": "M", "location": "New York, NY", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Alex Miller.jpg", "position": "VP of Operations", "name": "Alex Miller"}, 
        {"gender": "M", "location": "New York, NY", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Guy Zerega.jpg", "position": "National Sales Manager", "name": "Guy Zerega"}, 
        {"gender": "F", "location": "New York, NY", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Abby Miller.jpg", "position": "Community Growth Specialist", "name": "Abby Miller"}, 
        {"gender": "F", "location": "New York, NY", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Laura Dobrzynski.jpg", "position": "Associate Product Manager", "name": "Laura Dobrzynski"}, 
        {"gender": "M", "location": "New York, NY", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Sam Brand.jpg", "position": "Community Evangelist", "name": "Sam Brand"}, 
        {"gender": "M", "location": "Southwick, MA", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Chris Jaeger.jpg", "position": "Community Manager", "name": "Chris Jaeger"}, 
        {"gender": "M", "location": "London, UK", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Dimitar Stanimiroff.jpg", "position": "Regional Sales Director, Europe & Australia", "name": "Dimitar Stanimiroff"}, 
        {"gender": "M", "location": "New York, NY", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Demis Bellot.jpg", "position": "Developer", "name": "Demis Bellot"}, 
        {"gender": "F", "location": "New York, NY", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Rachel Boyman.jpg", "position": "Sales", "name": "Rachel Boyman"}, 
        {"gender": "M", "location": "New York, NY", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Peter Grace.jpg", "position": "Director of IT", "name": "Peter Grace"}, 
        {"gender": "M", "location": "New York, NY", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Charles Bernoskie.jpg", "position": "Sales", "name": "Charles Bernoskie"}, 
        {"gender": "M", "location": "Colorado", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Josh Heyer.jpg", "position": "Community Manager", "name": "Josh Heyer"}, 
        {"gender": "M", "location": "New York, NY", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Steve Feldman.jpg", "position": "Ad Operations Campaign Manager", "name": "Steve Feldman"}, 
        {"gender": "F", "location": "New York, NY", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Bethany Marzewski.jpg", "position": "Marketing Coordinator", "name": "Bethany Marzewski"}, 
        {"gender": "M", "location": "New York, NY", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Dammand Cherry.jpg", "position": "Sales", "name": "Dammand Cherry"}, 
        {"gender": "M", "location": "London, UK", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Ben Kiziltug.jpg", "position": "Sales", "name": "Ben Kiziltug"}, 
        {"gender": "M", "location": "New York, NY", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Jay Greenbaum.jpg", "position": "Sales", "name": "Jay Greenbaum"}, 
        {"gender": "M", "location": "New York, NY", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Matt Jibson.jpg", "position": "Developer", "name": "Matt Jibson"}, 
        {"gender": "M", "location": "London, UK", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Stefan Schwarzgruber.jpg", "position": "Sales", "name": "Stefan Schwarzgruber"}, 
        {"gender": "M", "location": "New York, NY", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Matt Napolitano.jpg", "position": "Sales", "name": "Matt Napolitano"}, 
        {"gender": "M", "location": "New York, NY", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Will Cole.jpg", "position": "Product Manager", "name": "Will Cole"}, 
        {"gender": "F", "location": "New York, NY", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Anna Lear.jpg", "position": "Community Manager", "name": "Anna Lear"}, 
        {"gender": "M", "location": "New York, NY", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Sean Bave.jpg", "position": "Marketing Manager, Inbound", "name": "Sean Bave"}, 
        {"gender": "F", "location": "New York, NY", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Robyn Wertman.jpg", "position": "Finance Manager", "name": "Robyn Wertman"}, 
        {"gender": "M", "location": "New York, NY", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Bart Silverstrim.jpg", "position": "Systems Administrator", "name": "Bart Silverstrim"}, 
        {"gender": "M", "location": "New York, NY", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Robert Brand.jpg", "position": "Sales", "name": "Robert Brand"}, 
        {"gender": "M", "location": "New York, NY", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Jay Hanlon.jpg", "position": "VP of Community Growth", "name": "Jay Hanlon"}, 
        {"gender": "F", "location": "Denver, CO", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Erin Gray.jpg", "position": "Sales", "name": "Erin Gray"}, 
        {"gender": "M", "location": "Denver, CO", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Joseph Sondag.jpg", "position": "Sales", "name": "Joseph Sondag"}, 
        {"gender": "M", "location": "Denver, CO", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Maxwell Applebaum.jpg", "position": "Sales", "name": "Maxwell Applebaum"}, 
        {"gender": "M", "location": "Denver, CO", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Jordan Conner.jpg", "position": "Sales", "name": "Jordan Conner"}, 
        {"gender": "F", "location": "Denver, CO", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Diandra Partridge.jpg", "position": "Office Manager", "name": "Diandra Partridge"}, 
        {"gender": "M", "location": "New York, NY", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Adam DeLanoy.jpg", "position": "Sales", "name": "Adam DeLanoy"}, 
        {"gender": "F", "location": "New York, NY", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Casey Ashenhurst.jpg", "position": "Office Manager", "name": "Casey Ashenhurst"}, 
        {"gender": "M", "location": "Denver, CO", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Robert Brooks.jpg", "position": "Sales", "name": "Robert Brooks"}, 
        {"gender": "F", "location": "New York, NY", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Maura Bradley.jpg", "position": "Sales", "name": "Maura Bradley"}, 
        {"gender": "M", "location": "Denver, CO", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Peter Schnelle.jpg", "position": "Sales", "name": "Peter Schnelle"}, 
        {"gender": "M", "location": "London, UK", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Chris Martin.jpg", "position": "Sales", "name": "Chris Martin"}, 
        {"gender": "M", "location": "New York, NY", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Joe Humphries.jpg", "position": "Recruiter", "name": "Joe Humphries"}, 
        {"gender": "M", "location": "Nashville, TN", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Jeremy Tunnell.jpg", "position": "Product Manager", "name": "Jeremy Tunnell"}, 
        {"gender": "F", "location": "New York, NY", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Natalie Eisen.jpg", "position": "Sales", "name": "Natalie Eisen"}, 
        {"gender": "M", "location": "Oconomowoc, WI", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Steven Murawski.jpg", "position": "Site Reliability Engineer", "name": "Steven Murawski"}, 
        {"gender": "F", "location": "Denver, CO", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Shefali Shah.jpg", "position": "Sales", "name": "Shefali Shah"}, 
        {"gender": "M", "location": "New York, NY", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Max Horstmann.jpg", "position": "Developer", "name": "Max Horstmann"}, 
        {"gender": "M", "location": "London, UK", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Oded Coster.jpg", "position": "Developer", "name": "Oded Coster"}, 
        {"gender": "F", "location": "New York, NY", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Wendy Paler.jpg", "position": "Sales", "name": "Wendy Paler"}, 
        {"gender": "F", "location": "London, UK", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Valentina Perez.jpg", "position": "Office Manager", "name": "Valentina Perez"}, 
        {"gender": "F", "location": "London, UK", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Shikha Malhotra.jpg", "position": "Sales", "name": "Shikha Malhotra"}, 
        {"gender": "M", "location": "New York, NY", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Pieter DePree.jpg", "position": "Recruiter", "name": "Pieter DePree"}, 
        {"gender": "M", "location": "London, UK", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Marco Cecconi.jpg", "position": "Developer", "name": "Marco Cecconi"}, 
        {"gender": "M", "location": "Denver, CO", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Bryan Ross.jpg", "position": "Developer", "name": "Bryan Ross"}, 
        {"gender": "F", "location": "New York, NY", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Jessica Brady.jpg", "position": "Sales", "name": "Jessica Brady"}, 
        {"gender": "M", "location": "New York, NY", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Derek Still.jpg", "position": "Sales", "name": "Derek Still"}, 
        {"gender": "M", "location": "London, UK", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Pawel Michalak.jpg", "position": "Sales", "name": "Pawel Michalak"}, 
        {"gender": "M", "location": "Denver, CO", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Jim Egan.jpg", "position": "Sales", "name": "Jim Egan"}, 
        {"gender": "M", "location": "London, UK", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Todd Jenkins.jpg", "position": "Sales", "name": "Todd Jenkins"}, 
        {"gender": "M", "location": "London, UK", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Paul Frey.jpg", "position": "Sales", "name": "Paul Frey"}, 
        {"gender": "M", "location": "Greenville, TX", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Ben Collins.jpg", "position": "Developer", "name": "Ben Collins"}, 
        {"gender": "M", "location": "New York, NY", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Michael Dillon.jpg", "position": "Sales", "name": "Michael Dillon"}, 
        {"gender": "M", "location": "New York, NY", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Matthew Charette.jpg", "position": "Sales", "name": "Matthew Charette"}, 
        {"gender": "F", "location": "New York, NY", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Allie Schwartz.jpg", "position": "Sales", "name": "Allie Schwartz"}, 
        {"gender": "M", "location": "New York, NY", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Tom Limoncelli.jpg", "position": "System Administrator", "name": "Tom Limoncelli"}, 
        {"gender": "M", "location": "Mandaluyong, Philippines", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Tim Post.jpg", "position": "Community Manager", "name": "Tim Post"}, 
        {"gender": "F", "location": "London, UK", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Sara Rayman.jpg", "position": "Sales", "name": "Sara Rayman"}, 
        {"gender": "M", "location": "London, UK", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/David Lislet.jpg", "position": "Sales", "name": "David Lislet"}, 
        {"gender": "F", "location": "New York, NY", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Monika Pradhan.jpg", "position": "Sales", "name": "Monika Pradhan"}, 
        {"gender": "M", "location": "New York, NY", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Jonathan Zizzo.jpg", "position": "Sales", "name": "Jonathan Zizzo"}, 
        {"gender": "M", "location": "Denver, CO", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Max Holley.jpg", "position": "Sales", "name": "Max Holley"}, 
        {"gender": "F", "location": "Denver, CO", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Angela Toney.jpg", "position": "Sales", "name": "Angela Toney"}, 
        {"gender": "M", "location": "New York, NY", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Philip Sireci.jpg", "position": "Chef", "name": "Philip Sireci"}, 
        {"gender": "F", "location": "New York, NY", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Shanna Sobel.jpg", "position": "Assistant Chef", "name": "Shanna Sobel"}, 
        {"gender": "M", "location": "Slovenia", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Samo Prelog.jpg", "position": "Developer", "name": "Samo Prelog"}, 
        {"gender": "M", "location": "Denver, CO", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Joel Bradley.jpg", "position": "Web Support Specialist", "name": "Joel Bradley"}, 
        {"gender": "F", "location": "London, UK", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Tania Rahman.jpg", "position": "Sales", "name": "Tania Rahman"}, 
        {"gender": "M", "location": "New York, NY", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Dean Grant.jpg", "position": "Sales", "name": "Dean Grant"}, 
        {"gender": "F", "location": "London, UK", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Angela Nyman.jpg", "position": "Marketing Manager, EMEA", "name": "Angela Nyman"}, 
        {"gender": "M", "location": "New York, NY", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Marvin Medrano.jpg", "position": "Kitchen Assistant", "name": "Marvin Medrano"}, 
        {"gender": "M", "location": "Mechanicsburg, PA", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Joshua Hynes.jpg", "position": "Senior Product Designer", "name": "Joshua Hynes"}, 
        {"gender": "M", "location": "New York, NY", "photo": "http://cdn.sstatic.net/stackexchange/Img/team/Kasra Rahjerdi.jpg", "position": "Developer", "name": "Kasra Rahjerdi"}
    ]

    return HttpResponse(json.dumps(employees_with_gender), content_type='application/json')


def get_employees_from_site():
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
