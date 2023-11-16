import requests
from django.db.models import Count, Q
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
import random

from .models import Joke, Entertainments, DogsPhoto
from .serializers import JokeSerializer, EntertainmentsSerializer, DogsPhotoSerializer, JokeRandomSerializer
from django.conf import settings


class BaseViewSet(APIView):
    permission_classes = [AllowAny]
    serializer_class = None
    api_url = None

    def post(self, request):
        response = requests.get(self.api_url)
        self.serializer_class.save_response(response.json(), response_data=response.json())
        return Response(response.json(), status=response.status_code)


class JokeViewSet(BaseViewSet):
    serializer_class = JokeSerializer
    api_url = settings.URL_JOKES


class EntertainmentsViewSet(BaseViewSet):
    serializer_class = EntertainmentsSerializer
    api_url = settings.URL_ENTERTAINMENTS


class DogsPhotoViewSet(BaseViewSet):
    serializer_class = DogsPhotoSerializer
    api_url = settings.URL_PHOTO


class RandomPhotoViewSet(APIView):
    serializer_class = DogsPhotoSerializer
    permission_classes = [AllowAny]

    def get(self, request):
        count_id = DogsPhoto.objects.count()
        data = DogsPhoto.objects.filter(id=random.randint(1, count_id)).values_list('link', 'status')
        print(data)
        return Response(data)


class RandomEntertainmentsViewSet(APIView):
    serializer_class = EntertainmentsSerializer
    permission_classes = [AllowAny]

    def get(self, request):
        count_id = Entertainments.objects.count()
        data = Entertainments.objects.filter(id=random.randint(1, count_id)).values_list('entertainment', 'participants')
        print(data)
        return Response(data)


class RandomJokeViewSet(APIView):
    # serializer_class = JokeRandomSerializer
    serializer_class = JokeSerializer
    permission_classes = [AllowAny]

    # def get(self, request): # Способ извлечение из БД с помощью сериализатора
    #     max_count = random.randint(0, Joke.objects.count())
    #     data = Joke.objects.values().get(id=max_count)
    #     print(data)
    #     serialaizer = self.serializer_class(data)
    #     return Response(serialaizer.data)

    def get(self, request): # Способ извлечение из БД
        count_id = Joke.objects.count()
        data = Joke.objects.filter(id=random.randint(1, count_id)).values_list('joke_setup', 'joke_punchline')
        print(data)
        return Response(data)
