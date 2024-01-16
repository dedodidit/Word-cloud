from rest_framework import serializers
from .models import WineMask


class WineMaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = WineMask
        fields = "__all__"
