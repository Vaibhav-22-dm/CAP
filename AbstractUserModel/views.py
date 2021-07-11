from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse 
from .utils import token_generator
from django.views.generic import View
from .utils import generate_ref_code
from django.template.loader import render_to_string

def index(request):
    leaderBoard = MyUser.objects.filter(is_superuser=False).order_by('rank')
    return render(request, 'AbstractUserModel/index.html', {'leaderBoard':leaderBoard})
 
def register(request):
    flag = False
    form = UserRegistrationForm()
    if request.method == 'POST':
        form = UserRegistrationForm(data = request.POST, files = request.FILES)
        email1 = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        try:
            user1 = MyUser.objects.get(email=email1)
            if user1 is not None:
                flag = True
                error = "There is already a user with this email id"
                return render(request, 'AbstractUserModel/register.html', {'form':form, 'error':error, 'flag':flag })
        except:
            if form.is_valid():
                form.save()
                # path_to_view
                    # - getting domain we are on
                    # - relative url to verification
                    # - encode uid
                    # - token
                user = MyUser.objects.order_by('-id')[0]
                last_user = MyUser.objects.order_by('-rank')[0]
                user.is_active = False
                user.rank = last_user.rank + 1
                user.save()
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                domain = get_current_site(request).domain
                link = reverse('activate', kwargs={'uidb64':uidb64, 'token':token_generator.make_token(user)})
                activate_url = 'http://' + domain + link
                email_subject = 'Activate your account'
                email_body = 'Hi!' + user.first_name + 'Please use this link to verify your account\n'+ activate_url
                #EmailMessage is a class responsible for creating the email message itself. 
                email = EmailMessage(
                    email_subject, #email subject
                    email_body, #email body
                    'registrations@ecell-iitkgp.org', #email id from which we want to send mails
                    [user.email] #email id to whom we want to send the email
                )

                email.send(fail_silently=False)
                # messages.success(request,'Account successfully created')
                return redirect('register')
            else:
                if password1 != password2:
                    flag = True
                    error = "Both the passwords don't match"
                    return render(request, 'AbstractUserModel/register.html', {'form':form, 'error':error, 'flag':flag })
    return render(request, 'AbstractUserModel/register.html', {'form':form, 'flag':flag})

def profile(request):
    profile = request.user
    return render(request, 'AbstractUserModel/profile.html', {'profile':profile})

def loginPage(request):
    flag = False 
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            error_msg = ""
            try:
                user = MyUser.objects.get(email=email)
                flag = True
                if user.is_active:
                    error_msg = "Password is incorrect"
                else:
                    error_msg = "Please verify your email first by visiting link given in verification mail."
                
            except:
                flag = True
                error_msg = "No such email-id is registered"
            return render(request, 'AbstractUserModel/login.html', {'error':error_msg, 'flag':flag})
    return render(request, 'AbstractUserModel/login.html')
    
def logoutPage(request):
    logout(request)
    return redirect('index')

def activate(request, uidb64, token):
    uid = force_text(urlsafe_base64_decode(uidb64))
    user = MyUser.objects.get(pk=uid)
    
    # user is activated if token from link is correct
    if user is not None and token_generator.check_token(user, token):
        user.is_active=True
        user.code = str(generate_ref_code())
        print(user.code)
        user.save()
        return redirect('loginPage')
    # else error is returned
    else:
        return redirect('register')

