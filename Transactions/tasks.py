import string, random
from Events.models import OrderTicket
from Transactions.models import Payment, SoldTicket
from Users.models import User
from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task
from django.template.loader import render_to_string


@shared_task
def send_mail():
    send_mail(subject='Your purchased ticket from StoneCorp.com',
    message='Thanks for subscribing to my channel' ,recipient_list=['user@example.com'], from_email='noreply.examplecom')



def random_code():
    return ''.join(random.choices(string.digits + string.ascii_letters, k=20))

@shared_task
def SendTicket_to_mail(email, key, name, address, date, multi_email):
    if email ==None:
        send_mail(subject='Your purchased ticket from StoneCorp.com',
        message=f'Thanks for purchasing with us. Your Ticket( Event name: {name}, Event address: {address}, Event Date: {date}, Event Access_key: {key})', recipient_list=[f'{multi_email}'], from_email=settings.EMAIL_HOST_USER, html_message=render_to_string('multimessage.html', {'date':date, 'name':name, 'address':address, 'keys':key}))
    else:
        send_mail(subject='Your purchased ticket from StoneCorp.com',
        message=f'Thanks for purchasing with us. Your Ticket( Event name: {name}, Event address: {address}, Event Date: {date}, Event Access_key: {key})', recipient_list=[f'{email}'], from_email=settings.EMAIL_HOST_USER, html_message=render_to_string('message.html', {'date':date, 'name':name, 'address':address, 'keys':key, 'p':len(key)}))


@shared_task
def Create_Ticket(email, user_id, bought_ticket_id, payment):
    user=User.objects.get(id=user_id)
    bought_ticket=OrderTicket.objects.get(id=bought_ticket_id, status='completed')
    P=Payment.objects.get(id=payment)
    if email == None:
        event=bought_ticket.event
        name=event.name
        address=f'{event.address},  {event.state} {event.country}. '
        date=f'{event.start_date} - {event.end_date}'     
        for i in bought_ticket.tickets.all():
            p=eval(i.emails)
            for t in p:
                p=i.event_ticket
                j=SoldTicket.objects.create(user=user, payment=P, event=bought_ticket,ticket_class=p )
                o=j.key
                if p.label:
                    key=f"{i.event_ticket.label}: {o} "
                else:
                    key=f"{o} "
                SendTicket_to_mail.delay(key=key, name=str(name), address=address, date=date, email=email, multi_email=t)  

    else:
        keys=[]
        for i in bought_ticket.tickets.all():
            for t in range(i.qty):
                p=i.event_ticket
                j=SoldTicket.objects.create(user=user, payment=P, event=bought_ticket,ticket_class=p )
                if p.label:
                    o=j.key
                    
                    key=f"{i.event_ticket.label}: {o}"
                else:
                    o=j.key
                    key=f"{o} "
                keys.append(key)
        event=bought_ticket.event
        name=event.name
        address=f'{event.address},  {event.state} {event.country}. '
        date=f'{event.start_date} - {event.end_date}'     
        SendTicket_to_mail.delay(key=keys, name=str(name), address=address, date=date, email=email, multi_email=None)  

@shared_task
def Create_PaymentRecord(bought_ticket_id, amount, user_id, email):
        u=User.objects.get(id=user_id)
        bought_ticket=OrderTicket.objects.get(id=bought_ticket_id, status='not completed')
        bought_ticket.status = 'completed'
        bought_ticket.save()
        p=Payment.objects.create(user=u, amount=amount, ticket=bought_ticket, payment_id=random_code())
        Create_Ticket.delay(email=email, bought_ticket_id=bought_ticket_id, payment=p.id, user_id=user_id)


def send_error_mail(error):
    send_mail(message=f'{error}', from_email='livingstonemaxwell971@gmail.com', recipient_list=['zionlivingstone4@gmail.com'])

