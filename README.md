<h1 align="center">E-Ticket API</h1>
This is an E-Ticket API system. It's an API created where users can sell tickets for their events but it first has to be approved by the admin, and also where users can buy tickets for an event.
Integrated Paystack payment API to handle payments, also made use of celery to handle background tasks.

##  Language Used
- python

##  Framework and Packages Used
- Django
- Django-Rest-Framework
- Celery
- Django-cors-headers
- DjangoRestFramework-simplejwt
- django-rest-swagger
- drf-yasg
- Django-allauth

## Third party API Used
- Paystack

## Live Project Link
   You can find the documentation of the API here <link>https://e-ticket.onrender.com/docs</link>

## Buying Ticket Demo
- NOTE: A user has to be authenticated to buy a ticket.
- A user picks the ticket he wants to buy and also chooses the qty. If he chooses more than one qty or buys more than one type of ticket for that event for example VIP and Regular,
  he has the option to send the tickets to a single email or multiple emails.
- The user will then be promted to input his card information. if the payment was successfull the tickets will be created then sent to the emails provided.




