from django.urls import path
from .views import CompanyEP, CitizenEP, TwoitizenEP


urlpatterns = [
    path('save_company', CompanyEP.as_view()),
    path('company/<slug:company_name>/', CompanyEP.as_view()),
    path('citizen', CitizenEP.as_view()),
    path('common_friends', TwoitizenEP.as_view()),
    path('save_citizen/', CitizenEP.as_view()),
]