from account.models import User


def contribution_ranking(request):
    return {'contrib_users': User.objects.all().order_by('-contribution_point')[:10]}
