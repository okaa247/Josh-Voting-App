from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import secrets
from .paystack import Paystack
# Create your models here.



class Userprofile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=300, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    fullname = models.CharField(max_length=100, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile')
    address = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return str(self.user)

    
class VotingCategory(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, max_length=300,)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(VotingCategory, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.name    


class Candidate(models.Model):
    name = models.CharField(max_length=255)
    candidate_image = models.ImageField(upload_to='candidate_images/', null=True, blank=True)
    bio = models.CharField(max_length=300)
    voting_category = models.ForeignKey(VotingCategory, on_delete=models.CASCADE)
    votes = models.ManyToManyField(User, related_name='votes')
    votes_count = models.IntegerField(default=0)
    # votes = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'candidate')  # Ensures a user can vote for a candidate only once




class Payment(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
	amount = models.PositiveIntegerField()
	ref = models.CharField(max_length=200)
	email = models.EmailField()
	verified = models.BooleanField(default=False)
	date_created = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ('-date_created',)

	def __str__(self):
		return f"Payment: {self.amount}"

	def save(self, *args, **kwargs):
		while not self.ref:
			ref = secrets.token_urlsafe(50)
			object_with_similar_ref = Payment.objects.filter(ref=ref)
			if not object_with_similar_ref:
				self.ref = ref

		super().save(*args, **kwargs)
	
	def amount_value(self):
		return int(self.amount) * 100

	def verify_payment(self):
		paystack = Paystack()
		status, result = paystack.verify_payment(self.ref, self.amount)
		if status:
			if result['amount'] / 100 == self.amount:
				self.verified = True
			self.save()
		if self.verified:
			return True
		return False
	
 

# class Payment(models.Model):
#     amount = models.PositiveIntegerField()
#     ref = models.CharField(max_length=200)
#     email = models.EmailField()
#     verified = models.BooleanField(default=False)
#     date_created = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ('-date_created',)

#     def __str__(self) -> str:
#         return f"Payment: {self.amount}"

#     def save(self, *args, **kwargs) -> None:
#         while not self.ref:
#             ref = secrets.token_urlsafe(50)
#             object_with_similar_ref = Payment.objects.filter(ref=ref)
#             if not object_with_similar_ref:
#                 self.ref = ref
#         super().save(*args, **kwargs)


#     def amount_value(self) -> str:
#         return self.amount *100  

#     def verify_payment(self):
#         paystack = PayStack()
#         status, result = paystack.verify_payment(self.ref, self.amount)
#         if status:
#             if result['amount'] / 100 == self.amount:
#                 self.verified = True
#             self.save()
#         if self.verified:
#             return True
#         return False                    
