from django.urls import path
from . import views

app_name = 'myledger'
urlpatterns = [
    path('',views.home,name='home'),
    path('dologin',views.dologin,name='dologin'),
    path('dologout',views.dologout,name='dologout'),
    path('dosignup',views.dosignup,name='dosignup'),
    path('userpage/<int:userID>/',views.userpage,name='userpage'),
    path('makegrp/<int:userID>',views.makegrp,name='makegrp'),
    path('userpage/<int:userID>/grpPanel/<int:grpID>/',views.grpPanel,name='grpPanel'),
    path('userpage/<int:userID>/grpPanel/<int:grpID>/userSearch',views.searchUser,name='userSearch'),
    path('userpage/<int:userID>/grpPanel/<int:grpID>/addUser',views.addUser,name='addUser'),
    path('userpage/<int:userID>/grpPanel/<int:grpID>/makeTransaction',views.makeTransaction,name='makeTransaction'),
]