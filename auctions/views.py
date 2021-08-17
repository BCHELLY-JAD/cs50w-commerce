from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import CommentForm

from .models import User, Auction, Watchlist, Comments, Bids


def index(request):
    listings = Auction.objects.filter(is_active=True).order_by('-date')
    return render(request, "auctions/index.html", { 
        "listings" : listings
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        # checks if the username and password are correct 
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



def create(request): 
        if request.method == "POST": 
            user = request.user
            title = request.POST["title"]
            description = request.POST["description"]
            bid = request.POST["bid"]
            image = request.POST["image"]
            category = request.POST["category"]
            information = Auction.objects.create(title = title, description = description, bid = bid, image = image, category = category, owner = user)
            information.save()
            return HttpResponseRedirect(reverse("index"), { 
                "auction" : Auction.objects.all()
            })

        return render(request, "auctions/create.html")



def item(request, item_id):

    message = False
    messageprice = False
    error = False
    form = CommentForm()
    item = Auction.objects.get(pk=item_id)
    current_bid = item.bid
    latest_bid = item.bids.last()
    winner_bid = Bids.objects.filter(listing=item_id).last()
    list_comment = Comments.objects.filter(comment_list=item_id).all()
    result = False
    active = Auction.objects.get(id=item_id).is_active


    user = request.user
    if request.user.is_authenticated: 
        data = Watchlist.objects.filter(auction=item_id, user_list=request.user)
        if data: 
            result = True

    if request.method == "GET":
         
        active = Auction.objects.get(id=item_id).is_active
        if not active: 
            winner_bid = Bids.objects.filter(listing=item_id).last().bidder
            print(f'Checking 1: {winner_bid}')
            if request.user == winner_bid:
                message = "Congrats you have won the auction!!"
                print(f'Checking 2: {message}')

    elif request.method == "POST":


        active = Auction.objects.get(id=item_id).is_active
        if active: 
            new_bidding_price = request.POST["new_bidding_price"]
            user = request.user

            if latest_bid is None: 
                latest_bid = current_bid 
            else: 
                latest_bid = latest_bid.bid
                              
            
            if int(new_bidding_price) > latest_bid and int(new_bidding_price) > 0: 
                message = "Bidding placed successfully!"
                print(f'Checking 1: {message}')
                messageprice = f" The Current Bid is $ {new_bidding_price}"
                print(f'Checking 2: {messageprice}')
                bidding = Bids(listing = item, bid = new_bidding_price, bidder = user)
                bidding.save()
            else:
                error = "The Bid must be bigger than the current one"
                print(f'Checking 3: {error}')
            
            
                       
    return render(request, "auctions/item.html", { 
        'item' : item,
        'form' : form, 
        'active': active,
        'winner_bid': winner_bid,
        "list_comment" : list_comment,         
        "result" : result,
        'latest_bid' : latest_bid,
        'current_bid' : current_bid,
        'message' : message,
        'messageprice': messageprice,
        'error' : error,
        
          })
        
            


def addComment(request, item_id): 
    if request.method == "POST":
        form  = CommentForm(request.POST)
        user = request.user
        listing = Auction.objects.get(pk=item_id)
        if form.is_valid(): 
            text =  form.cleaned_data["text"]
            comment = Comments(comment = text, commenter = user, comment_list = listing)
            comment.save()
            print(request.POST['text'])
        else: 
            form  = CommentForm
        return HttpResponseRedirect(reverse("item", args=(item_id,)))
     


def this_category(request, name):
    categories = Auction.objects.filter(category=name)   
    return render(request, "auctions/thiscategory.html", { 
        "categories" : categories,
        "name" : name          
            })


def Categories(request):
    categories = request.POST.get("category")
    return render(request, "auctions/categories.html", { 
        "categories"  : categories
    })



def addwatchlist(request, item_id): 
    user= request.user
    item = Auction.objects.get(pk=item_id)
    insert = Watchlist(user_list=user , auction=item)
    print(f'Checking 1: {item.id}')
    insert.save()
    return HttpResponseRedirect(reverse("item" , args=(item_id,)))



def removewatchlist(request, item_id): 
    remove = Watchlist.objects.filter(auction=item_id)
    remove.delete()
    return HttpResponseRedirect(reverse("item" , args=(item_id,)))
 
def watch_list(request): 
    watchitems = Watchlist.objects.filter(user_list= request.user)
    print(f'Checking 1: {watchitems}')
    return render(request, "auctions/watchlist.html", { 
        "watchitems" : watchitems,
    })

def closelisting(request, item_id): 

    close = Auction.objects.filter(id=item_id).update(is_active=False)
    return HttpResponseRedirect(reverse('item', args=(item_id,)))
