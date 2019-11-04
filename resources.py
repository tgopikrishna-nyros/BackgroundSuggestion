from tastypie.resources import ModelResource
from background.models import Picture
class PictureResource(ModelResource):
    class Meta:
        queryset = Picture.objects.all()
        resource_name = 'pic'