import tempfile

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import EmailMessage
from django.template.loader import get_template

from strecklista.forms import heddaHopperForm
from .forms import LoginForm, QuoteForm, BulkTransactionForm, ReturnTransactionForm, TransactionDateForm, RegisterRequestForm
from .models import Transaction, RegisterRequest

from strecklista.models import Group, PriceGroup, Product, ProductCategory, Quote
from django.forms import formset_factory
from EmailUser.models import MyUser
from EmailUser.forms import UpdateUserForm, UpdateUserImageForm

from password_reset_email.forms import RequestKeyForm, ResetPasswordForm

from password_reset_email.models import PasswordResetEmail

from django.core.management import call_command

from subprocess import Popen, PIPE

import os

@login_required
def index(request):
    return render(request, 'strecklista/index.html', get_index_context(request))


@login_required
def tabbed_index(request):
    return render(request, 'strecklista/tabbed_index.html', get_index_context(request))


def get_index_context(request):
    class UserRepresentation:
        def __init__(self, user):
            self.display_name = user.display_name()
            self.id = user.id
            self.group = user.group
            self.alcohol = user.bloodAlcohol()

    u_list = MyUser.objects.order_by('id')
    user_list = [UserRepresentation(user) for user in u_list]

    group_list = Group.objects.order_by('-sortingWeight')
    priceGroup_list = PriceGroup.objects.order_by('sortingWeight')
    product_list = Product.objects.filter(is_active = True).order_by('sortingWeight')
    productCategory_list = ProductCategory.objects.order_by('sortingWeight')
    quote = Quote.objects.order_by('?').first()
    # Set a threshold to only display the transactions from the last X minutes (could be set to "hours" or "days"
    # if you want)
    time_threshold = datetime.now() - timedelta(minutes=30)
    transactions = Transaction.objects.filter(admintransaction=False, timestamp__gte=time_threshold, returned=False).all().order_by(
    #transactions = Transaction.objects.filter(admintransaction=False, returned=False).all().order_by(
        "-timestamp")[:10]

    print(len(transactions))

    return {
        'current_user': UserRepresentation(request.user),
        'user_list': user_list,
        'group_list': group_list,
        'price_group_list': priceGroup_list,
        'drink_categories':
            [generate_drinks(category, product_list)
                for category in productCategory_list],
        'transactions': transactions,
        'quote': quote,
    }

# Generate a more convenient datastructure.
def generate_drinks(category, drinks):
    return {
        'name': category.name,
        'products':
            [generate_drink(drink)
                for drink in drinks if drink.productCategory == category],
    }

def generate_drink(drink):
    return {
        'url': drink.url if hasattr(drink, 'url') else None,
        'name': drink.name,
        'category': drink.priceGroup.name,
        'price': drink.priceGroup.defaultPrice,
    }

def register(request):

    if request.method== 'POST':
        form = RegisterRequestForm(request.POST)
        if form.is_valid():
            rrq = RegisterRequest()
            rrq.first_name = form.cleaned_data['first_name']
            rrq.last_name = form.cleaned_data['last_name']
            rrq.email = form.cleaned_data['email']
            if form.cleaned_data['message']:
                rrq.message = form.cleaned_data['message']
            else:
                rrq.message = ""
            rrq.save()
            return redirect("/")
        else:
            return render(request, 'strecklista/registeruser.html', context={'form' : form, 'error_message' : form.errors})

    return render(request, 'strecklista/registeruser.html', context={'form' : RegisterRequestForm()})


def login(request):
    if request.method != 'POST':
        return render(request, 'strecklista/login.html', {
            'action': request.get_full_path(),
            'form': LoginForm(),
            'error_message': None,
        })

    error_message = None
    form = LoginForm(request.POST)

    if form.is_valid():
        user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'])
        if user is None:
            error_message = "Your username and/or password were incorrect"
        elif user.is_active:
            auth_login(request, user)
            return redirect(request.GET.get('next', '/'))
        else:
            error_message = "Your account is not active. Please contact the admin"
    else:
        error_message = "Internal Error: Bad Form (contact the admin)"

    return render(request, 'strecklista/login.html', {
        'action': request.get_full_path(),
        'form': form,
        'error_message': error_message,
    })


@login_required
def detail(request, user_id):
    user = get_object_or_404(MyUser, pk=user_id)
    return render(request, 'strecklista/profile.html', {
        'person': user,
    })


