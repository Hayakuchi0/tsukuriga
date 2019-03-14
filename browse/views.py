from upload.models import VideoData
from core.utils import AltPaginationListView


class Browse(AltPaginationListView):
    template_name = 'browse/index.html'
    context_object_name = 'videos'

    def get_queryset(self):
        return [v.video for v in VideoData.objects.all().order_by('-video__profile__created_at')]


browse = Browse.as_view()
