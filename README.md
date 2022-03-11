# Invoicing-company-REST-Personal-Project-
This respository is a personal project of an invoicing company using Django Rest Framework and Postman.

Now we have an explanation of the deploy of this proyect:

1. Start and use the clients CRUD using the following paths:
    - Create a client using the url (host/users/signup/) with POST method. Here you with be asked for an email, username, password, password confirmation, first name, last name and document. This process creates a Jason web token (JWK) and sends it to the client email previusly provided.
    - After taking the token from the email, you can go head and click on the url (host/users/verify/) using POST where you can provide the token and receive a successfull message if it is the correct token.
    - Then, you can go a head and login in the url (host/users/login/) using POST method. Please remember that if you don't do the verify process before geting to the login, you will receive and errore message.
    - Once you are already authenticated, you are available to create bills using your provide token on each bill header url, it will be explaned later. Now, you can also Update (method PUT, url - host/users/{username}/) , partial update (method PATCH, url - host/users/{username}/) and delete (method DELETE, url - host/users/{username}/) your profile. Moreover, you can also watch all you profile information at url host/users/{{username}}/ using method GET.

2. Once you are done with all client avaible process, you can use the bills CRUD:
    - You can create bills using url (host/invoicing/create_bill/) with POST method, you won't be able to use this url unless you provide the prevous created JWK on the http request header. Here you will be asked for a company name, nit, code and product data. Remember that you won't be able to create a bill unless you use a unique bill code. Moreover, product data is a Json file that has all the new products to add for this bill on each value.
    - Once you have some bills, you can go head and use Update (method PUT, url - host/invoicing/{bill_code}/edit/) , partial update (method PATCH, url - host/invoicing/{bill_code}/edit/) and delete (method DELETE, url - host/invoicing/5165/). Moreover, you can list all client bills by using host/invoicing/ with th GET method, only if you use the client token in the http header.

3. You can also download a CSV register with all the client information saved, like document, first name, last name y invoice quantities related; by using the url host/download/ with the GET method. Moreover, you can also create clients by importing a CSV file with first name, last name, email, username, document and pasword; By using url host/import/ with GET method. There has been provied an example CSV model file.
