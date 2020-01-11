from rest_framework import serializers
from .models import Company, Citizen


class StringListField(serializers.ListField):  # list of strings
    child = serializers.CharField()


class ValueListField(serializers.ListField):  # list of dictionaries with integer values
    child = serializers.DictField(child=serializers.IntegerField())


class CompanySerializer(serializers.ModelSerializer):
    """
    To deserialize company records in order to save to db
    """
    class Meta:
        model = Company
        fields = "__all__"


class CitizenSerializer(serializers.ModelSerializer):
    """
    To deserialize Citizen data in order to save to db
    """
    favouriteFood = StringListField()
    friends = ValueListField()
    tags = StringListField()

    class Meta:
        model = Citizen
        exclude = ("fruits", "vegetables")

    def create(self, validated_data):
        validated_data['friends'] = [friend['index'] for friend in validated_data['friends']]  # convert to list of int
        return Citizen.objects.create(**validated_data)


class CitizenNameResponseSerializer(serializers.ModelSerializer):
    """
    Serialize / deserialize name field of a citizen/s only
    """

    class Meta:
        model = Citizen
        fields = ['name']


class OneCitizenResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Citizen
        fields = ('name', 'age', 'fruits', 'vegetables')


class TwoCitizenResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Citizen
        fields = ('name', 'age', 'address', 'phone')
