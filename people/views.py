from django.contrib import auth # not using this right now
from django.db.models.fields import NullBooleanField # not using this right now 
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, response # not using this right now
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin # not using this right now
from django.contrib.auth.decorators import login_required
from django.views import generic
from .models import Stock, Agent, User
from .forms import CustomUserCreationForm, loginForm
from .stock_function import generalInfo, showRevenue, showGrossProfit, summary, similar_tickers, similar_names, similar_prices, current_change, dividendPercentage, dividendGrowth

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

    # the log out request
    if request.method == 'POST':
        print(request.POST)
        if request.POST.get("logout"): # if logout button clicked
            logout(request)
            return redirect("/") # redirects to landing page

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
    if request.method == 'POST':
        print(request.POST)
        if request.POST.get("login"): # if login button pressed
            if len(request.POST.get("username")) != 0 and len(request.POST.get("password")) != 0:
                print("all sections filled")
                username = request.POST.get("username")
                password = request.POST.get("password")
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    id = User.objects.get(username=username)
                    return redirect("/people/" + str(id.id))
                else:
                    return redirect("/login")

    context = {
    }
    return render(request, "registration/login.html", context)



@login_required
def stock_add_delete(request, pk):

    # the log out request
    if request.method == 'POST':
        print(request.POST)
        if request.POST.get("logout"): # if logout button clicked
            logout(request)
            return redirect("/") # redirects to landing page

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


@login_required
def stock_update(request, pk):

    # the log out request
    if request.method == 'POST':
        print(request.POST)
        if request.POST.get("logout"): # if logout button clicked
            logout(request)
            return redirect("/") # redirects to landing page

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


@login_required
def stock_detail(request, pk):

    # the log out request
    if request.method == 'POST':
        print(request.POST)
        if request.POST.get("logout"): # if logout button clicked
            logout(request)
            return redirect("/") # redirects to landing page

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


@login_required
def detail_view(request, pk):
    global company_ticker, company_name # inroder to reasign

    # previous stocks suggestions (inorder to get the name) 
    suggestion_ticker = similar_tickers(company_ticker)
    suggestion_names = similar_names(company_ticker)
    suggestion_prices = similar_prices(company_ticker)

    if request.method == "POST":
        print(request.POST)
        if request.POST.get("suggestion"): # if the button of the stock was clicked
            print(request.POST.get("suggestion"))

            new_ticker = request.POST.get("suggestion") # ticker that was clicked on
            index = suggestion_ticker.index(new_ticker) # so I can get the name 
            new_name = suggestion_names[index] # company name of the ticker that was clicked on
            
            gen_info = generalInfo(new_ticker)
            gen_info_names = gen_info.get('names')
            gen_info_values = gen_info.get('values')

            yearAndAmountRev = showRevenue(new_name, new_ticker)
            revenueYears = yearAndAmountRev.get("years")
            revenueAmounts = yearAndAmountRev.get("revenues")

            yearAndAmountProf = showGrossProfit(new_name, new_ticker)
            profitYears = yearAndAmountProf.get("years")
            profitAmounts = yearAndAmountProf.get("profits")

            yearAndAmountDiv = dividendGrowth(new_ticker)
            dividendYears = yearAndAmountDiv.get("years")
            dividendAmounts = yearAndAmountDiv.get("amounts")

            comp_info = summary(new_ticker)

            suggestion_ticker = similar_tickers(new_ticker)
            suggestion_names = similar_names(new_ticker)
            suggestion_prices = similar_prices(new_ticker)

            company_ticker = new_ticker # reasigned for next clicked stock button
            company_name = new_name # reasigned for next clicked stock button

            context = {
                'gen_info_names': gen_info_names,
                'gen_info_values': gen_info_values,
                'revenueYears': revenueYears,
                'revenueAmounts': revenueAmounts,
                'profitYears': profitYears,
                'profitAmounts': profitAmounts,
                'sector': comp_info[0],
                'industry': comp_info[1],
                'employees': comp_info[2],
                'summary': comp_info[3],
                'suggestion_tickers': suggestion_ticker,
                'suggestion_names': suggestion_names,
                'suggestion_prices': suggestion_prices,
                'dividendYears': dividendYears,
                'dividendAmounts': dividendAmounts,
                'pk': pk,
                "company_name": new_name
            }
            return render(request, "people/stock_detail_view.html", context)

    else: # if not a post and just a redirect from above function view
        gen_info = generalInfo(company_ticker)
        gen_info_names = gen_info.get('names')
        gen_info_values = gen_info.get('values')

        yearAndAmountRev = showRevenue(company_name, company_ticker)
        revenueYears = yearAndAmountRev.get("years")
        revenueAmounts = yearAndAmountRev.get("revenues")

        yearAndAmountProf = showGrossProfit(company_name, company_ticker)
        profitYears = yearAndAmountProf.get("years")
        profitAmounts = yearAndAmountProf.get("profits")

        yearAndAmountDiv = dividendGrowth(company_ticker)
        dividendYears = yearAndAmountDiv.get("years")
        dividendAmounts = yearAndAmountDiv.get("amounts")

        comp_info = summary(company_ticker)

        context = {
            'gen_info_names': gen_info_names,
            'gen_info_values': gen_info_values,
            'revenueYears': revenueYears,
            'revenueAmounts': revenueAmounts,
            'profitYears': profitYears,
            'profitAmounts': profitAmounts,
            'sector': comp_info[0],
            'industry': comp_info[1],
            'employees': comp_info[2],
            'summary': comp_info[3],
            'suggestion_tickers': suggestion_ticker,
            'suggestion_names': suggestion_names,
            'suggestion_prices': suggestion_prices,
            'dividendYears': dividendYears,
            'dividendAmounts': dividendAmounts,
            'pk': pk,
            "company_name": company_name
        }
        return render(request, "people/stock_detail_view.html", context)

