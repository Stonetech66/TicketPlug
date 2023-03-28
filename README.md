<h1 align="center">E-ticket System</h1>
The E-Ticket System is an API designed to facilitate the sale and purchase of event tickets. This system allows event organizers to create and sell tickets, which must first be approved by the system administrator. Users can then easily browse and purchase tickets for upcoming events. 

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
git clone https://github.com/Stonetech66/E-Ticket-System.git
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

