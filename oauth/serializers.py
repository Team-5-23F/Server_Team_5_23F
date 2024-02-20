from rest_framework import serializers


class CallbackUserInfoSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=1000, required=False, help_text="접속 코드 (Web)")
    access_token = serializers.CharField(max_length=1000, required=False, help_text="토큰 (Mobile)")

class CallbackAppleInfoSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=1000, required=False, help_text="접속 코드(Web)")
