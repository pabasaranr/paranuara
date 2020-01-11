from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.response import Response
from rest_api.models import Company as ModelCompany, Citizen as ModelCitizen
from rest_api.serializers import CitizenNameResponseSerializer, OneCitizenResponseSerializer, \
    TwoCitizenResponseSerializer, CompanySerializer as ModComSerializer, CitizenSerializer as ModCitSerializer


class ModelClass(APIView):

    model_serializer = None  # MUST declare the serializer inside child classes

    def post(self, request):
        """
        Save a set of data records sent in a json through a given serializer
        :param request: POST request
        model_serializer: Serializer to be used. MUST declare the serializer inside child class.
        :return: Final response of the success/failure
        """
        if request.data:
            try:  # deserialize data and save if valid
                serializer = self.model_serializer(data=request.data, many=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response({'status': 'Records added'}, status=status.HTTP_201_CREATED)
            except ValidationError as e:  # invalid data
                return Response({'error': filter(None, e.detail)}, status=status.HTTP_409_CONFLICT)
        else:
            return Response({'status': 'Data not found'}, status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def db_get(model, **kwargs):
        """
        retrieve a db record with given **kwargs
        :param model: Database model
        :param kwargs: parameters to be passed to query
        :return: database record or response if invalid/not exist
        """
        try:
            db_record = get_object_or_404(model, **kwargs)
        except model.DoesNotExist:
            raise NotFound
        except ValueError:
            raise NotFound(detail="ValueError. Please check input parameters")
        else:
            return db_record

    @staticmethod
    def db_filter(model, **kwargs):
        """
        Return a queryset filtered with given **kwargs
        :param model: Database model
        :param kwargs: parameters to be passed to query
        :return: filtered records or response if invalid
        """
        try:
            records = model.objects.filter(**kwargs)
        except ValueError:
            raise NotFound(detail="ValueError. Please check input parameters")
        if records.exists():
            return records


class CompanyEP(ModelClass):
    """
    Provide functionality to two API endpoints to save company data and retrieve employees from a given company.
    POST (save_company): Receive company data as json in request body and save validated data to database
    GET (company/<company_name>/): Return employee names of a given company
    """
    model_serializer = ModComSerializer

    def get(self, request, company_name):
        company_details = self.db_get(ModelCompany, company=company_name)
        employee_list = self.db_filter(ModelCitizen, company_id=company_details.index)
        if employee_list:
            employee_data = CitizenNameResponseSerializer(employee_list, many=True).data
            return Response(employee_data, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'No employee records available'}, status=status.HTTP_404_NOT_FOUND)


class CitizenEP(ModelClass):
    """
    Provide functionality to three endpoints. One to save citizen data to db, another to send data of a provided citizen
    and the other to send data related to two given citizens and brown eyed living friends common to them
    POST (save_citizen/) : Receive citizen data as json in request body and save to database
    GET (citizen) : Return citizen data with their fruits and vegetable preferences to a provided citizen (citizen id)
    GET (common_friends) : Return citizen data and common brown eyed living friends to given two citizens (citizen id)
    """
    model_serializer = ModCitSerializer

    def get(self, request):
        citizen_one = request.GET.get('citizen_one', None)
        if citizen_one:
            citizen_one = self.db_get(ModelCitizen, index=request.GET['citizen_one'])
            citizen_serializer = OneCitizenResponseSerializer(citizen_one)  # serialize citizen's data
            return Response(citizen_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'parameters not found'}, status=status.HTTP_204_NO_CONTENT)


class TwoitizenEP(ModelClass):
    """
    Provide functionality to the endpoint sending data related to two given citizens and brown eyed living friends
    common to them
    GET (common_friends) : Return citizen data and common brown eyed living friends to given two citizens (citizen id)
    """
    model_serializer = ModCitSerializer

    def get(self, request):
        citizen_one = request.GET.get('citizen_one', None)
        citizen_two = request.GET.get('citizen_two', None)
        if citizen_one and citizen_two:
            citizens = self.db_filter(ModelCitizen, index__in=[citizen_one, citizen_two])
            if citizens.count() != 2:  # if sent unavailable citizen ids
                return Response({'error': 'citizens not found'}, status=status.HTTP_404_NOT_FOUND)
            else:
                citizen_serializer = TwoCitizenResponseSerializer(citizens, many=True)  # serialize citizens' data
                friends = set(citizens[0].friends)  # common friends
                friends.intersection_update(citizens[1].friends)
                brown_living_friends = self.db_filter(ModelCitizen, eyeColor='brown', has_died=0, index__in=list(friends))
                # serialize brown eyed common living friends
                brown_living_friends_serializer = CitizenNameResponseSerializer(brown_living_friends, many=True)
                return Response({'citizens': citizen_serializer.data,
                                 'common_browneyed_living': brown_living_friends_serializer.data},
                                status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error': 'parameters not found'}, status=status.HTTP_204_NO_CONTENT)