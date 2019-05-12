from rest_framework import serializers
from .models import Puppy


class PuppySerializer(serializers.ModelSerializer):
    # 展现的时候会自动调用get_desc方法
    desc = serializers.SerializerMethodField()
    # 展现的时候的值即为models里的Choices里的内容
    human_readable_gender = serializers.CharField(source='get_gender_display', required=False)

    class Meta:
        model = Puppy
        fields = '__all__'

    def get_desc(self, obj):
        return obj.get_breed()