@login_required
def transaction(request):
    if "userId" in request.POST.keys() and "priceGroup" in request.POST.keys():

        pg = PriceGroup.objects.filter(id=request.POST.get("priceGroup")).first()

        user = MyUser.objects.filter(id=request.POST.get("userId")).first()
        balanceBefore = user.balance
        transaction = Transaction()
        transaction.message = pg.name
        transaction.user = user
        transaction.amount = pg.calculatePrice(user.balance)
        user.balance -= transaction.amount
        user.save()
        transaction.save()

        if balanceBefore >= 0 and user.balance < 0:#This transaction made the user go to negative balance
            call_command("email_low_balance_user", "%i"%(user.id))


        return HttpResponse("success")
    return HttpResponse("failed")


@login_required
def profile(request, user_id):
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, request.FILES)
        if form.is_valid():
            user = MyUser.objects.filter(id=user_id).first()
            if request.user == user or request.user.is_admin:
                if form.cleaned_data['nickname'] != user.nickname:
                    user.nickname = form.cleaned_data['nickname']
                if form.cleaned_data['phone_number'] and form.cleaned_data['phone_number'] != user.phone_number:
                    user.phone_number = form.cleaned_data['phone_number']
                if form.cleaned_data['email'] and form.cleaned_data['email'] != user.email:
                    user.email = form.cleaned_data['email']
                if form.cleaned_data['avatar']:
                    user.avatar = form.cleaned_data['avatar']
                if form.cleaned_data['weight']:
                    user.weight = form.cleaned_data['weight']
                if form.cleaned_data['password']:
                    if not user.check_password(form.cleaned_data['password']):
                        user.set_password(form.cleaned_data['password'])
                if form.cleaned_data['y_chromosome']:
                    if form.cleaned_data['y_chromosome'] == "none":
                        user.y_chromosome = None
                    if form.cleaned_data['y_chromosome'] == "y":
                        user.y_chromosome = True
                    if form.cleaned_data['y_chromosome'] == "not_y":
                        user.y_chromosome = False
                user.save()
                return redirect("/profile/%s" %(user_id))
            else:
                return HttpResponseForbidden()

    if not MyUser.objects.filter(id=user_id).exists():
        return HttpResponse("user not found")

    user = MyUser.objects.filter(id=user_id).first()
    can_edit = request.user == user or request.user.is_admin

    context = {
        'user': user,
        'can_edit': can_edit,
        'imageForm': UpdateUserImageForm,
    }

    if request.GET.get('edit', False) and can_edit:
        context['edit_form'] = UpdateUserForm()

    if user == request.user or request.user.is_admin:
        all_history = request.GET.get('all_history', False)

        context['all_history'] = all_history
        transactions = Transaction.objects.filter(
            user=user, returned=False).all().order_by("-timestamp")

        if not all_history:
            transactions = transactions[:10]

        context['transactions'] = transactions
        context['balance'] = user.balance

    return render(request, 'strecklista/profile.html', context)


@user_passes_test(lambda u: u.is_admin)
@login_required
def bulkTransactions(request):
    state = ""
    only_active_singers = False
    if request.GET.get('active', False):
        user_list = MyUser.objects.filter(active_singer = True).order_by('group')
        only_active_singers = True
    else:
        user_list = MyUser.objects.order_by('group')
    if request.method == 'POST':
        formset = formset_factory(BulkTransactionForm)
        formset = formset(request.POST)
        if formset.is_valid():
            state = "success"
            for form in formset:
                if form.cleaned_data['amount'] != 0 and MyUser.objects.filter(id=form.cleaned_data['user_id']).exists():
                    t = Transaction()
                    t.amount = form.cleaned_data['amount']
                    t.user = MyUser.objects.filter(id=form.cleaned_data['user_id']).first()
                    t.message = form.cleaned_data['message']
                    t.admintransaction = True
                    t.save()

                    t.user.balance += t.amount
                    t.user.save()

        else:
            for i in range(len(user_list)):
                person = user_list[i]
                formset[i].fields['amount'].label = "%s %s" % (person.user.first_name, person.user.last_name)
            state = "failed. Make sure all the fields are filled in"
            context = {
                'formset': formset,
                'state': state,
                'only_active': only_active_singers,
            }

            return render(request, "strecklista/bulkTransaction.html", context)

    formset = formset_factory(BulkTransactionForm, extra=0)
    # TODO: remove need for [:-1]
    formset = formset(initial=[{'user_id': user.id} for user in user_list])
    for i in range(len(user_list)):
        user = user_list[i]
        formset[i].fields['amount'].label = "%s %s" % (user.first_name, user.last_name)

    context = {
        'formset': formset,
        'state': state,
        'only_active' : only_active_singers,
    }
    return render(request, "strecklista/bulkTransaction.html", context)


