import string, random
import io
import qrcode
import base64
from django.urls import reverse
from Events.models import OrderTicket
from Transactions.models import Payment, SoldTicket
from Users.models import User
from django.conf import settings
from celery import shared_task
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
import pdfkit
from .utils import format_date


def generate_ref_code():
 
   return ''.join(random.choices(string.digits + string.ascii_letters, k=20))

def generate_key():
    return ''.join(random.choices(string.digits, k=16))
    
def generate_pdf(html):
    return pdfkit.from_string(html)

def generate_qrcode(data):
    qr = qrcode.QRCode(
                    box_size=5,
                        )
    qr.add_data(data)
    qr.make(fit=True)
    buffer = io.BytesIO()
    img = qr.make_image(fill_color='black', back_color='white')
    img.save(buffer, format='PNG')
    return base64.b64encode(buffer.getvalue()).decode('utf-8')



def create_ticket(email, user_id, bought_ticket_id, payment_id):   
    user=User.objects.get(id=user_id)
    bought_ticket=OrderTicket.objects.get(id=bought_ticket_id, status='completed')
    payment=Payment.objects.get(id=payment_id)
    event=bought_ticket.event
    name=event.name
    address=f'{event.address} {event.state} {event.country}'
    date=format_date(event.start_date,event.end_date)
    if email == None: # send the tickets to the multiple emails the user provided
        for ticket in bought_ticket.tickets.all():
            emails=eval(ticket.emails)
            for email in emails:
                ticket=ticket.event_ticket
                key=generate_key()
                sold_ticket=SoldTicket.objects.create(user=user, payment=payment, event=bought_ticket,ticket=ticket, key=key )
                url=settings.ALLOWED_HOSTS[0] + str(reverse('verify-qrcode', kwargs={'key':key, 'event':event.id} )) 
                qrcode=generate_qrcode(url)
                context={'event':name, 'data' :None, 'qrcode':qrcode, 'date':date, 'address':address, 'label':ticket.label} 
                template= render_to_string('pdf.html', context)
                pdf=generate_pdf(template)
                subject='[TicketPlug] Purchased Tickets 🎉'
                text_content='Thanks for Purchasing with Us \n' 
                html_context={'event':name, 'address':address, 'label':ticket.label, 'date':date } 
                html_content=render_to_string('ticket.html', html_context)
                msg=EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
                msg.attach_alternative(html_content, "text/html")
                msg.attach(f'{name}_ticket.pdf', pdf)
                msg.send()
    else: #send the tickets to the single email the user provided during payment
        data=[] 
        for ticket in bought_ticket.tickets.all():
            for t in range(ticket.qty):
                ticket=t.event_ticket
                key=generate_key()
                sold_ticket=SoldTicket.objects.create(user=user, payment=payment, event=bought_ticket,ticket=ticket, key=key)
                url=settings.ALLOWED_HOSTS[0] + str(reverse('verify-qrcode', kwargs={'key':key, 'event':event.id} )) 
                qrcode=generate_qrcode(url)
                context={'event':name, 'qrcode':qrcode, 'date':date, 'address':address, 'label':ticket.label} 
                data.append(context) 
        html=render_to_string('pdf.html', {'data':data})      
        subject='[TicketPlug] Purchased Tickets 🎉'
        text_content='Thanks for Purchasing with Us \n' 
        html_context={'event':name, 'address':address, 'date':date } 
        html_content=render_to_string('ticket.html', html_context)
        msg=EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
        pdfs=generate_pdf(html)
        msg.attach_alternative(html_content, "text/html")
        msg.attach(f'{name}_ticket.pdf', pdfs)
        msg.send()
        
        
''' 
function to generate payment record and call the function to send tickets functions
if payment was sucessful
'''
@shared_task
def create_payment_record(bought_ticket_id, amount, user_id, email):
        user=User.objects.get(id=user_id)
        ref_code=generate_ref_code()
        try:
         payment=Payment.objects.create(user=user, amount=amount, ticket=bought_ticket, payment_id=ref_code)


         bought_ticket=OrderTicket.objects.get(id=bought_ticket_id, status='not completed')
         bought_ticket.status = 'completed'
         for ticket in bought_ticket.tickets.all():
              ticket.event_ticket.sold +=  ticket.qty
              ticket.event_ticket.save()
              ticket.completed= True
              ticket.save()
         bought_ticket.save()
         create_ticket(email=email, bought_ticket_id=bought_ticket_id, payment=payment.id, user_id=user_id)
        except Exception as e:
            print(e) 
'''
function to be called if payment failed
'''
@shared_task
def payment_failed(bought_ticket_id, amount, user_id, email):
        OrderTicket.objects.get(id=bought_ticket_id, status='not completed').tickets.delete()
        



