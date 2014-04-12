from django.views import generic
from django.db.models import get_model
from django.template import loader, RequestContext
from django.utils.translation import ugettext_lazy as _

from fancypages.assets import forms
from fancypages.mixins import JSONResponseMixin


ImageAsset = get_model('assets', 'ImageAsset')


class ImageListView(generic.ListView):
    model = ImageAsset
    template_name = 'fancypages/assets/image_list.html'
    context_object_name = 'image_list'


class ImageAssetCreateView(JSONResponseMixin, generic.CreateView):
    model = ImageAsset
    template_name = 'fancypages/assets/image_update.html'
    form_class = forms.ImageAssetCreateForm
    thumbnail_template_name = 'fancypages/assets/partials/image_thumbnail.html'

    def get(self, request, *args, **kwargs):
        return self.render_to_error_response(
            _("It is not possible to upload images using a get request."))

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.name = self.object.image.name
        self.object.creator = self.request.user
        self.object.save()

        f = self.request.FILES.get('image')

        template = loader.get_template(self.thumbnail_template_name)
        thumbnail_markup = template.render(RequestContext(self.request, {
            'image_asset': self.object,
        }))

        ctx = {
            'images': [{
                'name': f.name,
                'url': self.object.get_absolute_url(),
                'thumbnailMarkup': thumbnail_markup,
                # TODO add the delete URL back in again
                # reverse('upload-delete', args=[self.object.id]),
                'deleteUrl': '',
                'deleteType': 'DELETE',
            }]
        }
        return self.render_to_response(ctx)
