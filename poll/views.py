from django.shortcuts import render,get_object_or_404
from django.conf import settings
from rest_framework.viewsets import ModelViewSet 
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser

from poll.forms import PollResponseForm,CreatePollForm
from poll.models import Poll
from poll.serializers import PollSerializer
from accounts.mixins import TokenAuthRequiredMixin


CONTEXT = settings.CONTEXT

class PollModelViewSet(TokenAuthRequiredMixin,ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

    def get_permissions(self):
        actions = ["destroy","update","create","list","polled_users"]
        if self.action in actions:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

    def create(request):
        context = CONTEXT
        if request.method == 'POST':
            form = CreatePollForm(request.POST)
            if form.is_valid():
                poll = form.save()
                context["message"] = f"Poll created successfully with poll id - {poll.pk}"
                return render(request,'request.html',context)
            context["error"] = "An error occured while creating the poll"
            return render(request,'request.html',context)
        else:
            form = CreatePollForm()
            context["form"] = form
        return render(request, 'create_poll.html', context)


    @action(detail=False, methods=['get'])
    def active_polls(self, request):
        active_polls = self.queryset.filter(is_active=True)
        context = CONTEXT
        context["active_polls"] = active_polls
        return render(request, 'active_polls.html', context)


    @action(detail=False, methods=['get','post'])
    def poll(self, request):
        poll_id = request.query_params.get('poll_id')
        poll = get_object_or_404(Poll,pk=poll_id)
        
        context = CONTEXT
        if request.method=="GET":
            form = PollResponseForm()
            context["form"] = form
            context["poll"] = poll
            return render(request,"poll_form.html",context)
        
        elif request.method=="POST":
            form = PollResponseForm(request.POST)
            if form.is_valid():
                poll_response = form.cleaned_data['response']
                if poll_response=="True":
                    poll.users.add(request.user)
                    message = "Your polled yes successfully"
                elif poll_response=="False":
                    poll.users.remove(request.user)
                    message = "Your polled no successfully"
                context["message"] = message
                return render(request,"response.html",context)
            context["error"] = "An error occured while submitting your response!"
            return render(request,"response.html",context)


    @action(detail=False, methods=['get'])
    def polled_users(self,request):
        poll_id = request.query_params.get('poll_id')
        poll = get_object_or_404(Poll,pk=poll_id)
        polled_users = poll.users.all()        
        context = CONTEXT
        context["poll"] = poll
        context["users"] = polled_users
        return render(request, "polled_users.html", context)  


    @action(detail=False, methods=['get'])
    def my_polls(self,request):
        poll_ids = self.queryset.filter(users=request.user).values_list('id','event_date_time')
        context = CONTEXT
        context["poll_ids"] = poll_ids
        return render(request, "my_polls.html", context)
