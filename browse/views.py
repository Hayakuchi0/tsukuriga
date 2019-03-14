from upload.models import Video
from core.utils import AltPaginationListView


class Browse(AltPaginationListView):
    template_name = 'browse/index.html'
    context_object_name = 'videos'

    def get_queryset(self):
        return Video.objects.filter(profile__isnull=False, data__isnull=False).order_by('-profile__created_at')


browse = Browse.as_view()
