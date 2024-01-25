from django.urls import path
# NOTE: Import the view from the file where you saved it
from found.Process.views import PileAPIView, FootingAPIView, GroundAPIView


urlpatterns = [
    # Register our view
     path('pile/',
         PileAPIView.as_view(),
         name='pile'), 
    path('footing/',
         FootingAPIView.as_view(),
         name='footing'),
     path('ground/',
         GroundAPIView.as_view(),
         name='ground'),
     
]