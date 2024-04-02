from django.shortcuts import render,get_object_or_404
from django.conf import settings
from django.http.response import HttpResponse,HttpResponseRedirect
from rest_framework.viewsets import ModelViewSet 
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from django.utils import timezone
import pytz


from poll.forms import PollResponseForm
from poll.models import Poll
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
        active_polls = Poll.objects.active_polls().order_by('-start_date_time')
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
                poll_response = form.cleaned_data['response']
                if poll_response=="True":
                    poll.users.add(request.user)
                elif poll_response=="False":
                    poll.users.remove(request.user)
                return HttpResponseRedirect(f"{CONTEXT['basic_url']}polls/my_polls")
            context["error"] = "An error occured while submitting your response!"
            return render(request,"response.html",context)


    @action(detail=False, methods=['get'])
    def my_polls(self,request):
        poll_ids = self.queryset.filter(users=request.user).values_list('id','end_date_time','event_date_time','is_active').order_by('-start_date_time')
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
        lunch_date = poll.event_date_time.strftime("%d/%m/%Y")
        
        image_data = superimpose_images(
                        background_url=background_image,
                        profile_pic_url=user_image,
                        text=lunch_date
                    )
        response = HttpResponse(image_data, content_type='image/jpeg')
        response['Content-Disposition'] = 'attachment; filename="superimposed_image.jpg"'
        return response