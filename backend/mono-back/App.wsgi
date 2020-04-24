import sys

activate_this = "./Scripts/active_this.py"
execfile(activate_this, dict(__file__=activate_this))

sys.path.insert(0, "/wwwroot/open-back")

from App import app as application