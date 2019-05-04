from django.urls import path

from simplechoice.views import IndexView, NewView, ContinueView, DebugView#, PlayView#, SignupView, ActivateView, PageView

app_name = 'simplechoice'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('new/', NewView.as_view(), name='new'),
    path('debug/', DebugView.as_view(), name='debug'),
    path('continue/', ContinueView.as_view(), name='continue'),
]
