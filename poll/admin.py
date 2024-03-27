from django.contrib import admin
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from poll.models import Poll,ScheduledPoll
from poll.forms import ScheduledPollForm


class PollAdmin(admin.ModelAdmin):
    list_display = ( 'event_date_time', 'poll_text', 'poll_count')
    readonly_fields = ('poll_count',)
    actions = ['generate_pdf']


    def poll_count(self,obj):
        return Poll.objects.get_poll_count(obj.id)


    def generate_pdf(self, request, queryset):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="poll_users.pdf"'

        # Create canvas
        c = canvas.Canvas(response, pagesize=letter)
        y = 750
        
        for poll in queryset:
            c.drawString(100, y, f'Poll ID: {poll.id}')
            c.drawString(100, y-20, f'Event Date: {poll.event_date_time}')
            c.drawString(100, y-40, f"Polled User count:{Poll.objects.get_poll_count(poll.id)}")
            y -= 60
        
        # Create table
        data = [['No.', 'Name', 'Email']]
        for poll in queryset:
            polled_users = Poll.objects.get_polled_users(poll.id)
            for index, user in enumerate(polled_users, start=1):
                data.append([index, user.name, user.email])

        table = Table(data)
        table.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.gray),
                                   ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                                   ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                                   ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                                   ('BOTTOMPADDING', (0,0), (-1,0), 12),
                                   ('BACKGROUND', (0,1), (-1,-1), colors.beige),
                                   ('GRID', (0,0), (-1,-1), 1, colors.black)]))

        # Draw table on canvas
        table.wrapOn(c, 400, 200)
        table.drawOn(c, 100, y-80)

        # Close the canvas
        c.showPage()
        c.save()
        return response


    generate_pdf.short_description = "PDF of Polled Users"


class ScheduledPollAdmin(admin.ModelAdmin):
    form = ScheduledPollForm

admin.site.register(Poll, PollAdmin)
admin.site.register(ScheduledPoll,ScheduledPollAdmin)