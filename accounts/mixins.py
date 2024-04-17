from django.shortcuts import redirect
from django.urls import reverse


class TokenAuthRequiredMixin:
    def dispatch(self,request,*args,**kwargs):
        if not request.user.is_authenticated:
            sign_url = reverse('user-sign-in')
            return redirect(sign_url)
        return super().dispatch(request,*args,**kwargs)
