import sys

activate_this = "/wwwroot/open-back/Scripts/activate_this.py"
exec(open(activate_this).read(), dict(__file__=activate_this))

sys.path.insert(0, "/wwwroot/open-back")

from App import app as application