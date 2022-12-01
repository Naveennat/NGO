from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi import Form,File
from pydantic import BaseModel
from pymongo import MongoClient
from typing import List
from fastapi.encoders import jsonable_encoder



app = FastAPI()
templates = Jinja2Templates(directory="templates")
register = Jinja2Templates(directory="templates")
admin = Jinja2Templates(directory="templates")
delete= Jinja2Templates(directory="templates")


uri ="mongodb+srv://Demo:Demo_123@cluster0.9sjlmqh.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
ab = client.admin_user
db = client.NGO



class User(BaseModel):
    username: str
    password: str  

class Detail(BaseModel):
    name: str 
    email: str 
    contact: int
    reg_date: str 
    m_id: int

@app.get("/homePage", response_class=HTMLResponse) #http://127.0.0.1:8000/homePage
def show_service_page(request: Request):
    return templates.TemplateResponse("home.html", context={"request": request})

@app.get("/loginPage", response_class=HTMLResponse) #http://127.0.0.1:8000/loginPage
def show_service_page(request: Request):
    return templates.TemplateResponse("login.html", context={"request": request})

@app.get("/registerPage", response_class=HTMLResponse) #http://127.0.0.1:8000/registerPage
def show_register_page(request: Request):
    return register.TemplateResponse("Register.html", context={"request": request})

@app.get("/deletePage", response_class=HTMLResponse) #http://127.0.0.1:8000/deletePage
def show_service_page(request: Request):
    return templates.TemplateResponse("delete.html", context={"request": request})  

@app.get("/updatePage", response_class=HTMLResponse) #http://127.0.0.1:8000/updatePage
def show_service_page(request: Request):
    return templates.TemplateResponse("update.html", context={"request": request})   
    
@app.get("/findPage", response_class=HTMLResponse) #http://127.0.0.1:8000/findPage
def show_service_page(request: Request):
    return templates.TemplateResponse("donor.html", context={"request": request}) 

       




@app.post("/processlogin") #http://127.0.0.1:8000/processlogin
def check_user(request: Request,username:str= Form() , password:str= Form() ):

    user = ab["users"].find_one({"username": username})
    if username == user["username"] and password == user["password"]:

        return templates.TemplateResponse("control.html", context={"request": request})
           
    else:
        return " failed"    


@app.post("/findAll", response_model=List[Detail])#http://127.0.0.1:8000/findAll
def get_user(request: Request):

    user = db["Donors"].find()
    l = list(user)
    return l



@app.post("/create")  #http://127.0.0.1:8000/create 
def create_donor(response:Request, name: str=Form() , email: str=Form() ,contact: int=Form(), reg_date: str=Form() , m_id: int=Form()):
    x = {"name":name,"email":email,"contact":contact,"reg_date":reg_date,"m_id":m_id}
    obj = db["Donors"].insert_one(x)
    return "Registered Successfully"
    
      

@app.post("/delete") #http://127.0.0.1:8000/delete
def delete_donor(m_id: int = Form()):
    delete_donor = db["Donors"].delete_one({"m_id": m_id})
    return f"{m_id} deleted successfully"  

@app.post("/update") #http://127.0.0.1:8000/update
def update_user(updated_user: Detail,name: str=Form() , email: str=Form() ,contact: int=Form(), reg_date: str=Form() , m_id: int=Form()):
    user = x[name,email,contact,reg_date,m_id]
    x = {"name":name,"email":email,"contact":contact,"reg_date":reg_date,"m_id":m_id}
    user["name"] = updated_user.name
    user["email"] = updated_user.email
    user["contact"] = updated_user.contact
    user["reg_date"] = updated_user.reg_date
    user["m_id"] = updated_user.m_id
    obj = db["Donors"].update_one(user,x)
    return f"{m_id}Registered Successfully"
           