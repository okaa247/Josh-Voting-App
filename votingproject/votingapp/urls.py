from django.urls import path
from .views import *


urlpatterns = [
    path('', Dashboard.as_view(), name='dashboard'),
    path('votingcategorycreate/', VotingCategoryCreateView.as_view(), name='votingcategory-create'),
    path('categories/', VotingCategoryListView.as_view(), name='votingcategory-list'),
    path('votingcategory/<int:category_id>/delete/', VotingCategoryDeleteView.as_view(), name='votingcategory-delete'),
    path('createcandidate/', CandidateCreateView.as_view(), name='create-candidate'),
    path('admincandidates/', AdminCandidateListView.as_view(), name='admin-candidate-list'),
    # path('candidates/<slug:category_slug>/', CandidateListView.as_view(), name='candidate-list'),
    path('candidates/', CandidateListView.as_view(), name='candidate-list'),
    path('admincandidates/<int:candidate_id>/delete/', CandidateDeleteView.as_view(), name='delete-candidate'),
    
    path('vote/<int:candidate_id>/', VoteView.as_view(), name='vote'),
    
    path('initiate-payment/', initiate_payment, name='initiate_payment'),
	path('verify-payment/<str:ref>/', verify_payment, name='verify_payment'),

    # path('profilepage', ProfilePage.as_view(), name='profilepage'),
    # path('payment/', initiate_payment, name='initiate-payment'),
    # path('<str:ref>/', verify_payment, name='verify-payment'),

    # path('categories/<slug:category_slug>', Categories.as_view(), name='category'),
   
    
]


