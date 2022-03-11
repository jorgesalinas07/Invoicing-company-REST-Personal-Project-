# Invoicing-company-REST-Personal-Project-
This respository is a personal project of an invoicing company using Django Rest Framework

Now we have an explanation of the deply of this proyect:

1. Start and use the clients CRUD usiing the folowing paths:
    - Create a client using the url (host/users/signup/). Here you with be asked by an email, username, password, password confirmation, first name, last name and document. This process creates a Jason web token (JWK) and sends it to the client email previusly provided.
    - After taking the token from the email, you can go head and click on the url (host/users/verify/) where you can provide the token and recive a successfull message if it is the correct token.
    - Then, you can go a head and login in the url (host/users/login/)
