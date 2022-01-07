from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm
from django.contrib.auth.decorators import login_required
from catalogue.models import Favorite_product, Product
import re
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.http import JsonResponse


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return account(request)
    else:
        if request.method == 'GET':
            return connexion(request)
        elif request.method == 'POST':
            return user_login(request)


def connexion(request, context={}):
    if request.user.is_authenticated:
        return account(request)

    context['form'] = UserForm()
    return render(request, 'user/login.html', context)


@login_required(login_url='/user/login/')
def account(request):
    context = {
        'page_title': request.user.username,
    }
    return render(request, 'user/account.html', context)


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password1']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            return connexion(request, context={'msgs': ['Compte inconnu.']})

    return redirect('home')


@login_required(login_url='/')
def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('home')


regex_remove_tag = re.compile(r'<[^>]*>')


def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    context = {'msgs': []}
    if request.method == 'GET':
        form = UserForm()
    else:
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('home')

        context['msgs'].append('Compte non créé.')

    for msg in form.errors.values():
        msg = regex_remove_tag.sub('', str(msg))
        context['msgs'].append(msg)

    context['form'] = form
    return render(request, 'user/register.html', context)


@login_required(login_url='/user/login/')
def favorite(request):
    context = {'msgs': []}
    user_search = request.GET.get('user_search')
    if not user_search:  # show Menu 1: product to substitute
        data = Favorite_product.objects.filter(user=request.user)

        db = set(product.product for product in data)

        if not db:
            context['msgs'].append("Aucun produit n'a encore été sauvegardé.")

        context['db'] = db
        context['in_favorite_menu'] = True
    else:  # show Menu 2: display substitute
        product_search = Product.objects.get(code=user_search)
        data = Favorite_product.objects.filter(
            user=request.user,
            product=user_search)

        context['product_id'] = product_search
        context['db'] = [
            product.substitute for product in data]

    context['page_title'] = 'Mes aliments'
    context['display_save_button'] = True

    return render(request, 'catalogue/result.html', context)


@login_required(login_url='/user/login/')
def delete_account(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            return JsonResponse({
                'text': 'Supprimer son compte est un choix définitif' +
                        ', veuillez le confirmer.'})

        request.user.delete()
    return redirect('home')


@login_required(login_url='/user/login/')
def change_email(request):
    context = {'msgs': []}
    if request.method != 'POST':
        context['msgs'].append('Erreur : E-mail non modifié !')
        return redirect('home')

    context['msgs'] = user_change_email(
                request.user,
                request.POST.get('user_new_email', ''),
                request.POST.get('user_new_email_confirm', ''))

    return render(request, 'user/account.html', context)


def user_change_email(user, new_email_1: str, new_email_2: str) -> str:
    msgs = []
    if not new_email_1 or not new_email_2:
        msgs.append('Tous les champs ne sont pas renseignés.')
    elif new_email_2 != new_email_1:
        msgs.append('Les deux adresses ne sont pas identiques.')
    elif new_email_1 == user.email:
        msgs.append("L'adresse email n'a pas été changée.")
    else:
        try:
            validate_email(new_email_1)
        except ValidationError as e:
            msgs.extend(e)
        else:
            user.email = new_email_1
            user.save()
            msgs.append("Changement effectué.")
    return msgs


@login_required(login_url='/user/login/')
def modify_account(request):
    context = {
        'page_title': request.user.username,
        'msgs': ['Modification de mes informations']
    }

    return render(request, 'user/modify_account.html', context)
