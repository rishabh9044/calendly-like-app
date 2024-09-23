import sys

# add your project directory to the sys.path
project_home = '~/PycharmProjects/calendly-like-app/'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

from controller.app import app as application  # noqa

application.run(debug=True)