from rest_framework.serializers import ModelSerializer

from base.models import Link


class LinkSerializer(ModelSerializer):
    """
    Serializer for the Link model.
    """
    class Meta:
        model = Link
        fields = ['link_type', 'url']
