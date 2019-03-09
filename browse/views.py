from upload.models import Video
from core.utils import AltPaginationListView


class Browse(AltPaginationListView):
    template_name = 'browse/index.html'
    context_object_name = 'videos'

    def get_queryset(self):
        return Video.objects.all().order_by('-profile__created_at')


browse = Browse.as_view()
