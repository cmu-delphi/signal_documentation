from rest_framework.serializers import ModelSerializer, SlugRelatedField

from base.serializers import LinkSerializer
from signals.models import Signal, GeographyUnit


class SignalBaseSerializer(ModelSerializer):
    """
    Serializer for the base Signal model.
    """

    class Meta:
        model = Signal
        fields = ['id', 'name', 'display_name']


class SignalSerializer(ModelSerializer):
    """
    Serializer for the Signal model.
    """

    links = LinkSerializer(many=True)
    pathogen = SlugRelatedField(many=True, read_only=True, slug_field='name')
    signal_type = SlugRelatedField(many=True, read_only=True, slug_field='name')
    available_geography = SlugRelatedField(many=True, read_only=True, slug_field='name')
    category = SlugRelatedField(read_only=True, slug_field='name')
    source = SlugRelatedField(read_only=True, slug_field='name')
    base = SignalBaseSerializer()

    class Meta:
        model = Signal
        fields = '__all__'


class GeographyUnitSerialializer(ModelSerializer):
    """
    Serializer for the GeographyUnit model.
    """

    category = SlugRelatedField(read_only=True, slug_field='name')

    class Meta:
        model = GeographyUnit
        fields = '__all__'
