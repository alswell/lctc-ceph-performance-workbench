from django.conf import urls

urlpatterns = []

def register(view):
    p = urls.url(view.url_regex, view.as_view())
    urlpatterns.append(p)
    return view

