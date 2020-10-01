from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm

from .models import User, Listing, Bid, Comment


def index(request):

    # Display all active listings, if user is logged in.
    if not request.user.is_authenticated:
        return render(request, "auctions/index.html", {"message": "Please Log in to see active listings."})
    
    else:
        return render(request, "auctions/index.html", {"listing": Listing.objects.all()})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

# Detailed Listing Page
@login_required
def listing(request, list_id):

    class BidForm(ModelForm):
        class Meta:
            model = Bid
            fields = ["bid"]

    class CommentForm(ModelForm):
        class Meta:
            model = Comment
            fields = ["text"]

    # Make new Bid. Must be higher than previous one.
    if request.method == "POST" and "bidtry" in request.POST:
        current_bid = Listing.objects.get(pk=list_id).bids.latest().bid
        new_bid = int(request.POST["bid"])
        
        if current_bid >= new_bid:
            print(f"{new_bid} is lower than {current_bid}")
            
            return render(request, "auctions/listing.html", {"listing": Listing.objects.get(pk=list_id), 
    "comments": Comment.objects.filter(listings=list_id), "form": BidForm(request.POST), "message": "New bid must be higher than the previous bid",
    "commentform": CommentForm()})
        else:
            updatebid = Bid(user=request.user, listing=Listing(list_id), bid=new_bid)
            updatebid.save()
            return render(request, "auctions/listing.html", {"listing": Listing.objects.get(pk=list_id), 
    "comments": Comment.objects.filter(listings=list_id), "form": BidForm(), "message": "Success!", "commentform": CommentForm()})

    # Functionality to add comments
    elif request.method == "POST":
        newcomment = Comment(user=request.user, text=request.POST["text"], listings=Listing(list_id))
        newcomment.save()
        return render(request, "auctions/listing.html", {"listing": Listing.objects.get(pk=list_id), 
    "comments": Comment.objects.filter(listings=list_id), "form": BidForm(), "commentmessage": "Success!", "commentform": CommentForm()})

    # Standard Get request display.
    else:
        return render(request, "auctions/listing.html", {"listing": Listing.objects.get(pk=list_id), 
    "comments": Comment.objects.filter(listings=list_id), "form": BidForm(), "commentform": CommentForm()})
