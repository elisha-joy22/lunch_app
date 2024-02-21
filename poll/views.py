from django.shortcuts import render,get_object_or_404

from rest_framework.viewsets import ModelViewSet 
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser

from poll.forms import PollResponseForm,CreatePollForm
from poll.models import Poll
from poll.serializers import PollSerializer


class PollModelViewSet(ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

    def get_permissions(self):
        actions = ["destroy","update","create","list","polled_users"]
        if self.action in actions:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

    def create(request):
        if request.method == 'POST':
            form = CreatePollForm(request.POST)
            message = "An error occured while creating the poll"
            if form.is_valid():
                poll = form.save()
                message = f"Poll created successfully with poll id - {poll.pk}"
                return render(request,'request.html',{"message":message})
            return render(request,'request.html',{"error":message})
        else:
            form = CreatePollForm()
        return render(request, 'create_poll.html', {'form': form})



    @action(detail=False, methods=['get'])
    def active_polls(self, request):
        active_polls = self.queryset.filter(is_active=True)
        return render(request, 'active_polls.html', {'active_polls': active_polls})


    @action(detail=False, methods=['get','post'])
    def poll(self, request):
        poll_id = request.query_params.get('poll_id')
        poll = get_object_or_404(Poll,pk=poll_id)
        
        if request.method=="GET":
            form = PollResponseForm()
            return render(request,"poll_form.html",{"form":form,"poll":poll})
        
        elif request.method=="POST":
            form = PollResponseForm(request.POST)
            message = "An error occured while submitting your response!"
            if form.is_valid():
                poll_response = form.cleaned_data['response']
                if poll_response=="True":
                    poll.users.add(request.user)
                    message = "Your polled yes successfully"
                elif poll_response=="False":
                    poll.users.remove(request.user)
                    message = "Your polled no successfully"
                return render(request,"poll_response.html",{"message":message})
            return render(request,"poll_response.html",{"error":message})


    @action(detail=False, methods=['get'])
    def polled_users(self,request):
        poll_id = request.query_params.get('poll_id')
        poll = get_object_or_404(Poll,pk=poll_id)
        polled_users = poll.users.all()        
        return render(request, "polled_users.html", {"poll":poll,"users":polled_users})  


    @action(detail=False, methods=['get'])
    def my_polls(self,request):
        poll_ids = self.queryset.filter(users=request.user).values_list('id','event_date_time')
        url = f"https://0a85-103-141-56-118.ngrok-free.app/polls/"
        return render(request, "my_polls.html", {"url":url,"poll_ids":poll_ids})
