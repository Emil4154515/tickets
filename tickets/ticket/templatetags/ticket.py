from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def query_transform(context, **kwargs):
    query = context['request'].GET.copy()
    for k, v in kwargs.items():
        query[k] = v
    return query.urlencode()


@register.simple_tag(takes_context=True)
def query_transform(context, **kwargs):
    query = context['request'].GET.copy()
    for k, v in kwargs.items():
        if k in query and str(v) in query.getlist(k):
            handler = query.getlist(k)
            handler.remove(str(v))
            query.setlist(k, handler)
        elif k in query:
            query.update({k: str(v)})
        else:
            query[k] = str(v)
    return query.urlencode()


@register.simple_tag(takes_context=True)
def query_transform_change(context, **kwargs):
    query = context['request'].GET.copy()
    for k, v in kwargs.items():
        query[k] = v
    return query.urlencode()