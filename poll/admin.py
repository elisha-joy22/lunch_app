from django.contrib import admin
from django.http import HttpResponse
from poll.forms import ScheduledPollForm,CreatePollForm
from django.template.loader import render_to_string
from django.db.models import Sum
from weasyprint import HTML

from poll.models import Poll,ScheduledPoll,PollUser,PollExtraCount

#from utils.timezone_converter import convert_utc_to_kolkata_time

class PollAdmin(admin.ModelAdmin):
    list_display = ( 'id','event_date_time', 'poll_text', 'poll_count','extra_count','total_count')
    fields = ['start_date_time','end_date_time','event_date_time', 'poll_text','is_active']
    readonly_fields = ('poll_count',)
    actions = ['generate_pdf']

    form = CreatePollForm
    
    poll_count_var = None
    extra_count_var = None
    
    def poll_count(self,obj):
        count = Poll.objects.get_poll_count(obj.id) or 0
        self.p_count = count 
        return self.p_count

    def extra_count(self,obj):
        count = Poll.objects.get_poll_extra_count(obj.id) or 0
        self.ex_count = count
        return self.ex_count
    
    def total_count(self,obj):
        return self.p_count + self.ex_count
    
    def generate_pdf(self,request,queryset):
        poll_data = []
        for poll in queryset:
            polled_users = PollUser.objects.filter(poll=poll)
            extra_counts = PollExtraCount.objects.filter(poll=poll)
            
            polled_user_data = [(
                index,
                polled_user.user.name,
                polled_user.user.email,
                polled_user.polled_date_time,
            ) for index,polled_user in enumerate(polled_users, start=1)]
            
            extra_count_data = [(
                index,
                extra_count.department,
                extra_count.count,
                extra_count.user.name,
                extra_count.user.email,
                extra_count.polled_date_time,
            ) for index,extra_count in enumerate(extra_counts, start=1)]
            
            polled_user_count = len(polled_users)
            extra_count_sum = extra_counts.aggregate(extra_count_sum=Sum('count'))['extra_count_sum'] or 0
            total_count = polled_user_count + extra_count_sum
            poll_data.append({
                'id': poll.id,
                'poll_text': poll.poll_text,
                'event_date_time': poll.event_date_time,
                'polled_user_count': len(polled_users),
                'polled_user_data': polled_user_data,
                'extra_count_data': extra_count_data,
                'extra_count_sum':extra_count_sum,
                'total_count': total_count
            })
        context = {'poll_data': poll_data}
        html_content = render_to_string('poll_result.html', context)

        pdf_file = HTML(string=html_content).write_pdf()

    # Create HTTP response with PDF content
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="poll_data.pdf"'
        return response


    generate_pdf.short_description = "PDF of Polled Users"


class ScheduledPollAdmin(admin.ModelAdmin):
    form = ScheduledPollForm

admin.site.register(Poll, PollAdmin)
admin.site.register(ScheduledPoll,ScheduledPollAdmin)