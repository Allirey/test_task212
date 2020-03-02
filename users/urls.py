from django.urls import path

from . import views

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('activate/<uidb64>/<token>/', views.ActivateView.as_view(), name='activate'),
    path('activate/done/', views.activate_request, name='activate_request'),
]
