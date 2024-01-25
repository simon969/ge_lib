# https://sourcery.blog/a-comprehensive-guide-to-api-views-in-django-rest-framework-part-1/

# This is how the basic APIView class is imported
from rest_framework.views import APIView
# DRF provides its own Response object which we will
# use in place of Django's standard HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response 
from django.http import JsonResponse
from found.pyPile.PileProcess import process_request as process_pile_request
from found.pyFooting.FootingProcess import process_request as process_footing_request
from found.pyGround.GroundProcess import process_request as process_ground_request
import json
from pathlib import Path

class PileAPIView(APIView):
   
    def post(self, request, *args, **kwargs):
        
        try:
            data = json.loads(request.body)
            ret = process_pile_request (data, "json")
            return Response (ret)
        
        except Exception as e:
            msg = "problem processing pile request {0}".format(str(e))
            return Response({'error':msg})
    
    # def get (self, request,*args, **kwargs):
    #     try:
    #         data = json.loads(request.body)
    #         ret = process_pile_request (data, "json")
    #         return Response (ret)
        
    #     except Exception as e:
    #         msg = "problem processing pile request {0}".format(str(e))
    #         return Response({'error':msg})
   
class FootingAPIView(APIView):
   
   def post(self, request, *args, **kwargs):
        
        try:
            data = json.loads(request.body)
            ret = process_footing_request (data, "json")
            return Response (ret)
        
        except Exception as e:
            msg = "problem processing footing request {0}".format(str(e))
            return Response({'error':msg})    

class GroundAPIView(APIView):
   
   def post(self, request, *args, **kwargs):
        
        try:
            data = json.loads(request.body)
            ret = process_ground_request (data, "json")
            return Response (ret)
        
        except Exception as e:
            msg = "problem processing ground request {0}".format(str(e))
            return Response({'error':msg})  