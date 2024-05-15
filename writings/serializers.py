from rest_framework.serializers import ModelSerializer
from .models import *

class ParagraphSerializer(ModelSerializer):
    class Meta:
        model = Paragraph
        fields = ('pk','content','bookmark',)

class ParagraphCreateSerializer(ModelSerializer):
    class Meta:
        model = Paragraph
        fields = ["pk","content","writing"]
        read_only_fields = ["writing"]

class WritingCreateSerializer(ModelSerializer):
    class Meta:
        model = Writing
        fields = ["pk","format","purpose","writer"]
        read_only_fields = ["writer"]

class WritingSerializer(ModelSerializer):
    paragraphs = ParagraphSerializer(many=True)
    class Meta:
        model = Writing
        fields = ("pk","format","purpose","paragraphs",)

class WritingBaseModelSerializer(ModelSerializer):
    class Meta:
        model = Writing
        fields = '__all__'

class WritingListModelSerializer(WritingBaseModelSerializer):
    class Meta:
        fields = ['pk','format','purpose']
        depth = 1
