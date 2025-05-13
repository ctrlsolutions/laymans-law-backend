from rest_framework import viewsets
from .models import Law, Summary, Translation
from .serializers import LawSerializer, SummarySerializer, TranslationSerializer

class LawViewSet(viewsets.ModelViewSet):
    queryset = Law.objects.all()
    serializer_class = LawSerializer

class SummaryViewSet(viewsets.ModelViewSet):
    queryset = Summary.objects.all()
    serializer_class = SummarySerializer

class TranslationViewSet(viewsets.ModelViewSet):
    queryset = Translation.objects.all()
    serializer_class = TranslationSerializer
