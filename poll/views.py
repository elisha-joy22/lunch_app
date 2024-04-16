from django.shortcuts import render,get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.http.response import HttpResponse,HttpResponseRedirect
from rest_framework.viewsets import ModelViewSet 
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from django.utils import timezone
import pytz
from datetime import datetime


from poll.forms import PollResponseForm,PollExtraCountForm
from poll.models import Poll,PollExtraCount
from poll.serializers import PollSerializer
from accounts.mixins import TokenAuthRequiredMixin
from utils.unique_images import superimpose_images

CONTEXT = settings.CONTEXT

class PollModelViewSet(TokenAuthRequiredMixin,ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

    def get_permissions(self):
        actions = ["destroy","update","create","list"]
        if self.action in actions:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


    @action(detail=False, methods=['get'])
    def active_polls(self, request):
        datetime_now_utc = timezone.now()
        active_polls = Poll.objects.active_polls().filter(start_date_time__lte=datetime_now_utc).order_by('-start_date_time')
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
            user_polled_status = poll.users.filter(id=request.user.id).exists()
            if user_polled_status==True:
                form.fields.get('response').initial = user_polled_status
            context["form"] = form
            context["poll"] = poll
            return render(request,"poll_form.html",context)
        
        elif request.method=="POST":
            form = PollResponseForm(request.POST)
            if form.is_valid():
                user_polled_status = poll.users.filter(id=request.user.id).exists()
                poll_response = form.cleaned_data['response']
                if user_polled_status==True and poll_response=="True":
                    messages.info(request,'You have already polled YES')
                    print("1")
                if user_polled_status==False and poll_response=="True":
                    poll.users.add(request.user)
                    messages.success(request,'You successfully polled YES')
                    print("2")
                elif user_polled_status==True and poll_response=="False":
                    messages.success(request,'Your poll was removed successfully')
                    a = poll.users.remove(request.user)
                    print("response",a)
                    print("3")
                elif user_polled_status==False and poll_response=="False":
                    messages.warning(request,"You haven't polled for the event event yet!")
                    print("4")
                return HttpResponseRedirect(f"{CONTEXT['basic_url']}polls/my_polls")
            context["error"] = "An error occured while submitting your response!"
            return render(request,"response.html",context)
        
    
    @action(detail=False, methods=['get','post','delete'])
    def poll_extra_count(self, request):
        poll_id = request.query_params.get('poll_id')
        poll = get_object_or_404(Poll,pk=poll_id)
        poll_extra_counts = poll.poll_extra_counts.all()
        print(poll_extra_counts)
        print("inside_poll_extra")
        context = CONTEXT
        if request.method=="GET":
            form = PollExtraCountForm()
            context["form"] = form
            context["poll"] = poll
            context["poll_extra_counts"] = poll_extra_counts
            context["user_id"] = request.user.id
            print("user",request.user)
            return render(request,"poll_extra_count.html",context)
            
        elif request.method=="POST":
            form = PollExtraCountForm(request.POST)
            if form.is_valid():
                print(0)
                poll_response = form.save(commit=False)
                poll_response.user_id = request.user.id
                poll_response.poll_id = poll.id
                poll_response.save()
                return HttpResponseRedirect(f"{CONTEXT['basic_url']}polls/poll_extra_count?poll_id={poll_id}")
 
            context["error"] = "An error occured while submitting your response!"
            return render(request,"response.html",context)
                    
    

    @action(detail=False, methods=['get','post'])
    def edit_poll_extra_count(self, request):
        poll_extra_count_id = request.query_params.get('id')
        poll_extra_count_instance = get_object_or_404(PollExtraCount,pk=poll_extra_count_id)
        poll_id = poll_extra_count_instance.poll_id
        print("inside_poll_edit_extra")
        context = CONTEXT
        if request.method=="GET":
            form = PollExtraCountForm(instance=poll_extra_count_instance)
            context['form'] = form
            context['poll'] = Poll.objects.get(id=poll_id)
            return render(request,"edit_poll_extra_count.html",context)
        elif request.method == "POST":
            form = PollExtraCountForm(data=request.POST, instance=poll_extra_count_instance)
            if form.is_valid():
                form.save()
                context["form"] = form
                print("user",request.user)
                return HttpResponseRedirect(f"{CONTEXT['basic_url']}polls/poll_extra_count?poll_id={poll_id}")
            context["error"] = "An error occured while submitting your response!"
            return render(request,"response.html",context)

    
    @action(detail=False, methods=['get','post'])
    def delete_poll_extra_count(self, request):
        poll_extra_count_id = request.query_params.get('id')
        poll_extra_count_instance = get_object_or_404(PollExtraCount,pk=poll_extra_count_id)
        print(poll_extra_count_instance.poll.id)

        if poll_extra_count_instance.user.id == request.user.id:
            context = CONTEXT
            if request.method=="GET":
                print(request.query_params)
                print(request.query_params.get('delete'))
                if request.query_params.get('delete')=='True':
                    print("hi")
                    deleted_count, _ = PollExtraCount.objects.filter(pk=poll_extra_count_id).delete()    
                    if deleted_count == 1:
                        print("deleted")
                        messages.success(request,'Extra count was Successfully deleted.')
                        return HttpResponseRedirect(f"{CONTEXT['basic_url']}polls/poll_extra_count?poll_id={poll_extra_count_instance.poll.id}")
                    else:
                        messages.error(request, 'Deleting extra count failed!')
                        return HttpResponseRedirect(f"{CONTEXT['basic_url']}polls/poll_extra_count?poll_id={poll_extra_count_instance.poll.id}")
                context['extra_count'] = poll_extra_count_instance
                context['poll_id'] = poll_extra_count_instance.poll.id
                return render(request,"delete_extra_count.html",context)
        messages.error(request,'Unauthorised Request!')
        return HttpResponse("Unauthorised!!")
            





    @action(detail=False, methods=['get'])
    def my_polls(self,request):
        poll_ids = self.queryset.filter(users=request.user).values_list('id','poll_text','end_date_time','event_date_time','is_active').order_by('-start_date_time')
        context = CONTEXT
        context["poll_ids"] = poll_ids
        datetime_now_utc = timezone.now()
        timezone_kolkata = pytz.timezone('Asia/Kolkata')
        datetime_now_kolkata = datetime_now_utc.astimezone(timezone_kolkata)

        context["datetime_now"] = datetime_now_kolkata
        print("now", context["datetime_now"])
        
        return render(request, "my_polls.html", context)


    @action(detail=False, methods=['get'])
    def download_unique_image(self,request):
        poll_id = request.query_params.get('poll_id')
        poll = get_object_or_404(Poll,pk=poll_id)
        user_image = request.user.picture_url
        try:
            user_image = user_image.replace("_48.jpg", "_192.jpg")
        except:
            pass
        
        background_image = f"https://picsum.photos/id/{poll_id}/350/550"
        event_date = poll.event_date_time.strftime("%d/%m/%Y")
        
        image_data = superimpose_images(
                        background_url=background_image,
                        profile_pic_url=user_image,
                        text=event_date
                    )
        response = HttpResponse(image_data, content_type='image/jpeg')
        response['Content-Disposition'] = 'attachment; filename=f"unique_image_{event_date}.jpg"'
        return response