@login_required
def submitQuote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)

        if form.is_valid():
            q = Quote()
            q.text = form.cleaned_data['text']
            q.who = form.cleaned_data['name']
            q.submittedBy = request.user

            q.save()
            return HttpResponse("success")

            # else:
            #    print (form.errors)

    return HttpResponse("Misslyckades av någon anledning. Kan vara en kopia.")


@login_required
def quote(request):
    quote_list = Quote.objects.order_by('-id')
    form = QuoteForm()
    context = {
        'form': form,
        'quote_list': quote_list,
    }

    return render(request, 'strecklista/quotes.html', context)


@login_required
def product(request):
    product_list = Product.objects.filter(is_active=True).order_by('sortingWeight')
    productCategory_list = ProductCategory.objects.order_by('sortingWeight')
    priceGroup_list = PriceGroup.objects.all().order_by('sortingWeight')

    context = {
        'product_list': product_list,
        'product_category_list': productCategory_list,
        'price_group_list': priceGroup_list,
    }

    return render(request, 'strecklista/products.html', context)


def returnTransaction(request):
    if request.method == 'POST':
        form = ReturnTransactionForm(request.POST)
        if form.is_valid():
            if not request.user.is_admin:  # regular users can only return a transaction whithin a time limit
                time_threshold = datetime.now() - timedelta(hours=1)
                transaction = Transaction.objects.filter(admintransaction=False, timestamp__gte=time_threshold,
                                                         id=form.cleaned_data['transaction_id']).first()
            else:  # admins are allowed to return any transaction
                transaction = Transaction.objects.filter(id=form.cleaned_data['transaction_id']).first()

            transaction.ret()
            return HttpResponse("success")

    return HttpResponse("failed")


def transactionHistory(request):
    startDate = datetime.now()-timedelta(days=60)
    endDate = datetime.now()

    if request.method == 'POST':
        form = TransactionDateForm(request.POST)
        if form.is_valid():
            startDate = form.cleaned_data['start_date']
            endDate = form.cleaned_data['end_date']

    transaction_list = Transaction.objects.all().filter(timestamp__lte=endDate, timestamp__gte=startDate).order_by("-timestamp")
    context = {
        'transaction_list'  :   transaction_list,
        'dateForm'          :   TransactionDateForm(),
    }

    return render(request, 'strecklista/transactionHistory.html', context)


def requestPasswordReset(request):
    context = {}

    if request.method == 'POST':
        form = RequestKeyForm(request.POST)
        if form.is_valid() and MyUser.objects.filter(email__iexact=form.cleaned_data['email']).exists():
            pre = PasswordResetEmail()
            pre.key = pre.random_string()
            pre.user = MyUser.objects.filter(email=form.cleaned_data['email']).first()
            pre.save()
            pre.email_user()
        else:
            print("failed :(")


    else:
        context['resetForm'] = RequestKeyForm()

    return render(request, 'strecklista/requestReset.html', context)


def resetPassword(request):
    context = {}
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            print("form is valid")
            if PasswordResetEmail.objects.filter(key=form.cleaned_data["key"], used=False).exists() and form.cleaned_data["password1"] == form.cleaned_data["password2"]:
                pre = PasswordResetEmail.objects.filter(key=form.cleaned_data["key"]).first()
                pre.reset_password(form.cleaned_data['password1'])
                context['state'] = "reset done"
                return redirect("/login/")
            else:
                context['state'] = "Please check all fields"
                context['resetForm'] = ResetPasswordForm()
        else:
            print("form is not valid")
            context['state'] = "Please check all fields"
            context['resetForm'] = ResetPasswordForm()

    else:
        if request.GET.get('key', False):
            context['key'] = request.GET.get('key', False)
        context['resetForm'] = ResetPasswordForm()

    return render(request, 'strecklista/resetPassword.html', context)


