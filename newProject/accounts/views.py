from django.core.exceptions import ObjectDoesNotExist
from newProject.accounts.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse

import bcrypt

#Response

created = {"status": "201"}
conflict = {"status": "409", 'detail': ''}

@csrf_exempt
def submit_signup(request):
    if request.POST:
        email = request.POST.get('email')
        password = encrypt_password(request.POST.get('password'))
        name = request.POST.get('name')
        sobrenome = request.POST.get('sobrenome')

        try:
            emailExist = User.objects.get(email=email)
        except ObjectDoesNotExist:
            emailExist = None

        if emailExist is None:
            User.objects.create(email=email, password=password, name=name, sobrenome=sobrenome)
            return JsonResponse(created)
        else:
            return JsonResponse(conflict)

@csrf_exempt
def submit_login(request):
    if request.POST:
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            loginExist = User.objects.get(email=email)
        except ObjectDoesNotExist:
                loginExist = None

        if loginExist is not None:

            user = User.objects.filter(email=email).values()

            myHash = user[0]['password']

            if check_password(password, myHash):
                newUser = {'name': '', 'sobrenome': ''}
                newUser['name'] = user[0]['name']
                newUser['sobrenome'] = user[0]['sobrenome']
                return JsonResponse(newUser)
            else:
                conflict['detail'] = 'password ou login errado.'
                return JsonResponse(conflict)
        else:
            conflict['detail'] = 'usuário inexistente.'
            return JsonResponse(conflict)


def encrypt_password(password): #Ajeitar tamanho do saltRounds
    salt = bcrypt.gensalt(14)
    myhash = bcrypt.hashpw(password.encode('utf-8'), salt)

    return myhash.decode('utf-8')

def check_password(password, myHash):
    mboolean = bcrypt.checkpw(password.encode('utf-8'), myHash.encode('utf-8'))

    return mboolean