def register_customer(request):
    flag = 0
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        code = request.POST['code']
        try:
            ambassador = MyUser.objects.get(code=code) #Queries the ambassador with whose code the customer is registered
            print(ambassador)
            count = ambassador.count #sQuering the count of the ambassador
            print(count)
            count = count + 1 #Increasing the count of the ambassador
            print(count)
            ambassador.count = count  #updating the count of the ambassador
            curr_rank = ambassador.rank #storing the rank in a new variavle by the name curr_rank
            curr_count = count ##storing the count in a new variavle by the name curr_count

            list_user = MyUser.objects.filter(is_superuser=False).order_by('rank') #Quering the list of ambassador in ascending order of their ranks
            i = curr_rank - 2 #Declaring and initialising i to the first ambassador just above the current ambassador in the leader board
            print(i)
            while i >= 0: #Looping through the 'list_user' list
                if list_user[i].count < curr_count: #If the count of (i+1)th ambassador is less than the count of the current ambassador then swap the rank of the two ambassadors
                    print(list_user[i].rank)
                    temp = list_user[i].rank
                    print(list_user[i].email)
                    user2 = MyUser.objects.get(email=list_user[i].email)
                    print(user2)
                    # list_user[i].rank = curr_rank
                    user2.rank = curr_rank
                    user2.save() #Save the ith ambassador
                    print(user2.rank)
                    curr_rank = temp
                    print(curr_rank)
                    print(list_user[i].rank)
                    i = i - 1 #Updating i for the next iteration
                else:
                    break
                    
            print(curr_rank)
            ambassador.rank = curr_rank  #Udating the rank of the current ambassador    
            ambassador.save() 
            print(ambassador.rank)
            customer = Customer.objects.create(name=name, email=email, code=code, ambassador=ambassador)
            success_msg = "You have successfully registered! Thank you"
            flag = 1
            return render(request, 'AbstractUserModel/customer.html', {'success_msg':success_msg, 'flag':flag})
        except:
            error_msg = "The referral code is invalid"
            return render(request, 'AbstractUserModel/customer.html', {'error_msg':error_msg, 'flag':flag})
    return render(request, 'AbstractUserModel/customer.html')


#Example of ranking logic:
"""     list_user = {a, b, c, d, e}
        a.rank = 1, b.rank = 2, c.rank = 3, d.rank = 4, e.rank = 5
        a.count = 6, b.count = 4, c.count = 4, d.count = 4, e.count = 3

        supppose a customer is registered using the referral code of the user 'd'
        curr_rank = d.rank
        i = curr_rank - 2 = 2
        while i > 0 is true as i = 2
        1st iteration:
            list_user[i] is the (i+1)th user...i.e. 3rd ambassador i.e. 'c'
            As the count of c is 4 and count of d is 5 so the ranks of the two ambassadors will be exchanged
            c.rank = 4 and d.rank = 3
            i = i - 1 = 2 - 1 = 1
        2nd iteration:
            list_user[i] is the (i+1)th user...i.e. 2rd ambassador i.e. 'b'
            As the count of b is 4 and count of d is 5 so the ranks of the two ambassadors will be exchanged
            b.rank = 3 and d.rank = 2
            i = i - 1 = 1 - 1 = 0
        3rd iteration:
            list_user[i] is the (i+1)th user...i.e. 1st ambassador i.e. 'a'
            As the count of a is 6 and count of d is 5 so the if block is not executed rather else block is executed wherein we are breaking the loop keeping all the parameters unchanged
        Finally:
            a.rank = 1, b.rank = 3, c.rank = 4, d.rank = 2, e.rank = 5

"""


def forget(request):
    flag=False
    if request.method == 'POST':
      email2 = request.POST['email']
      print("Hi")
      try:
        user2=MyUser.objects.get(email=email2)
        print(user2)
        uidb64 = urlsafe_base64_encode(force_bytes(user2.pk))
        print(user2.pk)
        domain = get_current_site(request).domain
        print(domain)
        link = reverse('reset', kwargs={'uidb64':uidb64, 'token':token_generator.make_token(user2)})
        reset_url = 'http://' + domain + link
        email_subject = 'Reset your password'
        email_body = 'Hi!' + user2.first_name + 'Please use this link to reset your account password\n'+ reset_url
        email = EmailMessage(
                email_subject, #email subject
                email_body,#email body with html content
                'registrations@ecell-iitkgp.org', #email id from which we want to send mails
                [user2.email] #email id to whom we want to send the email
        )
        # email.content_subtype = "html"
        email.send(fail_silently=False)
        return redirect('loginPage')
      except:
        flag = True
        error = "There is no user with this email id"
        return render(request, 'AbstractUserModel/forgot.html', {'error':error, 'flag':flag })
    return render(request, 'AbstractUserModel/forgot.html')
  
def reset(request, uidb64, token):
    uid = force_text(urlsafe_base64_decode(uidb64))
    user = MyUser.objects.get(pk=uid)
    if user is not None and token_generator.check_token(user, token):
        email3 = user.email
        return render(request, 'AbstractUserModel/reset.html', {'email':email})
        # else error is returned
    else: 
            return redirect('forget')
    
def reset_pass(request):
    return render(request, 'AbstractUserModel/reset.html')



