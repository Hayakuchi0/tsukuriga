from django.utils import timezone


class Contribution:
    VIDEO_RATE = 100
    COMMENT_RATE = 80
    FAVORITE_RATE = 50
    POINT_RATE = 20

    def __init__(self, user):
        self.user = user
        self.week_ago = timezone.now() - timezone.timedelta(14)

    def point(self):
        result = 0
        for prop in self.__dir__():
            if prop.startswith('calc_'):
                result += getattr(self, prop)()
        return result

    def calc_videos(self):
        return self.user.video_set.filter(published_at__gte=self.week_ago).count() * self.VIDEO_RATE

    def calc_comments(self):
        return self.user.comment_set.filter(created_at__gte=self.week_ago).count() * self.COMMENT_RATE

    def calc_favorites(self):
        return self.user.favorite_set.filter(created_at__gte=self.week_ago).count() * self.FAVORITE_RATE

    def calc_points(self):
        return self.user.point_set.filter(created_at__gte=self.week_ago).count() * self.POINT_RATE
