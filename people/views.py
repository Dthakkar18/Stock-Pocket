from django.contrib import auth # not using this right now
from django.db.models.fields import NullBooleanField # not using this right now 
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, response # not using this right now
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin # not using this right now
from django.contrib.auth.decorators import login_required
from django.views import generic
from .models import Stock, Agent, User
from .forms import CustomUserCreationForm, loginForm
from .stock_function import generalInfo, showRevenue, showGrossProfit, purchase, summary, similar_tickers, similar_names, similar_prices, current_change, dividendPercentage

# Create your views here.

# made the signup view in class form
class SignupView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm 

    def get_success_url(self):
        return reverse("login")


def landing_page(request):
    if request.method == "POST":
        print(request.POST)
        if request.POST.get("toSignup"):
            return redirect("/signup")
        else:
            return redirect("/login")

    return render(request, "people/landing_page.html")


@login_required
def home_page(request, pk):
    agent = Agent.objects.get(id=pk)
    stocks = Stock.objects.filter(agent_id=pk)
    amountIn = []
    tickers = []
    shares = []
    company = []
    for i in range(len(stocks)):
        amountIn.append(round(stocks[i].shares * stocks[i].avg_share_price,2))
        tickers.append(stocks[i].company_ticker.upper())
        shares.append(stocks[i].shares)
        company.append(stocks[i].company_name)
    dividendAmounts = dividendPercentage(tickers, company, amountIn)
    current_prices = current_change(tickers, shares, amountIn)
    context = {
        "agent": agent,
        "stocks": stocks,
        "amountIn": amountIn, 
        "tickers": tickers,
        "current_prices": current_prices,
        "dividendAmounts": dividendAmounts,
        "pk": pk
    }
    return render(request, "people/home_page.html", context)


def login_view(request):
    form = loginForm
    if request.method == "POST":
        form = loginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                id = User.objects.get(username=username)
                return redirect("/people/" + str(id.id))
            else:
                return redirect("/login")
    context = {
        'form': form
    }
    return render(request, "registration/login.html", context)



@login_required(login_url='/login')
def stock_add_delete(request, pk):
    stocks = Stock.objects.filter(agent_id=pk)
    if request.method == "POST":
        print(request.POST)
        if request.POST.get("addStock"): # if request from adding form
            if len(request.POST.get("name")) != 0 and len(request.POST.get("ticker")) != 0 and len(request.POST.get("shares")) != 0 and len(request.POST.get("avgPrice")) != 0:
                print("all items were given")
                company_name = request.POST.get("name")
                company_ticker = request.POST.get("ticker")
                shares = request.POST.get("shares")
                avg_share_price = request.POST.get("avgPrice")
                 # check if there is same stock in database
                testing = stocks.filter(company_ticker=company_ticker)
                # if not then continue with creating 
                if len(testing) == 0: 
                    Stock.objects.create(
                        company_name = company_name,
                        company_ticker = company_ticker,
                        shares = shares,
                        avg_share_price = avg_share_price,
                        agent_id = pk
                    )
                    print("The stock has been added")
                    return redirect("/people/" + str(pk)) 
                else:
                    print("stock in database already")
            else:
                print("not all items here")

        elif request.POST.get("deleteStock"): # if request from deleting form
            if len(request.POST.get("ticker")) != 0:
                print("got all contents")
                company_ticker = request.POST.get("ticker")
                deleteStock = Stock.objects.get(agent_id=pk, company_ticker=company_ticker)
                deleteStock.delete()
                print("Stock has been deleted")
                return redirect("/people/" + str(pk))
            else:
                print("not all content provided")

    context = {
        "pk": pk,
        'stocks': stocks
    }
    return render(request, "people/stock_add_delete.html", context)


@login_required(login_url='/login')
def stock_update(request, pk):
    stocks = Stock.objects.filter(agent_id=pk)
    if request.method == "POST":
        print(request.POST)
        if request.POST.get("updateStock"): # check that request is from correct button
            if len(request.POST.get("ticker")) != 0 and len(request.POST.get("shares")) != 0 and len(request.POST.get("avgPrice")) != 0:
                print("all items were given")
                company_ticker = request.POST.get("ticker")
                shares = request.POST.get("shares")
                avg_share_price = request.POST.get("avgPrice")
                updatingStock = Stock.objects.get(agent_id=pk, company_ticker=company_ticker)
                updatingStock.shares = shares
                updatingStock.avg_share_price = avg_share_price
                updatingStock.save()
                print("The stock has been updated")
                return redirect("/people/" + str(pk)) 
            else:
                print("not all items given")
 
    context = {
        "pk": pk,
        'stocks': stocks
    }
    return render(request, "people/stock_update.html", context)


@login_required(login_url='/login')
def stock_detail(request, pk):
    stocks = Stock.objects.filter(agent_id=pk)
    if request.method == "POST":
        print(request.POST)
        if request.POST.get("detailStock"): # check that request is from corrent button
            if len(request.POST.get("ticker")) != 0 and len(request.POST.get("name")) != 0: #making sure its vaild form
                print("all items were given")
                global company_ticker, company_name
                company_ticker = request.POST.get("ticker")
                company_name = request.POST.get("name")
                return redirect("/people/" + str(pk) + "/detail/view/")
            else:
                print("not all items given")
            
    context = {
        'pk': pk,
        'stocks': stocks
    }
    return render(request, "people/stock_detail.html", context)


@login_required(login_url='/login')
def detail_view(request, pk):
    gen_info = generalInfo(company_ticker)
    revenues = showRevenue(company_name, company_ticker)
    profits = showGrossProfit(company_name, company_ticker)
    should_buy = purchase(company_ticker)
    comp_info = summary(company_ticker)
    suggestion_ticker = similar_tickers(company_ticker)
    suggestion_names = similar_names(company_ticker)
    suggestion_prices = similar_prices(company_ticker)
    context = {
        'gen_info': gen_info,
        'revenues': revenues,
        'profits': profits,
        'buy_num': should_buy[0],
        'buy_word': should_buy[1],
        'sector': comp_info[0],
        'industry': comp_info[1],
        'employees': comp_info[2],
        'summary': comp_info[3],
        'suggestion_tickers': suggestion_ticker,
        'suggestion_names': suggestion_names,
        'suggestion_prices': suggestion_prices,
        'pk': pk,
        "company_name": company_name
    }
    return render(request, "people/stock_detail_view.html", context)

