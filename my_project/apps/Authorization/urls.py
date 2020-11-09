from django.urls import path
from .views import Registration, Authorize

urlpatterns = [
   path('registration/', Registration.as_view()),
   path('login/', Authorize.as_view()),
]
