from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    categoryName = models.CharField(max_length=50)

    def __str__(self):
        return self.categoryName

    
class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userBid")
    bid = models.DecimalField(max_digits=10, decimal_places=2)
    # Ajoutez d'autres champs si nécessaire pour Bid

    def __str__(self):
        return f"{self.bid} by {self.user.username}"

        

class Listing(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    imageUrl = models.CharField(max_length=1000)
    price = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True, related_name="listed_item_price")
    isActive = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    category = models.ForeignKey(Category, on_delete=models.CASCADE,blank=True, null=True, related_name="category")
    watchlist = models.ManyToManyField(User, blank=True, related_name="watching_listings")

    def __str__(self):
        return self.title
    
class Comments(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True, related_name="userComment")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE,blank=True, null=True, related_name="listingComment")
    message = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.author} comment on {self.listing}"
    
