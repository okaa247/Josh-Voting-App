from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from .models import *
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.conf import settings
from django.contrib import messages
from django.views import View




class Dashboard(View):
    def get(self, request):
        return render(request, 'index.html')
    
    def post(self, request):
        return render(request, 'index.html')



# class DashboardView(View):
#     template_name = 'dashboard.html'

#     def get(self, request):
#         categories = VotingCategory.objects.all()
#         candidates = Candidate.objects.all()
#         return render(request, self.template_name, {'categories': categories, 'candidates': candidates})


# For voting category creation
class VotingCategoryCreateView(View):
    def get(self, request):
        return render(request, 'votingcategory_create.html')

    def post(self, request):
        name = request.POST.get('name')
        if request.user.is_superuser:
            try:
                category = VotingCategory.objects.create(name=name)
            except IntegrityError:
                error = "Category with this name already exists."
                messages.error(request, 'Voting category already exists.')
                return render(request, 'votingcategory_create.html', {'error': error})
            return redirect('votingcategory-list')
        return redirect('dashboard')



# This is for viewing voting categories
class VotingCategoryListView(View):
    def get(self, request):
        categories = VotingCategory.objects.all()
        return render(request, 'votingcategory_list.html', {'categories': categories})
    


class VotingCategoryDeleteView(View):
    def get(self, request, category_id):
        category = get_object_or_404(VotingCategory, id=category_id)
        return render(request, 'votingcategory_delete.html', {'category': category})

    def post(self, request, category_id):
        if request.user.is_superuser:
            category = get_object_or_404(VotingCategory, id=category_id)
            category.delete()
            messages.success(request, 'Voting category deleted successfully.')
            return redirect('votingcategory-list')
        else:
            return redirect('dashboard')





class CandidateCreateView(View):

    def get(self, request):
        voting_categories = VotingCategory.objects.all()
        return render(request, 'create_candidate.html', {'voting_categories': voting_categories})

    def post(self, request):
        name = request.POST.get('name')
        bio = request.POST.get('bio')
        voting_category_id = request.POST.get('voting_category')

        if request.user.is_superuser:
            # Validate the inputs as needed
            candidate_image = request.FILES.get('candidate_image')
            voting_category = VotingCategory.objects.get(pk=voting_category_id)

            new_candidate = Candidate.objects.create(
                name=name,
                bio=bio,
                candidate_image=candidate_image,
                voting_category=voting_category
            )
            return redirect('admin-candidate-list')
        return redirect('dashboard')




class CandidateListView(View):

    @staticmethod
    def payment_verified(user):
        # Define your logic to check if the user's payment is verified
        return user.payment_set.filter(verified=True).exists()

    @method_decorator(login_required(login_url='/user/login/'))
    @method_decorator(user_passes_test(payment_verified, login_url='/initiate-payment/'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        # Your existing view logic here
        categories = VotingCategory.objects.all()
        categories_with_candidates = []

        for category in categories:
            candidates = Candidate.objects.filter(voting_category=category)
            categories_with_candidates.append((category, candidates))

        context = {
            'categories_with_candidates': categories_with_candidates
        }

        return render(request, 'candidate_list.html', context=context)



class AdminCandidateListView(View):

    def get(self, request):
        # Your existing view logic here
        categories = VotingCategory.objects.all()
        categories_with_candidates = []

        for category in categories:
            candidates = Candidate.objects.filter(voting_category=category)
            categories_with_candidates.append((category, candidates))

        context = {
            'categories_with_candidates': categories_with_candidates
        }

        return render(request, 'admin_candidate_list.html', context=context)



class CandidateDeleteView(View):
    def get(self, request, candidate_id):
        if request.user.is_superuser:
            candidate = get_object_or_404(Candidate, id=candidate_id)
            return render(request, 'delete_candidate_confirm.html', {'candidate': candidate})
        else:
            return redirect('dashboard')

    def post(self, request, candidate_id):
        if request.user.is_superuser:
            candidate = get_object_or_404(Candidate, id=candidate_id)
            candidate.delete()
            messages.success(request, 'Candidate deleted successfully.')
            return redirect('admin-candidate-list')
        else:
            return redirect('dashboard')



class VoteView(View):

    @staticmethod
    def payment_verified(user):
        # Define your logic to check if the user's payment is verified
        return user.payment_set.filter(verified=True).exists()

    @method_decorator(login_required(login_url='/user/login/'))
    @method_decorator(user_passes_test(payment_verified, login_url='/initiate-payment/'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, candidate_id):
        # Check if the user has already voted in this category
        candidate = get_object_or_404(Candidate, id=candidate_id)
        category = candidate.voting_category
        user_has_voted = Candidate.objects.filter(
            voting_category=category, votes__id=request.user.id
        ).exists()

        if user_has_voted:
            return redirect('candidate-list')
            # return HttpResponse("You have already voted in this category")

        return render(request, 'vote.html', {'candidate': candidate})

    def post(self, request, candidate_id):
        candidate = get_object_or_404(Candidate, id=candidate_id)

        # Check if the user has already voted in this category
        category = candidate.voting_category
        user_has_voted = Candidate.objects.filter(
            voting_category=category, votes__id=request.user.id
        ).exists()

        if user_has_voted:
            return redirect('candidate-list')
        
        # Save the vote
        candidate.votes.add(request.user)

        # Update the votes count for the candidate
        candidate.votes_count += 1
        candidate.save()

        return redirect('candidate-list')



def initiate_payment(request):
	if request.method == "POST":
		amount = 50
		email = request.POST['email']

		pk = settings.PAYSTACK_PUBLIC_KEY

		payment = Payment.objects.create(amount=amount, email=email, user=request.user)
		payment.save()

		context = {
			'payment': payment,
			'field_values': request.POST,
			'paystack_pub_key': pk,
			'amount_value': payment.amount_value(),
		}
		return render(request, 'make_payment.html', context)
    
	return render(request, 'payment.html')


def verify_payment(request, ref):
    payment = get_object_or_404(Payment, ref=ref)
    verified = payment.verify_payment()

    if verified:
        print(request.user.username, " payment successfully")
        return CandidateListView.as_view()(request)
    else:
        return render(request, "payment.html")








# def initiate_payment(request: HttpResponse) -> HttpResponse:
#     if request.method == "POST":
#         payment_form = forms.PaymentForm(request.POST)
#         if payment_form.is_valid():
#             payment = payment_form.save()
#             return render(request, 'make_payment.html', {'payment': payment, 'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY})
#     else:
#         payment_form = forms.PaymentForm()
#     return render(request, 'initiate_payment.html', {'payment_form': payment_form})           


# def verify_payment(request: HttpResponse, ref: str) -> HttpResponse:
#     payment = get_object_or_404(Payment, ref=ref)
#     verified = payment.verify_payment()
#     if verified:
#         messages.success(request, 'verification successful')
#     else:
#         messages.error(request, 'verification failed')    
#     return redirect('initiate-payment')


# class CandidateListView(View):
#     template_name = 'candidate_list.html'

#     def get(self, request):
#         categories = VotingCategory.objects.all()
#         candidates_by_category = {}

#         for category in categories:
#             candidates = Candidate.objects.filter(voting_category=category)
#             candidates_by_category[category] = candidates

#         context = {
#             'candidates_by_category': candidates_by_category
#         }
#         return render(request, self.template_name, context=context)
    







