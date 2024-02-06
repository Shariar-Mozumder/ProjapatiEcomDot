import json
from .models import *
from .serializers import *
from django.db import connections
from .utils import api_response
from datetime import datetime,timedelta
import jwt

def getUserbyEmail(email):
    default_db=connections['default']
    data=[]
    parameters=[]
    try:
        if email is not None:
            
            query =(" Select * from [Projapoti].[dbo].[UserTable] where Email=%s")
            parameters.append(email)
            with default_db.cursor() as cursor:
                cursor.execute(query,parameters)
                columns = [col[0] for col in cursor.description]
                data=[dict(zip(columns, row)) for row in cursor.fetchall()]
                user=data[0] if data else None
            if user:
                response= api_response(200,"get User Successfully",user)
            else:
                response= api_response(200,"User Not found")
        else:
            response= api_response(401,"Invalid input")
    except Exception as e:
        response=api_response(500,"Server error: "+str(e))
    return response

def registration(userData):
    try:
        firstName=userData.get("FirstName")
        lastName=userData.get("LastName")
        password=userData.get("Password")
        email=userData.get("Email")
        phoneNumber=userData.get("PhoneNumber")
        gender=userData.get("Gender")
        user_pay=getUserbyEmail(email)
        if user_pay.get("status_code")==200 and user_pay.get("payload") is not None:
            response=api_response(401,"This email is already registered")
            return response
        elif user_pay.get("status_code")==200 and user_pay.get("payload") is None:
            if firstName is not None and password is not None and email is not None and phoneNumber is not None:
                token=create_token(email,password)
                if token:
                    user_payload={
                        "FirstName":firstName,
                        "LastName":lastName,
                        "Password":password,
                        "Email":email,
                        "PhoneNumber":phoneNumber,
                        "Gender":gender,
                        "RoleID":1,
                        "Status":1,
                        "IsDeleted":0,
                        "Token":token
                    }
                    user = Users(**user_payload)
                    user.save()
                    # user_json = json.dumps(user)
                    response=api_response(200,"Registered Successfully")
                else:
                    response=api_response(500,"Authentication Faild, Try again!")
            else:
                response=api_response(404,"Insufficient Data")
        else:
            return user_pay
    except Exception as e:
        response=api_response(500,"Server error: "+str(e))
    
    return response

def getAllUser():
    default_db=connections['default']
    data=[]
    try:
        query =(" Select * from [Projapoti].[dbo].[UserTable]")

        with default_db.cursor() as cursor:
            cursor.execute(query)
            columns = [col[0] for col in cursor.description]
            data=[dict(zip(columns, row)) for row in cursor.fetchall()]
        response= api_response(200,"Get all Users successfully",data)
    except Exception as e:
        response= api_response(500,"Server error: "+str(e),data)
    return response

def login(email, password):
    try:
        user_pay=getUserbyEmail(email)
        if user_pay.get("status_code")==200 and user_pay.get("payload") is not None:
            user=user_pay.get("payload")
            print(user)
            passwo=user["Password"]
            token=user["Token"]
            if passwo==password:
                # Define your payload (claims)
                token_response=varify_token(token,email,passwo)
                if token_response.get("status_code")==200:
                    new_token=create_token(email,passwo)
                    login_token=new_token if new_token else token
                    # user_obj = Users.objects.get(UserID=user["UserID"]) 
                    insert_token={
                        "Token":login_token
                    }
                    Users.objects.filter(UserID=user["UserID"]).update(**insert_token)
                    # user_serializer=UserSerializer(instance=user_obj,data=insert_token,partial=True)
                    # if user_serializer.is_valid():
                    #     user_serializer.save()
                    login_response={
                        "Email":email,
                        "Token":token
                    }
                    response=api_response(200,"Logged in successfully",login_response)
                else:
                    response=api_response(401,"Authentication Failed!")
            else:
                response=api_response(401,"Wrong Password")
        else:
            response=api_response(401,"User not found, Sign up first!")
    except Exception as e:
        response=api_response(500,"Server error: "+str(e))
    
    return response

def create_token(email, password):
    payload = {
        'email':email,
        'password': password,
        'exp': datetime.utcnow() + timedelta(days=1)  # Set expiration time to 30 minutes from now
    }
    # Define a secret key to sign the token (keep this secret!)
    secret_key = 'your_secret_keyqqqqqqqqqqqqqqqqq'
    # Generate JWT token
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token if token else None

def varify_token(token,email,password):
    # Define the secret key used to sign the token
    secret_key = 'your_secret_keyqqqqqqqqqqqqqqqqq'
    try:
        # Decode and verify the token
        decoded_payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        print("Token verification successful!")
        print("Decoded payload:", decoded_payload)
        if decoded_payload.get("email")==email and decoded_payload.get("password")==password:
            return api_response(200,"Token varified")
    except jwt.ExpiredSignatureError:
        return api_response(500,"Token has expired!")
    except jwt.InvalidTokenError:
        return api_response(500,"Token is invalid!")