from django import template
import datetime

register = template.Library()


@register.simple_tag
def filter_tag(node, time_start, time_end):
    now = datetime.datetime.now()
    start = datetime.datetime(now.year, now.month, now.day, int(time_start[:2]), int(time_start[3:6]))

    if time_end[3:6] == '59':
        end = datetime.datetime(now.year, now.month, now.day, int(time_end[:2]), int(time_end[3:6]), 59, 999999)
        node_obj = node.filter(timestamp__time__gte=start,
                               timestamp__time__lte=end)
    else:
        end = datetime.datetime(now.year, now.month, now.day, int(time_end[:2]), int(time_end[3:6]))

        node_obj = node.filter(timestamp__time__gte=start,
                               timestamp__time__lt=end)

    if node_obj.count() == 0:
        return -1

    total = 0.0
    for n in node_obj:
        total += float(n.moisture)

    ave = float('{number:.{digits}f}'.format(number=total / float(node_obj.count()), digits=1))

    return ave
