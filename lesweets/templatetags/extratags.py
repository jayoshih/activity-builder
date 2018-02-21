import json
import re

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(is_safe=True)
def parsestory(value):
    story = value["story"]
    MATHLIBS_REGEX = r'(\[([^\]]+)\])'
    for match in re.findall(MATHLIBS_REGEX, story):
        try:
            data = next(m for m in value["items"] if m["id"] == match[1])
            span = "<b class='display-blank {}'>{}</b>".format(data["id"], data["label"])
            story = story.replace(match[0], span)
        except StopIteration as e:
            print("No item found in {} with id {}".format(value["id"], match))
    return story
