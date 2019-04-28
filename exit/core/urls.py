from django.urls import path

from core.views import IndexView, NewView, DebugView#, PlayView#, SignupView, ActivateView, PageView

app_name = 'core'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('new/', NewView.as_view(), name='new'),
    path('debug/', DebugView.as_view(), name='debug'),
    #path('play/', PlayView.as_view(), name='play'),
]
