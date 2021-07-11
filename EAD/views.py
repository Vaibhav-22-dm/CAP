from django.shortcuts import render
from .models import *
from AbstractUserModel.models import MyUser
# Create your views here.
def index_ead(request):
    flag = 0
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        college = request.POST['college']
        code = request.POST['code']
        try:
            ambassador = MyUser.objects.using('default').get(code=code) #Queries the ambassador with whose code the customer is registered
            print(ambassador)
            count = ambassador.count #sQuering the count of the ambassador
            print(count)
            count = count + 1 #Increasing the count of the ambassador
            print(count)
            ambassador.count = count  #updating the count of the ambassador
            curr_rank = ambassador.rank #storing the rank in a new variavle by the name curr_rank
            curr_count = count ##storing the count in a new variavle by the name curr_count

            list_user = MyUser.objects.using('default').filter(is_superuser=False).order_by('rank') #Quering the list of ambassador in ascending order of their ranks
            i = curr_rank - 2 #Declaring and initialising i to the first ambassador just above the current ambassador in the leader board
            print(i)
            while i >= 0: #Looping through the 'list_user' list
                if list_user[i].count < curr_count: #If the count of (i+1)th ambassador is less than the count of the current ambassador then swap the rank of the two ambassadors
                    print(list_user[i].rank)
                    temp = list_user[i].rank
                    print(list_user[i].email)
                    user2 = MyUser.objects.using('default').get(email=list_user[i].email)
                    print(user2)
                    list_user[i].rank = curr_rank
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
            print("check")
            customer = ead_Participant(name=name, email=email, code=code, ambassador=ambassador, college=college)
            
            print("check")
            # customer.save(using='EAD_db')
            success_msg = "You have successfully registered! Thank you"
            flag = 1
            return render(request, 'EAD/index.html', {'success_msg':success_msg, 'flag':flag})
        except:
            error_msg = "The referral code is invalid"
            return render(request, 'EAD/index.html', {'error_msg':error_msg, 'flag':flag})
    return render(request, 'EAD/index.html')