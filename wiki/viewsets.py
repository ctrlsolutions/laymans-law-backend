from rest_framework import viewsets
from .models import Law, Summary, Translation, OFWSupportDetail
from .serializers import LawSerializer, SummarySerializer, TranslationSerializer, OFWSupportDetailSerializer

class LawViewSet(viewsets.ModelViewSet):
    queryset = Law.objects.all()
    serializer_class = LawSerializer

class SummaryViewSet(viewsets.ModelViewSet):
    queryset = Summary.objects.all()
    serializer_class = SummarySerializer

class TranslationViewSet(viewsets.ModelViewSet):
    queryset = Translation.objects.all()
    serializer_class = TranslationSerializer
    
class OFWSupportDetailViewSet(viewsets.ModelViewSet):
    queryset = OFWSupportDetail.objects.all()
    serializer_class = OFWSupportDetailSerializer
