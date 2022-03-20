from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from imgtry4.settings import LOGIN_URL

from myledger.models import MyGroup, Tally, Transaction

# Create your views here.

def home(request):
    return redirect("accounts/login")

# Authentication system:
from django.contrib.auth import authenticate, login, logout

def dologin(request):
    if request.method== 'POST':
        usrname = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=usrname, password=password)
        if user is not None:
            login(request, user)
            theuser = User.objects.get(username=usrname)
            # Redirect to a success page:
            return redirect(reverse('myledger:userpage',kwargs={'userID':theuser.id}))
        else:
            # define an error message:
            err_message='Incorrect username or password'
            # redirect to login page with error message:
            return redirect(reverse('hpage',kwargs={'err_message':err_message}))
    else:
        return redirect(reverse('hpage'))

def dologout(request):
    logout(request)
    # Redirect to a success page:
    return redirect(reverse('hpage'))

from .forms import SignUpForm

def dosignup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect(reverse('hpage'))
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
@login_required
def userpage(request,userID):
    theuser = User.objects.get(id=userID)
    hisgroups = theuser.mygroup_set.all()
    # transactions in which user is the lender:
    histransacsl = list(Transaction.objects.filter(lender=theuser))
    # transactions in which user is the borrower:
    histransacsb = list(Transaction.objects.filter(borrower=theuser))
    # combining both lists
    histransacs = histransacsb + histransacsl
    # sorting the list according to transactionDate:
    histransacs.sort(key=lambda x: x.transactionDate)
    # making a dictionary with keys as groups and values as the user's tally for that group:
    grp_dict={}
    i=0
    for agroup in hisgroups:
        grp_dict[agroup]=theuser.tally_set.values('balance')[i]['balance']
        i+=1
    context={'theuser':theuser,'hisgroups':hisgroups,'histransacs':histransacs,'dict':grp_dict}
    return render(request,'myledger/userpage.html',context)

@login_required
def makegrp(request,userID):
    grpName = request.POST.get('groupName')
    grp = MyGroup(groupName=grpName)
    grp.save()
    user = User.objects.get(id=userID)
    grp.members.add(user)
    return grpPanel(request,user.id,grp.id)

@login_required
def grpPanel(request,userID,grpID):
    grp = MyGroup.objects.get(id=grpID)
    theuser = User.objects.get(id=userID)
    hisgroups = theuser.mygroup_set.all()
    grp_dict={}
    i=0
    for agroup in hisgroups:
        grp_dict[agroup]=theuser.tally_set.values('balance')[i]['balance']
        i+=1
    normal_dict = normalized_dict(grp,theuser)
    transacList = Transaction.objects.filter(group=grp)
    context={'theuser':theuser,'hisgroups':hisgroups,'grp':grp,'dict':grp_dict,'normal_dict':normal_dict,'transacList':transacList}
    return render(request,'myledger/grpPanel.html',context)

@login_required
def searchUser(request,userID,grpID):
    grp = MyGroup.objects.get(id=grpID)
    usr = User.objects.get(id=userID)
    qtext= request.GET.get('username')
    suchUsers=User.objects.filter(username__startswith=qtext)
    suchUsers=suchUsers.exclude(username=usr.username)
    context={'suchUsers':suchUsers,'grp':grp,'usr':usr}
    return render(request,'myledger/userList.html',context)

@login_required
def addUser(request,userID,grpID):
    grp= MyGroup.objects.get(id=grpID)
    allusers = User.objects.all()
    for auser in allusers:
        if request.POST.get(str(auser.id))=="clicked":
            grp.members.add(auser)
    grp.save()
    return grpPanel(request,userID,grp.id)

@login_required
def makeTransaction(request,userID,grpID):
    grp= MyGroup.objects.get(id=grpID)
    # person1 is the user:
    person1 = User.objects.get(id=userID)
    # person2 is the other person involved in the transaction:
    person2 = grp.members.get(id=request.POST.get("otherPerson"))
    if person1==person2:
        return grpPanel(request,userID,grp.id)
    amount = int(request.POST.get("amount"))
    # ower tells which person is the lender:
    ower = int(request.POST.get("owedByWho"))
    lable=str(request.POST.get("lable"))
    # tally (object) of person1 with the group grp:
    tally1 = Tally.objects.get(user_id=person1.id,group_id=grp.id)
    # tally (object) of person2 with the group grp:
    tally2 = Tally.objects.get(user_id=person2.id,group_id=grp.id)
    # if ower=1 this means person1 is the lender:
    if ower==1:
        tally1.balance+=amount
        tally2.balance-=amount
        transac = Transaction(group=grp,lender=person1,borrower=person2,amount=amount,lable=lable)
        transac.save()
    # if ower=2 this means person2 is the lender:
    elif ower==2:
        tally1.balance-=amount
        tally2.balance+=amount
        transac = Transaction(group=grp,lender=person2,borrower=person1,amount=amount,lable=lable)
        transac.save()
    tally1.save()
    tally2.save()
    person1.save()
    person2.save()
    grp.save()
    return grpPanel(request,userID,grp.id)

