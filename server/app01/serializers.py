from rest_framework import serializers

from .models import AudioUploadLoggingModel, BirdInfo


class AudioUploadSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    aid = serializers.SerializerMethodField()

    class Meta:
        model = AudioUploadLoggingModel
        fields = (
            'aid', 'file_name', 'classic', 'create_time'
        )

    def get_aid(self, obj):
        return obj.id


class BirdInfoSerializer(serializers.ModelSerializer):
    bid = serializers.SerializerMethodField()

    class Meta:
        model = BirdInfo
        fields = (
            'bid', 'name_CN', 'name_EN', 'wiki_link', 'image_link'
        )

    def get_bid(self, obj):
        return obj.id
