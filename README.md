# Flask_api_mongodb

### About

> A flask api, with authentication, password encoding, with endpoints that allow users to create account, login, create templates, and perform CRUD actions with the templates.

## How to use

### 1. To register as a new user 
    
    <URL : localhost:5000/register
    Method : POST
    Headers : {
                'Accept': 'application/json',
                'Content-Type': 'application/json',          
              }
    Body :    {
                first_name : 'lead_test@subi.com',
                last_name : '123456'
                email : 'lead_test@subi.com',
                password : '123456'
              }
>

### 2. Login as a user

    <URL : localhost:5000/login
      Method : POST
      Headers : {
                 'Accept': 'application/json',
                'Content-Type': 'application/json',          
              }
     Body :    {
                email : 'lead_test@subi.com',
                password : '123456'
              }  
    > 


### 3 Template CRUD
    
> 1. Insert new Template

    <URL : locahost:5000/template
    Method : POST
    Headers : {
                'Authorization': 'Bearer ' + 'token from login step',
                'Accept': 'application/json',
                'Content-Type': 'application/json',          
              }
    Body :    {
                'template_name': ' ',
                'subject': ' ',
                'body': ' ',
                     }  
>
    
> 2. Get All Template

    <URL : locahost:5000/template  
    Method : GET
    Headers : {
                'Authorization': 'Bearer ' + "{token}"
                'Accept': 'application/json',
                'Content-Type': 'application/json',          
              }
    Body :    {}      


### 3. Single Template
> 1. GET single
    <URL : locahost:5000/template/template_id
    Method : GET
    Headers : {
                'Authorization': 'Bearer ' + "{token}"
                'Accept': 'application/json',
                'Content-Type': 'application/json',          
              }
    Body :    {}  >

>2.Update Single Template

    URL : locahost:5000/template/<template_id>
    
    Method : PUT
    Headers : {
                'Authorization': 'Bearer ' + <access_token from login step>,
                'Accept': 'application/json',
                'Content-Type': 'application/json',          
              }
    Body :    {
                'template_name': ' ',
                'subject': ' ',
                'body': ' ',
    }   

 > 3. DELETE Single Template
    
    <URL : locahost:5000/template/template_id
    Method : DEL
    Headers : {
                'Authorization': 'Bearer ' + "{token}"
                'Accept': 'application/json',
                'Content-Type': 'application/json',          
              }
    Body :    {}                  

>
