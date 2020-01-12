from django.test import TestCase, Client
from rest_framework.test import APITestCase
from rest_framework import status
import json
from .models import Citizen, Company


client = Client()


class CitizenModelTest(TestCase):
    """ Test module for Citizen Model"""

    def setUp(self):
        Citizen.objects.create(index=1, guid="5efdre5d-61c0-4f3b-8b92-d77310c7fa43", has_died=False, balance="$2,418.59",
                               picture="http://placehold.it/12x32", age=34, eyeColor="brown", name="Carla Gunasinghe",
                               gender="female", company_id=58, email="carlagpt@earthmark.com",
                               phone="+1 (910) 587-3630", address="628 Winter is here, Spiderville, America, 9819",
                               about="Tengo agua, por favor", greeting="Hello, Carmella Lambert!",
                               registered="2016-07-13T12:29:07 -10:00", tags=["id", "sint"], friends=[3, 4, 5],
                               favouriteFood=["banana", "apple", "cucumber"])

    def test_citizen_model(self):
        carla = Citizen.objects.get(index=1)
        self.assertEqual(carla.name, "Carla Gunasinghe")
        self.assertCountEqual(carla.fruits, ["banana", "apple"])
        self.assertCountEqual(carla.friends, [3, 4, 5])
        self.assertCountEqual(carla.vegetables, ["cucumber"])
        self.assertEqual(carla.has_died, 0)


