from django.urls import path
from .views import CompanyEP, CitizenEP, TwoCitizenEP


urlpatterns = [
    path('save_company', CompanyEP.as_view()),
    path('company/<int:company_id>/employees', CompanyEP.as_view()),
    path('citizen', CitizenEP.as_view()),
    path('common_friends', TwoCitizenEP.as_view()),
    path('save_citizen', CitizenEP.as_view()),
]