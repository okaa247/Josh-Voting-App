from .models import *



def cate_list(request):
    categories =VotingCategory.objects.all()
    global_list = []
    for category in categories:
            candidates = Candidate.objects.filter(voting_category=category)
            global_list.append((category, candidates))
    return {
        'global_list': global_list,
    }
