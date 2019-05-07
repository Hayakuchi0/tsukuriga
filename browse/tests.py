from core.tests import AbstractTests, star_seed, comment_seed
from .models import Ranking
from ajax.models import Point


class CalcPopularTests(AbstractTests):

    def setUp(self):
        self.video = self.create_test_video()
        self.video.views_count = 124
        self.video.published_at = self.last_week
        self.video.save()
        self.add_stars_from_people(
            video=self.video, sender_type="user",
            star_seeds_each=[
                [star_seed(self.last_month, 314), star_seed(self.last_week, 15), star_seed(self.yesterday, 9), ],
                [star_seed(self.yesterday, 26), star_seed(self.today, 5), ],
                [star_seed(self.today, 35), ],
            ]
        )
        self.add_stars_from_people(
            video=self.video, sender_type="ip",
            star_seeds_each=[
                [star_seed(self.today, 897), star_seed(self.today, 93), star_seed(self.yesterday, 23), ],
                [star_seed(self.yesterday, 84), star_seed(self.last_week, 6), ],
                [star_seed(self.last_month, 26), ],
            ]
        )
        self.add_comments_from_people(
            video=self.video,
            comment_seeds_each=[
                [comment_seed(self.today, "TS"), comment_seed(self.today, "U"), comment_seed(self.yesterday, "KU"), ],
                [comment_seed(self.yesterday, "RI"), comment_seed(self.last_week, "G"), ],
                [comment_seed(self.last_month, "A"), ]
            ]
        )
        self.add_favorites(
            video=self.video,
            times=[self.today, self.today, self.yesterday, self.yesterday, self.last_week, self.last_month, ]
        )
        self.video.calculate_rankings()
        self.rankings = Ranking.objects.filter(video=self.video)
        self.users = []
        self.ip_list = []
        for star in Point.objects.all():
            if star.user:
                self.users.append(star.user)
            else:
                self.ip_list.append(star.ip)
        self.users = list(set(self.users))
        self.ip_list = list(set(self.ip_list))

    def rank_stars(self, ranking):
        result = Point.objects.filter(video=self.video)
        if ranking.day_count > 0:
            result = result.filter(created_at__gte=ranking.from_datetime)
        return result

    def test_calc_popular_day(self):
        for day_ranking in self.rankings.filter(day='day'):
            self.assertEqual(day_ranking.calc_popular(), 42)  # ((38+0)*1) + (2*2)

    def test_calc_popular_week(self):
        for week_ranking in self.rankings.filter(day='week'):
            self.assertEqual(week_ranking.calc_popular(), 122)  # ((53+0)*2) + (4*4)

    def test_calc_popular_month(self):
        for month_ranking in self.rankings.filter(day='month'):
            self.assertEqual(month_ranking.calc_popular(), 381)  # ((54+124)*2)+ (5*5)

    def test_calc_popular_all(self):
        for all_ranking in self.rankings.filter(day='all'):
            self.assertEqual(all_ranking.calc_popular(), 627)  # ((73+124)*3) + (6*6)

    def test_sum_of_sqrt_star_login_day(self):
        for day_ranking in self.rankings.filter(day='day'):
            self.assertEqual(day_ranking.sum_of_sqrt_star_login(self.rank_stars(day_ranking), self.users), 7)  # [√35] + [√5]

    def test_sum_of_sqrt_star_login_week(self):
        for week_ranking in self.rankings.filter(day='week'):
            self.assertEqual(week_ranking.sum_of_sqrt_star_login(self.rank_stars(week_ranking), self.users), 13)  # [√35] + [√(5+26)] + [√9]

    def test_sum_of_sqrt_star_login_month(self):
        for month_ranking in self.rankings.filter(day='month'):
            self.assertEqual(month_ranking.sum_of_sqrt_star_login(self.rank_stars(month_ranking), self.users), 14)  # [√35] + [√(5+26)] + [√(9+15)]

    def test_sum_of_sqrt_star_login_all(self):
        for all_ranking in self.rankings.filter(day='all'):
            self.assertEqual(all_ranking.sum_of_sqrt_star_login(self.rank_stars(all_ranking), self.users), 28)  # [√35] + [√(5+26)] + [√(9+15+314)]

    def test_sum_of_sqrt_star_anonymous_day(self):
        for day_ranking in self.rankings.filter(day='day'):
            self.assertEqual(day_ranking.sum_of_sqrt_star_anonymous(self.rank_stars(day_ranking), self.ip_list), 31)  # [√(897+93)]

    def test_sum_of_sqrt_star_anonymous_week(self):
        for week_ranking in self.rankings.filter(day='week'):
            self.assertEqual(week_ranking.sum_of_sqrt_star_anonymous(self.rank_stars(week_ranking), self.ip_list), 40)  # [√(897+93+23)] + [√84]

    def test_sum_of_sqrt_star_anonymous_month(self):
        for month_ranking in self.rankings.filter(day='month'):
            self.assertEqual(month_ranking.sum_of_sqrt_star_anonymous(self.rank_stars(month_ranking), self.ip_list), 40)  # [√(897+93+23)] + [√(84+6)]

    def test_sum_of_sqrt_star_anonymous_all(self):
        for all_ranking in self.rankings.filter(day='all'):
            self.assertEqual(all_ranking.sum_of_sqrt_star_anonymous(self.rank_stars(all_ranking), self.ip_list), 45)  # [√(897+93+23)] + [√(84+6)+[√26]]

    def test_score_of_stars_day(self):
        for day_ranking in self.rankings.filter(day='day'):
            self.assertEqual(day_ranking.score_of_stars(), 38)  # [√5] + [√35] + [√(897+93)]

    def test_score_of_stars_week(self):
        for week_ranking in self.rankings.filter(day='week'):
            self.assertEqual(week_ranking.score_of_stars(), 53)  # [√9] + [√(26+5)] + [√35] + [√(897+93+23)] + [√84]

    def test_score_of_stars_month(self):
        for month_ranking in self.rankings.filter(day='month'):
            self.assertEqual(month_ranking.score_of_stars(), 54)  # [√(15+9)] + [√(26+5)] + [√35] + [√(897+93+23)] + [√(84+6)]

    def test_score_of_stars_all(self):
        for all_ranking in self.rankings.filter(day='all'):
            self.assertEqual(all_ranking.score_of_stars(), 73)  # [√(314+15+9)] + [√(26+5)] + [√35] + [√(897+93+23)] + [√(84+6)] + [√26]

    def test_score_of_view_day(self):
        for day_ranking in self.rankings.filter(day='day'):
            self.assertEqual(day_ranking.score_of_views(), 0)

    def test_score_of_view_week(self):
        for week_ranking in self.rankings.filter(day='week'):
            self.assertEqual(week_ranking.score_of_views(), 0)

    def test_score_of_view_month(self):
        for month_ranking in self.rankings.filter(day='month'):
            self.assertEqual(month_ranking.score_of_views(), 124)

    def test_score_of_view_all(self):
        for all_ranking in self.rankings.filter(day='all'):
            self.assertEqual(all_ranking.score_of_views(), 124)

    def test_score_of_comment_day(self):
        for day_ranking in self.rankings.filter(day='day'):
            self.assertEqual(day_ranking.score_of_comments(), 1)

    def test_score_of_comment_week(self):
        for week_ranking in self.rankings.filter(day='week'):
            self.assertEqual(week_ranking.score_of_comments(), 2)

    def test_score_of_comment_month(self):
        for month_ranking in self.rankings.filter(day='month'):
            self.assertEqual(month_ranking.score_of_comments(), 2)

    def test_score_of_comment_all(self):
        for all_ranking in self.rankings.filter(day='all'):
            self.assertEqual(all_ranking.score_of_comments(), 3)