#normalization code 
#it returns a dictionary with keys as user objects in the group grp (except the user usr) and values as the debt/excess of the user usr with other users
#wrote this in one go and now I can't explain what is going on in this :,-( 
def normalized_dict(grp,usr):
    itsMembers = grp.members.all()
    tally_list = []
    i=0
    ans_dict={}
    member_list = list(itsMembers)
    for memberObj in member_list :
        ans_dict[memberObj]=0
    del ans_dict[usr]
    for amember in itsMembers:
        tally_list.append(Tally.objects.get(user_id=amember.id,group_id=grp.id).balance)
        if amember==usr:
            usr_index = i
        i+=1
    temp_dict={index:tally_list[index] for index in range(i)}
    order_list=[]
    sorted_dict = dict(sorted(temp_dict.items(), key=lambda item: item[1], reverse=True))
    order_list=list(sorted_dict.keys())
    usr_order = order_list.index(usr_index)
    l = len(order_list)
    if tally_list[usr_index]<0:
        sum=0
        for t in range(1,l-usr_order):
            sum += tally_list[order_list[l-t]]
        p=0
        while sum<=0:
            sum += tally_list[order_list[p]]
            p+=1
        remainderr = sum
        req_list = order_list[p-1:usr_order]
        usr_money = tally_list[usr_index]
        tally_list[req_list[0]]=remainderr
        q=0
        while usr_money<0:
            temp2=usr_money
            usr_money += tally_list[req_list[q]]
            if usr_money<0:
                ans_dict[member_list[req_list[q]]]=-tally_list[req_list[q]]
            else:
                ans_dict[member_list[req_list[q]]]=temp2
            q+=1

    elif tally_list[usr_index]>0:
        sum=0
        for t in range(0,usr_order):
            sum += tally_list[order_list[t]]
        p=l-1
        while sum>=0:
            sum += tally_list[order_list[p]]
            p-=1
        remainderr=sum
        req_list = order_list[usr_order+1:p+2]
        usr_money = tally_list[usr_index]
        tally_list[req_list[-1]]=remainderr
        q=-1
        while usr_money>0:
            temp2=usr_money
            usr_money += tally_list[req_list[q]]
            if usr_money>0:
                ans_dict[member_list[req_list[q]]]=-tally_list[req_list[q]]
            else:
                ans_dict[member_list[req_list[q]]]=temp2
            q-=1

    return ans_dict

#channel i oauth
# I have registered my app on channel.in but it is not approved till now (March 20, 2022 - 21:45:33). But I will keep this code here (incase app is approved later)
import requests
client_id='Rpd9gbaDjlrLiFcF7yKKsY14f9DUT6OmNhwzFNuJ'
client_secret='g2mqhQDtuGLoAqFmMNs4ebsEWrXMDmvOWWCFg0dee6OB0yVxkAXVf50dOs20ywazwGG8JXaqzQv2O5dbPk17Mjf1kJnPbNRVeRkQFg5Qi0nHvROnKlrUmhbIlt5KWKPJ'
redirect_uri='http://127.0.0.1:8000/oauth2/login/redirect'
auth_url = 'https://channeli.in/oauth/authorise/?client_id='+client_id

def authToChanneli(request):
    return redirect(auth_url)

def redirector(request):
    auth_code = request.GET.get('code')
    final_data = exchanger(auth_code)
    username= final_data.student.enrolmentNumber
    full_name = final_data.person.fullName
    firstName = full_name.split()[0]
    lastName = full_name.split()[-1]
    suchuser = User.objects.filter(username=username)
    if suchuser is not None:
        login(request,suchuser)
        return userpage(request,suchuser.id)
    else:
        suchuser = User.objects.create_user(username=username,first_name=firstName,last_name=lastName)
        login(request,suchuser)
        return userpage(request,suchuser.id)

def exchanger(auth_code):
    final_data={}
    data={
        "client_id":client_id,
        "client_secret":client_secret,
        "grant_type":"authorization_code",
        "code":auth_code,
        "redirect_uri":redirect_uri,
    }
    headers={
        'Content-Type':'application/x-www-form-urlencoded'
    }
    response= requests.post('https://channeli.in/open_auth/token',data=data,headers=headers)
    if response.status_code==200:
        credentials = response.json()
        access_token = credentials['access_token']
        headers={
            "Authorization": "Bearer %s" %access_token
        }
        response = requests.get('https://channeli.in/open_auth/get_user_data',headers=headers)
        if response.status_code==200:
            final_data = response.json
    return final_data

