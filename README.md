A quickly thrown together employee name recognition application to help me learn the fine folks I work with at [Stack Exchange](http://stackexchange.com/), running off of Django on Heroku.

The majority of the nitty-gritty work for the app is in staticfiles/main.js, the Django requirement was only done because I expected to need a webserver and ended up not needing it at all. You can look in quiz/views.py$get_employees_from_site to see what I was originally doing that needed a web server.


## setting up a dev environment

Note: This assumes you already have Python and the Heroku Toolbelt installed. If you don't, [check it out here](https://devcenter.heroku.com/articles/getting-started-with-django#prerequisites).

1. Clone this repository
1. In the folder for this, run `virtualenv venv --distribute`
1. `source venv/bin/activate` to enter the virtualenv
1. `pip install -r requirements.txt` to install the requirements.
1. `foreman start`
1. Visit [http://127.0.0.1:5000/](http://127.0.0.1:5000/)


To set this application up on Heroku, follow the instructions in the link to them above to set up an environment, then add a git remote of this repository to your Heroku repo.
