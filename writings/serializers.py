from rest_framework.serializers import ModelSerializer
from .models import *

class ParagraphSerializer(ModelSerializer):
    class Meta:
        model = Paragraph
        fields = ('pk','index','content','bookmark',)

class ParagraphCreateSerializer(ModelSerializer):
    class Meta:
        model = Paragraph
        fields = ["pk",'index',"content","writing"]
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
        fields = ['pk','format','purpose']

class WritingListModelSerializer(WritingBaseModelSerializer):
    class Meta(WritingBaseModelSerializer.Meta):
        fields = ['pk','format','purpose']
        depth = 1


class ParagraphBaseModelSerializer(ModelSerializer):
    class Meta:
        model = Paragraph
        fields = '__all__'

class ParagraphListModelSerializer(ParagraphBaseModelSerializer):
    writing = WritingBaseModelSerializer()
    class Meta(ParagraphBaseModelSerializer.Meta):
        fields = ['pk','index','writing']
        depth = 1