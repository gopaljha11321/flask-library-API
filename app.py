from dataclasses import dataclass
from flask import Flask,request
from pymongo import MongoClient
import datetime
CONNECTION_STRING = "mongodb+srv://gopal:jhaji9871436400@cluster0.it4owmc.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(CONNECTION_STRING)
mydatabase = client['Books']
mydatabase2=client['Transaction']
collection2=mydatabase2['entry']
collection = mydatabase['library']

app=Flask(__name__)

@app.route('/')
def home():
    return "Welcome to libraray managment system!!"
#First_API
@app.route('/list',methods=['GET','POST'])
def list():
    name=request.json["name"]
    data=collection.find({"book_name":name})
    l1=[]
    l=1;
    for i in data:
        output={}
        output["S.No"]=l
        output["Book name"]=i["book_name"]
        l1.append(output)
        l+=1
    print(l1)
    return l1

#Second_API
@app.route('/range',methods=['GET','POST'])
def range():
    start=request.json['start']
    end=request.json['end']
    data=collection.find({'$and':[{'rent':{'$gte':start}},{'rent':{"$lte":end}}]})
    l1=[]
    for i in data:
        output={}
        output["Name"]=i["book_name"]
        output['RentPrice']=i["rent"]
        l1.append(output)
    return l1

#Third API
@app.route('/books_list',methods=['GET','POST'])
def books_list():
    start=request.json['start']
    end=request.json['end']
    name=request.json["name"]
    category=request.json["category"]
    data=collection.find({'$and':[{'rent':{'$gte':start}},{'rent':{"$lte":end}},{"book_name":name},{"category":category}]})
    l1=[]
    l=1
    for i in data:
        output={}
        output["S.No"]=l
        output["Name"]=i["book_name"]
        l+=1;
        l1.append(output)
    return l1

#Fourth_API
@app.route('/issue',methods=['POST'])
def issue():
    price=10
    data={
    "price":10,
    "book_name":request.json["book_name"],
    "person_name":request.json["person_name"],
    "issue_date":request.json["issue_date"]
    }
    collection2.insert_one({"Price":data["price"],"Book_name":data["book_name"],"Person_name":data["person_name"],"Issue_date":data['issue_date']})
    return "Data entry successfully"

#Fifth_API
@app.route('/return',methods=['POST'])
def total():
    price=10
    input={
    "Book_name":request.json["book_name"],
    "Person_name":request.json["person_name"],
    }
    return_date=request.json["return_date"]
    data=collection2.find({"Book_name":input["Book_name"],"Person_name":input["Person_name"]})
    issue_date=""
    for i in data:
        issue_date=i["Issue_date"]
    date1=datetime.datetime.strptime(issue_date,"%b %d %Y")
    date2=datetime.datetime.strptime(return_date,"%b %d %Y")
   
    dif=(date2-date1).days
    print(dif)
    data_update={
        "$set":{
    "Return_date":return_date,
    "Amount":dif*price
        }
    }
    collection2.update_one({"Person_name":request.json["person_name"]},data_update)
    return str(dif*price)

#Sixth_API
@app.route('/issue_list',methods=['POST'])
def issue_list():
    price=10
    book_name=request.json["book_name"]
    output={}
    count_total=collection2.count_documents({"Book_name":book_name})
    
    issue_count=collection2.count_documents({'$and':[{"Book_name":book_name},{'Return_date':{"$exists" :False}}]})
    print(count_total,issue_count)
    output["Total_count"]=count_total
    output["Issue_count"]=issue_count
    return output

#Seventh_API   
@app.route('/total_rent',methods=['POST'])
def total_rent():
    price=10
    book_name=request.json["book_name"]
    total_book=collection2.find({'$and':[{"Book_name":book_name},{'Return_date':{"$exists" :True}}]})
    sum=0
    for i in total_book:
        sum+=i["Amount"]
    return str(sum)

#Eighth_API
@app.route('/person_list',methods=['POST'])
def person_list():
    price=10
    person_name=request.json["person_name"]
    total_book=collection2.find({"Person_name":person_name})
    data={}
    k=1
    for i in total_book:
        data[k]=i['Book_name']
        k+=1  
    return data

#Ninth_API
@app.route('/date_range',methods=['POST'])
def data_range():
    start=request.json["start"]
    start_date=datetime.datetime.strptime(start,"%b %d %Y")
    end=request.json["end"]
    end_date= datetime.datetime.strptime(end,"%b %d %Y")
    total_data=collection2.find({})
    l1=[]
    for i in total_data:
        data={}
        book_date=datetime.datetime.strptime(i["Issue_date"],"%b %d %Y")
        if(book_date>=start_date and book_date<=end_date):
            data['Issue_Date']=i['Issue_date']
            data['Book_name']=i["Book_name"]
            l1.append(data)
    return l1


if __name__=="__main__":
    app.run()



