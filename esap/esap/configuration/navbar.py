from django.utils.translation import gettext as _

frontend_basename = "esap-gui"

logo = "https://alta.astron.nl/alta-static/images/esap/esap_logo.png"

# definition of the navigation bar items
archives = {"title": _("Archives"), "route": "/archives"}
multi_query = {"title": _("Multi Query"), "route": "/query"}
ida = {"title": _("Interactive Analysis"), "route": "/interactive"}
jobs = {"title": _("Asynchronous Jobs"), "route": "/jobs"}
samp = {"title": _("IVOA-SAMP"), "route": "/samp"}

# Older navbar items
# rucio = {"title": _("Rucio"), "route": "/rucio"}
# batch_analysis = {"title": _("Batch Analysis"), "route": "/batch"}
# asteroids = {"title": _("Asteroids"), "route": "/aladin_simple"}
# exoplanets = {"title": _("Exoplanets"), "route": "/aladin_advanced"}

# Order of the navbar items
navbar = [archives, multi_query, ida, jobs, samp]