@login_required
def heddaHopper(request):
    form = heddaHopperForm()
    context = {
        'form': form,
    }

    if request.method == 'POST':
        form = heddaHopperForm(request.POST)
        if form.is_valid():

            email_subject = "Ny topphemlig information!"
            email_body = ""
            if form.cleaned_data["where"]:
                email_body += "Var?: {}\n\n".format(form.cleaned_data["where"])
            if form.cleaned_data["when"]:
                email_body += "När?: {}\n\n".format(form.cleaned_data["when"])
            if form.cleaned_data["what"]:
                email_body += "Vad?: {}\n\n".format(form.cleaned_data["what"])

            EmailMessage(email_subject, email_body, "strecklistan@gmail.com", ["heddahopperktk@gmail.com"]).send()

        else:
            print("failed :(")
            print (form.errors)

    return render(request, 'strecklista/heddaHopper.html', context)


@login_required
def lista_as_pdf(request):
    if request.GET.get("active", False):
        userlist = MyUser.objects.filter(active_singer=True).all().order_by('first_name')
    else:
        userlist = MyUser.objects.all().order_by('first_name')

    grouplist = []

    # Filter to only get used groups
    for user in userlist:
        if user.group is not None and user.group not in grouplist:
            grouplist.append(user.group)

    grouplist.sort(key=lambda x: x.sortingWeight, reverse=True)

    context = {
        'user_list' : userlist,
        'group_list' : grouplist,
    }
    template = get_template('strecklista/lista_latex_template.tex')
    rendered_tpl = template.render(context).encode('utf-8')
    # Python3 only. For python2 check out the docs!
    with tempfile.TemporaryDirectory() as tempdir:
        # Create subprocess, supress output with PIPE and
        # run latex twice to generate the TOC properly.
        # Finally read the generated pdf.
        for i in range(2):
            process = Popen(
                ['pdflatex', '-output-directory', tempdir],
                stdin=PIPE,
                stdout=PIPE,
            )
            process.communicate(rendered_tpl)
        with open(os.path.join(tempdir, 'texput.pdf'), 'rb') as f:
            pdf = f.read()
    r = HttpResponse(content_type='application/pdf')
    # r['Content-Disposition'] = 'attachment; filename=texput.pdf'
    r.write(pdf)
    return r


@user_passes_test(lambda u: u.is_admin)
@login_required
def admin_tools(request):
    context = {}
    if "balanceEmail" in request.POST.keys():
        # Send mail to all the users
        print("yay")
        context["balanceEmailStatus"] = "emails sent"
        call_command('email_low_balance')

    registerRequests = RegisterRequest.objects.all().filter(active=True)
    for r in registerRequests:
        print("%s %s %i" %(r.first_name, r.last_name, r.id))
    context['registerRequests'] = registerRequests

    return render(request, 'strecklista/admintools.html', context)

@user_passes_test(lambda u: u.is_admin)
@login_required
def acceptRegisterRequest(request):
    if request.method == 'GET':
        if 'id' in request.GET.keys():
            rq = RegisterRequest.objects.all().filter(id=request.GET.get('id'), active=True).first()
            if rq:
                try:
                    rq.registerUser()
                    rq.active = False
                    rq.save()

                    pre = PasswordResetEmail()
                    pre.key = pre.random_string()
                    pre.user = MyUser.objects.filter(email=rq.email).first()
                    pre.save()
                    pre.email_new_user()

                    return HttpResponse("Success")
                except:
                    return HttpResponse("Failed - probably a duplicate email address")


    return HttpResponse("Failed - Send a valid ID to register")


@user_passes_test(lambda u: u.is_admin)
@login_required
def denyRegisterRequest(request):
    if request.method == 'GET':
        if 'id' in request.GET.keys():
            rq = RegisterRequest.objects.all().filter(id=request.GET.get('id'), active=True).first()
            if rq:
                try:
                    rq.active = False
                    rq.save()
                    return HttpResponse("Success")
                except:
                    return HttpResponse("Failed")


    return HttpResponse("Failed - Send a valid ID")


@login_required
def updateAvatar(request):
    if request.method == 'POST':
        form = UpdateUserImageForm(request.POST, request.FILES)
        print("post request")
        if form.is_valid():
            user = MyUser.objects.filter(id = form.cleaned_data["id"]).first()
            user.avatar = form.cleaned_data['avatar']
            user.save()
            return redirect("/profile/%i" %user.id)
        else:
            print("form is not valid")
            print(form.errors)

    return HttpResponse("Failed :/")
