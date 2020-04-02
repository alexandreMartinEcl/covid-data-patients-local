from django import template
from maj.models import MAJ
register = template.Library()


@register.simple_tag
def last_maj(number: int = 10):
    nb = int(number)
    majs = MAJ.objects.all().order_by("-date")[:nb]
    table = "<table class='table'><tbody>"
    suffix = "</tbody></table>"
    for m in majs:
        table += "<tr><td>" + m.date.strftime("%m-%d-%Y") +\
                 "</td><td>" + m.description + "</td></tr>"
    return table + suffix
