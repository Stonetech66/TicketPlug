<h1 align="center">TicketPlug</h1>
TicketPlug is a robust backend system for an online ticketing platform that simplifies the process of creating, managing, and selling event tickets. With TicketPlug, event organizers can effortlessly create and sell tickets, which undergo approval by the system admin. Attendees can easily browse and purchase tickets for upcoming events using the API and receive automatic PDF tickets with QR codes. TicketPlug incorporates Paystack payment API and Celery for background task management.










##  Features
- Approval workflow for event tickets created by organizers
- Integration with the Paystack payment API for secure online payments
- Background task management using Celery
- Automatic generation of PDF tickets with QR codes
- QR code scanning for easy ticket validation 
- Dockerized for easy deployment 

## Installation
To install the E-Ticket System, ensure you have docker and docker compose installed then follow these steps:

- Clone the repository to your local machine:
```
git clone https://github.com/Stonetech66/TicketPlug.git
```
- Cd into the directory 
```
cd E-Ticket-System
```
- Run the Docker Container
```
docker compose up
```
- Access the application in your browser 
at `http://localhost:8000/`.

## Usage
To use the E-Ticket System, follow these steps:

- Create an event as an organizer. This event will be subject to approval by the system administrator.
- Once approved, users can browse and purchase tickets for the event.
- Upon purchase, a PDF ticket will be generated containing a QR code.
- At the event, the QR code can be scanned to validate the ticket

## Credits
The E-Ticket System was developed by `Livingstone Maxwell`.

This project makes use of the following technologies:

- Django web framework
- Paystack payment API
- Celery task queue
- Pdfkit PDF generation library
- django-rest-framework for building Rest APIs
- django-filter for filtering APIs 
- docker and docker compose for containerization 

