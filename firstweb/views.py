from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView,UpdateView
from . import forms
from .models import CoffeehouseUser,Friend
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.http import HttpResponse
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.

#def index(request):
 #   return render(request,'firstweb/ls.html')

#class SignUp(CreateView):
 #   form_class=forms.UserCreateForm
  #  success_url=reverse_lazy('login')
   # template_name='firstweb/signup.html'


#class UP(CreateView):
 #   form_class=forms.UserProfileForm
  #  success_url=reverse_lazy('login')
   # template_name='firstweb/signup.html'


def SignUp(request):
    if request.method == 'POST':
        form = forms.UserCreateForm(request.POST)
        if form.is_valid():
            #form.save()
            user = form.save()
            # default to non-active
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('firstweb/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })

            email_message = EmailMessage(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [user.email]
            )

            email_message.send()

            #user.email_user(subject, message)

            #messages.success(request, ('Please Confirm your email to complete registration.'))

            return HttpResponse('check ur email for verification mail')
    else:
        form = forms.UserCreateForm()
    return render(request, 'firstweb/signup.html', {
        'form': form
    })


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CoffeehouseUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CoffeehouseUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # return redirect('home')
        return redirect('login')
    else:
        return HttpResponse('Activation link is invalid!')  

@login_required
def search_status(request):

    if request.method == "GET":
        search_text = request.GET['search_text']
        if search_text is not None and search_text != u"":
            search_text = request.GET['search_text']
            statuss = CoffeehouseUser.objects.filter(clgname__contains = search_text).values('clgname')
            p=[c for c in statuss]
            #print(p[0]['clgname'])
            print(p)
            pp=[p[d]['clgname'] for d in range(len(p))]
            u=request.user
            un=u.clgname
            print(pp)
            if pp.count(un)==1:
                pp.remove(un)
            print(set(pp))
            statuss_list=list(set(pp))
        elif search_text=='':
            statuss=['']
            statuss_list= list(statuss)
        else:
            statuss = []
            statuss_list= list(statuss)

        return render(request, 'firstweb/ajax_search.html', {'statuss_list':statuss_list})

#class Update(UpdateView):
 #   model=CoffeehouseUser
  #  fields=('age')
   # success_url=reverse_lazy('test')
    #template_name='firstweb/update.html'

@login_required
def profile(request):
    if request.method=="POST":
        u_form=forms.UserUpdateForm(request.POST,instance=request.user)
        p_form=forms.PicUpdateForm(request.POST,request.FILES,instance=request.user)
        if u_form.is_valid and p_form.is_valid :
            u_form.save()
            p_form.save()
            messages.success(request,'Your account has been updated!')
            return redirect('/profile/')
    else:
        u_form=forms.UserUpdateForm(instance=request.user)
        p_form=forms.PicUpdateForm(instance=request.user)
    context={'u_form':u_form,'p_form':p_form}
    return render(request,'firstweb/profile.html',context)

@login_required
def Stud(request,status='Default'):


    studlist1=CoffeehouseUser.objects.filter(clgname__exact = status).values('username','first_name','age','college','clgcourse','clgyear','image','id')
    #studlist=[c for c in studlist1]
    studlist=[]
    u=request.user
    un=u.username
    for c in studlist1:
        if c['username']!=un:
            studlist.append(c)
    #studlist3=[studlist2[d]['username'] for d in range(len(studlist2))]
    #t=[studlist[f]['username'] for f in range(len(studlist))]
    #u=['@'+i for i in t]
    #print(u)
    #print([j.image for j in u])

    return render(request,'firstweb/stud.html',context={"status": status,"studlist": studlist,})

    #return HttpResponse(status)

@login_required
def chat(request):
    try:
        friend_list=Friend.objects.get(current_user=request.user)
        friends_list=friend_list.users.all()
    except:
        friends_list=[]
    #print(friends_list)
    context={'friends_list':friends_list}
    return render(request,'firstweb/chat.html',context)

@login_required
def change_friends(request,username):
    
    new_friend=CoffeehouseUser.objects.get(username=username)
    print(username,new_friend)
    Friend.make_friend(request.user,new_friend)

    return redirect('/test')

@login_required
def messages(request,f):

    print(f)

    return render(request,'firstweb/messages.html',{'f':f})

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.edit import FormMixin

from django.views.generic import DetailView, ListView

from .forms import ComposeForm
from .models import Thread, ChatMessage

@login_required
class InboxView(LoginRequiredMixin, ListView):
    template_name = 'firstweb/chat.html'
    def get_queryset(self):
        return Thread.objects.by_user(self.request.user)

class ThreadView(LoginRequiredMixin, FormMixin, DetailView):
    template_name = 'firstweb/messages.html'
    form_class = ComposeForm
    success_url = './'

    def get_queryset(self):
        return Thread.objects.by_user(self.request.user)

    def get_object(self):
        other_username  = self.kwargs.get("username")
        obj, created    = Thread.objects.get_or_new(self.request.user, other_username)
        if obj == None:
            raise Http404
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        thread = self.get_object()
        user = self.request.user
        message = form.cleaned_data.get("message")
        ChatMessage.objects.create(user=user, thread=thread, message=message)
        return super().form_valid(form)




