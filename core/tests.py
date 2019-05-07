from django.test import TestCase
from django.utils import timezone
from account.models import User
from ajax.models import Comment, Point
from upload.models import Video, VideoProfile
from ipaddress import IPv4Address


def star_seed(time, count):
    return {"time": time, "count": count}


def comment_seed(time, text):
    return {"time": time, "text": text}


class AbstractTests(TestCase):

    usernumber = 0
    ipnumber = 0
    last_month = timezone.now() - timezone.timedelta(31)
    last_week = timezone.now() - timezone.timedelta(8)
    yesterday = timezone.now() - timezone.timedelta(hours=25)
    today = timezone.now() - timezone.timedelta(hours=23)

    def create_test_user(self):
        self.usernumber += 1
        return User.objects.create(username='JohnDoe'+str(self.usernumber), name='名無しの権兵衛'+str(self.usernumber)+'号')

    def create_test_users(self, number):
        result = []
        for i in range(number):
            result.append(self.create_test_user())
        return result

    def create_test_ip(self):
        self.ipnumber += 1
        return str(IPv4Address(self.ipnumber))

    def create_test_video(self):
        author = self.create_test_user()
        result = Video.objects.create(user=author, is_active=True)
        VideoProfile.objects.create(video=result, title='かっこいいムービー')
        result.publish_and_save()
        return result

    def add_star(self, video, sender, star_seed):
        point = Point.objects.create(
            video=video, count=star_seed["count"], created_at=star_seed["time"], updated_at=star_seed["time"]
        )
        if type(sender) is User:
            point.user = sender
        else:
            point.ip = sender
        point.save()

    def add_stars_from_person(self, video, sender, star_seeds):
        for star_seed in star_seeds:
            self.add_star(video, sender, star_seed)

    def add_stars_from_people(self, video, sender_type, star_seeds_each):
        for star_seeds in star_seeds_each:
            if sender_type == "user":
                sender = self.create_test_user()
            else:
                sender = self.create_test_ip()
            self.add_stars_from_person(video, sender, star_seeds)

    def add_favorites(self, video, times):
        for time in times:
            user = self.create_test_user()
            video.favorite_set.create(user=user, created_at=time, updated_at=time)

    def add_comment(self, video, user, comment_seed):
        comment = Comment.objects.create(
            video=video, user=user, text=comment_seed["text"], created_at=comment_seed["time"]
        )
        comment.save()

    def add_comments_from_person(self, video, user, comment_seeds):
        for comment_seed in comment_seeds:
            self.add_comment(video, user, comment_seed)

    def add_comments_from_people(self, video, comment_seeds_each):
        for comment_seeds in comment_seeds_each:
            user = self.create_test_user()
            self.add_comments_from_person(video, user, comment_seeds)