class CitizenPOSTAPITest(APITestCase):
    """Test POST api to save citizen data"""

    def test_create_invalid(self):
        invalid_payload1 = [
            {"_id": "595eeb9b96d80a5bc7afb106", "index": "12", "guid": "5e71dc5d-61c0-4f3b-8b92-d77310c7fa43",
             "has_died": False, "balance": "$2,418.59", "picture": "http://placehold.it/32x32", "age": 61,
             "eyecolor": "blue", "name": "Mallika Gunasinghe", "gender": "female", "company_id": 58,
             "email": "carmellalambert@earthmark.com", "phone": "+1 (910) 567-3630", "address": "6289819",
             "about": "Non duis dol aliquip.", "registered": "2016-07-13T12:29:07 -10:00",
             "tags": ["id", "quis", "ullamco", "velit"], "friends": [{"index": 3}, {"index": 4}],
             "greeting": "Hello, Carmella Lambert! You have 6 unread messages.",
             "favouriteFood": ["orange", "apple", "banana", "cucumber"]}]
        response = client.post('https://127.0.0.1:8000/rest/save_citizen', data=json.dumps(invalid_payload1),
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_create_valid(self):
        # payload with data
        valid_payload1 = [{"_id": "595eeb9b96d80a5bc7afb106", "index": 2, "guid": "5e71dc5d-61c0-4f3b-8b92-d77310c7fa43",
                           "has_died": False, "balance": "$2,418.59", "picture": "http://plaehold.it/32x32", "age": 61,
                           "eyeColor": "blue", "name": "Tilaka Gunasinghe", "gender": "female", "company_id": 58,
                           "email": "caghbert@earthmark.com", "phone": "+1 (910) 567-3630", "address": "6289819",
                           "about": "Non duis dol aliquip.", "registered": "2016-07-13T12:29:07 -10:00",
                           "tags": ["id", "quis", "ullamco", "velit"], "friends": [{"index": 3}, {"index": 4}],
                           "greeting": "Hello, Carmella Lambert! You have 6 unread messages.",
                           "favouriteFood": ["orange", "apple", "banana", "cucumber"]}]
        response = client.post('https://127.0.0.1:8000/rest/save_citizen', data=json.dumps(valid_payload1),
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # status ok
        # values ok
        tilaka = Citizen.objects.get(index=2)
        self.assertEqual(tilaka.name, "Tilaka Gunasinghe")
        self.assertCountEqual(tilaka.fruits, ["banana", "apple", "orange"])
        self.assertCountEqual(tilaka.friends, [3, 4])
        self.assertCountEqual(tilaka.vegetables, ["cucumber"])
        self.assertEqual(tilaka.has_died, 0)

        # payload without data
        response = client.post('https://127.0.0.1:8000/rest/save_citizen', data=json.dumps([]),
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class CompanyEmployeeGETAPITEST(APITestCase):
    """ Test company employee GET"""

    def setUp(self):
        Citizen.objects.create(index=7, guid="5efdre5d-61c0-4f3b-8b92-d77310c7fa43", has_died=False, balance="$2,418.59",
                               picture="http://placehold.it/12x32", age=34, eyeColor="brown", name="Martin Mystery",
                               gender="male", company_id=9, email="carlagpt@earthmark.com",
                               phone="+1 (910) 587-3630", address="628 Winter is here, Spiderville, America, 9819",
                               about="Tengo agua, por favor",
                               registered="2016-07-13T12:29:07 -10:00", tags=["id", "sint"],
                               friends=[3, 4, 5],
                               greeting="Hello, Carmella Lambert!",
                               favouriteFood=["banana", "apple", "cucumber"])
        Company.objects.create(index=9, company='ASDFG')
        Company.objects.create(index=10, company='QWERTY')

    def test_company_employee_unavailable(self):
        # company without employees
        response = client.get('https://127.0.0.1:8000/rest/company/QWERTY/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_company_get_employees(self):
        # company with employees
        response = client.get('https://127.0.0.1:8000/rest/company/ASDFG/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_company_not_available(self):
        # company not found
        response = client.get('https://127.0.0.1:8000/rest/company/NOTAVAILABLE/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CompanyModelTest(TestCase):
    """ Test module for Company Model"""
    def setUp(self):
        Company.objects.create(index=2, company='PANPRODUCT')
        Company.objects.create(index=1, company='TGTR')

    def test_company_model(self):
        panproduct = Company.objects.get(company='PANPRODUCT')
        tgtr = Company.objects.get(index=1)
        self.assertEqual(panproduct.index, 2)
        self.assertEqual(tgtr.company, "TGTR")


class CompanyPOSTAPITest(APITestCase):
    """ Test company data save through POST"""

    def setUp(self):
        self.valid_payload1 = [{"index": 4, "company": "LINGOAGE"}, {"index": 3, "company": "MAINELAND"}]

    def test_create_invalid(self):
        # payload with incorrect keys
        invalid_payload1 = [{"jibberish": 2, "company": "LINGOAGE"}, {"index": 5, "company": "GFDS"}]
        response = client.post('https://127.0.0.1:8000/rest/save_company', data=json.dumps(invalid_payload1),
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

        # payload with incorrect values
        invalid_payload2 = [{"index": "error", "company": "DHJHEUS"}, {"index": 54, "company": "ASGED"}]
        response = client.post('https://127.0.0.1:8000/rest/save_company', data=json.dumps(invalid_payload2),
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

        # payload with incorrect content type
        response = client.post('https://127.0.0.1:8000/rest/save_company', data=json.dumps(self.valid_payload1),
                               content_type='text/plain')
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_create_valid(self):
        # payload with data
        response = client.post('https://127.0.0.1:8000/rest/save_company', data=json.dumps(self.valid_payload1),
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # payload without data
        response = client.post('https://127.0.0.1:8000/rest/save_company', data=json.dumps([]),
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class OneCitizenGETAPITEST(APITestCase):
    """ Test citizen data GET"""

    def setUp(self):
        Citizen.objects.create(index=17, guid="5efdre5d-61c0-4fgd-8b92-d77310c7fa43", has_died=False,
                               balance="$2,418.59",
                               picture="http://placehold.it/12x32", age=44, eyeColor="brown", name="Harry Potter",
                               gender="male", company_id=4, email="voldermort@hogwarts.com",
                               phone="+1 (910) 587-3630", address="628 Winter is here, Spiderville, America, 9819",
                               about="Tengo agua, por favor",
                               registered="2016-07-13T12:29:07 -10:00", tags=["id", "sint"],
                               friends=[3, 4, 5],
                               greeting="Expelliarmus",
                               favouriteFood=["banana", "apple", "cucumber"])

    def test_citizen_get_invalid(self):
        # citizen not available
        response = client.get('https://127.0.0.1:8000/rest/citizen', data={"citizen_one": 231})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # citizen id invalid
        response = client.get('https://127.0.0.1:8000/rest/citizen', data={"citizen_one": "45"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # citizen id not sent / wrong key
        response = client.get('https://127.0.0.1:8000/rest/citizen', data={"wrong_key": 17})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_citizen_get_valid(self):
        response = client.get('https://127.0.0.1:8000/rest/citizen', data={"citizen_one": 17})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TwoCitizenGETAPITEST(APITestCase):
    """ Test two citizen common brown eyed friends GET"""
    def setUp(self):
        Citizen.objects.create(index=10, guid="b4ec8asa-7b57-4830-bf46-140135123549", has_died=False,
                               balance="$3,433.05", picture="http://placehold.it/32x32", age=62,
                               eyeColor="blue", name="Mindy Beasley", gender="female", company_id=18,
                               email="mindybeasley@earthmark.com", phone="+1 (862) 503-2197",
                               address="628 Brevoort Place, Bellamy, Kansas, 2696",
                               about="Et cois ut. Amet et nostrud dolorecupidatat do officia ent id excepteur.",
                               registered="2017-03-19T03:28:28 -11:00",
                               tags=["exercitation", "ad", "amet"], friends=[11, 12],
                               greeting= "Hello, Mindy Beasley! You have 8 unread messages.",
                               favouriteFood= ["orange", "apple", "banana", "strawberry"])

        Citizen.objects.create(index=11, guid="b4ec8asa-7b57-4830-bf46-140135123549", has_died=False,
                               balance="$3,433.05", picture="http://placehold.it/32x32", age=64,
                               eyeColor="blue", name="Carla Beasley", gender="female", company_id=18,
                               email="mindybeasley@earthmark.com", phone="+1 (862) 503-2197",
                               address="628 Brevoort Place, Bellamy, Kansas, 2696",
                               about="Et cois ut. Amet et nostrud dolorecupidatat do officia ent id excepteur.",
                               registered="2017-03-19T03:28:28 -11:00",
                               tags=["exercitation", "ad", "amet"], friends=[10, 12],
                               greeting="Hello, Mindy Beasley! You have 8 unread messages.",
                               favouriteFood=["orange", "apple", "banana", "strawberry"])

        Citizen.objects.create(index=12, guid="b4ec8asa-7b57-4830-bf46-140135123549", has_died=False,
                               balance="$3,433.05", picture="http://placehold.it/32x32", age=68,
                               eyeColor="brown", name="Molly Beasley", gender="female", company_id=18,
                               email="mindybeasley@earthmark.com", phone="+1 (862) 503-2197",
                               address="628 Brevoort Place, Bellamy, Kansas, 2696",
                               about="Et cois ut. Amet et nostrud dolorecupidatat do officia ent id excepteur.",
                               registered="2017-03-19T03:28:28 -11:00",
                               tags=["exercitation", "ad", "amet"], friends=[11, 10],
                               greeting="Hello, Mindy Beasley! You have 8 unread messages.",
                               favouriteFood=["orange", "apple", "banana", "strawberry"])

    def test_brown_friends(self):
        response = client.get('https://127.0.0.1:8000/rest/common_friends', data={"citizen_one": 10, "citizen_two": 11})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['common_browneyed_living'], [{"name": "Molly Beasley"}])

    def test_citizens_not_available(self):
        response = client.get('https://127.0.0.1:8000/rest/common_friends', data={"citizen_one": 100, "citizen_two": 12})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_no_brown_friends(self):
        response = client.get('https://127.0.0.1:8000/rest/common_friends', data={"citizen_one": 10, "citizen_two": 12})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['common_browneyed_living'], [])

    def test_no_para(self):
        response = client.get('https://127.0.0.1:8000/rest/common_friends', data={"wrong_key": 17})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)








