from django.db import models
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image

class UserManager(BaseUserManager):
    def create_user(self, email, username, password, alias=None):
        if not email:
            raise ValueError("ENTER AN EMAIL BUDDY")
        if not username:
            raise ValueError("I KNOW YOU HAVE A NAME")
        if not password:
            raise ValueError("PASSWORD?!?!?!? HELLO??")
        if not alias:
            alias = username
        
        user = self.model(
             email = self.normalize_email(email),
             username = username,
             alias = alias)
        user.set_password(password)
        user.save()
        return user
        
    def create_superuser(self, email, username, password, alias=None):
        user=self.create_user(email, username, password, alias)
        user.is_staff()
        user.is_superuser = True
        user.save()
        return user


#class UserProfile(models.Model):
 #   user=models.OneToOneField(User,on_delete=models.CASCADE)
  #  age=models.IntegerField()

   # def __str__(self):
    #    return self.user.name
    


#class User(auth.models.User,auth.models.PermissionsMixin):

 #   def __str__(self):
  #      return "@{}".format(self.username)

class CoffeehouseUser(AbstractUser):
    age = models.PositiveSmallIntegerField(blank=True,null=True)
    college = models.BooleanField(default=True)
    email=models.EmailField(unique=True)
    clgname=models.CharField(max_length=100)
    clgcourse=models.CharField(max_length=100)
    clgyear=models.CharField(max_length=100)
    image=models.ImageField(upload_to='profile_pics',default='default.jpg')
    USERNAME_FIELD=('email')
    REQUIRED_FIELDS=['username']

    def __str__(self):
        return "{}".format(self.username)


    def save(self,*args, **kwargs):

        super().save(*args, **kwargs)

        img=Image.open(self.image.path)

        if img.height>300 or img.height>300:
            op=(250,200)
            img.thumbnail(op)
            img.save(self.image.path)

class Friend(models.Model):

    users=models.ManyToManyField(CoffeehouseUser)
    current_user= models.ForeignKey(CoffeehouseUser,related_name='owner',null=True,on_delete=models.CASCADE)

    @classmethod
    def make_friend(cls,current_user,new_friend):
        friend,created= cls.objects.get_or_create(current_user=current_user)
        otherfriend=cls.objects.get_or_create(current_user=new_friend)
        friend.users.add(new_friend)
        otherfriend[0].users.add(current_user)
        print(otherfriend[0])
        print(type(friend))
        print(type(otherfriend[0]))

    @classmethod
    def lose_friend(cls,current_user,new_friend):
        friend,created= cls.objects.get_or_create(current_user=current_user)
        friend.users.remove(new_friend)
    


#class Profile(models.Model):
 #   user=models.OneToOneField(CoffeehouseUser,on_delete=models.CASCADE)
  #  image=models.ImageField(upload_to='profile_pics',default='default.jpg')

   # def __str__(self):
    #    return "{}".format(self.user)

from django.conf import settings
from django.db.models import Q


class ThreadManager(models.Manager):
    def by_user(self, user):
        qlookup = Q(first=user) | Q(second=user)
        qlookup2 = Q(first=user) & Q(second=user)
        qs = self.get_queryset().filter(qlookup).exclude(qlookup2).distinct()
        return qs

    def get_or_new(self, user, other_username): # get_or_create
        username = user.username
        if username == other_username:
            return None
        qlookup1 = Q(first__username=username) & Q(second__username=other_username)
        qlookup2 = Q(first__username=other_username) & Q(second__username=username)
        qs = self.get_queryset().filter(qlookup1 | qlookup2).distinct()
        if qs.count() == 1:
            return qs.first(), False
        elif qs.count() > 1:
            return qs.order_by('timestamp').first(), False
        else:
            Klass = user.__class__
            user2 = Klass.objects.get(username=other_username)
            if user != user2:
                obj = self.model(
                        first=user, 
                        second=user2
                    )
                obj.save()
                return obj, True
            return None, False


class Thread(models.Model):
    first        = models.ForeignKey(CoffeehouseUser, on_delete=models.CASCADE, related_name='chat_thread_first')
    second       = models.ForeignKey(CoffeehouseUser, on_delete=models.CASCADE, related_name='chat_thread_second')
    updated      = models.DateTimeField(auto_now=True)
    timestamp    = models.DateTimeField(auto_now_add=True)
    
    objects      = ThreadManager()

    @property
    def room_group_name(self):
        return f'chat_{self.id}'

    def broadcast(self, msg=None):
        if msg is not None:
            broadcast_msg_to_chat(msg, group_name=self.room_group_name, user='admin')
            return True
        return False


class ChatMessage(models.Model):
    thread      = models.ForeignKey(Thread, null=True, blank=True, on_delete=models.SET_NULL)
    user        = models.ForeignKey(CoffeehouseUser, verbose_name='sender', on_delete=models.CASCADE)
    message     = models.TextField()
    timestamp   = models.DateTimeField(auto_now_add=True)


