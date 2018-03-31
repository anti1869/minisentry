from django.shortcuts import render

from sunhead.blog.models import Entry, Category
from sunhead.content.models import Tree

from bhom import __version__
from bhom.commodities.models import Commodity
from bhom.currencies.models import Currency


def mainpage(request):
    """
    View for the mainpage
    """
    tree_object = Tree.objects.get(id=1)
    savings_object = Category.objects.get(id=1)
    loans_object = Category.objects.get(id=2)
    markets_object = Category.objects.get(id=3)
    currencies_object = Category.objects.get(id=4)

    last_savings = Entry.objects.filter(category=savings_object).order_by("-created")[0:3]
    last_loans = Entry.objects.filter(category=loans_object).order_by("-created")[0:3]
    last_markets = Entry.objects.filter(category=markets_object).order_by("-created")[0:3]
    last_currencies = Entry.objects.filter(category=currencies_object).order_by("-created")[0:3]

    quotes = (
        Currency.objects
        .filter(ticker__in=["USD", "EUR"])
        .values("ticker", "price", "price_deviation")
        .order_by("-ticker")
    )

    commodities = (
        Commodity.objects
        .filter(slug__in=["neft-brent", "zoloto"])
        .values("slug", "title", "price", "price_deviation")
        .order_by("slug")
    )

    c = {
        "savings_object": savings_object,
        "last_savings": last_savings,
        "loans_object": loans_object,
        "last_loans": last_loans,
        "tree_object": tree_object,
        "last_markets": last_markets,
        "markets_object": markets_object,
        "last_currencies": last_currencies,
        "currencies_object": currencies_object,
        "mainpage": True,
        "version": __version__,
        "quotes": quotes,
        "commodities": commodities,
    }
    return render(request, "mainpage.html", c)
