# serializers.py
from rest_framework import serializers
from .models import Law, Summary, Translation

class SummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Summary
        fields = ['summary']

class TranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Translation
        fields = ['language_tagalog', 'language_bisaya', 'language_waray']

class LawSerializer(serializers.ModelSerializer):
    summary = SummarySerializer(read_only=True)
    translation = TranslationSerializer(read_only=True)

    class Meta:
        model = Law
        fields = ['id', 'title', 'code', 'full_law', 'summary', 'translation']
