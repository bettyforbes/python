import mysql.connector as rome
import bcrypt
#Function to add values in tables
def add_intable(table,column,data):
    #table = srting; column= list ; data=list with tuple entries
    costring=", ".join(column)
    placeholder=", ".join(["%s"] * len(data[0])) 
    inque="insert into {}({}) values({})".format(table,costring,placeholder)
    for a in range(0,len(data)):
        cursor.execute(inque,data[a])
    mycon.commit()
#**Function to check the login id and password
def checkpass(service_id, login,passwd):
    ser={100:'Police_stations',101:'Fire_Brigade',102:'Hospitals',108:' Disaster_Managment',112:'Emergency_Services'}
    if service_id in ser:
        cursor.execute("select Login_id,Password from {} where Service_id={}".format(ser[service_id],service_id))
        s=cursor.fetchall()
        b=[]
        for a in s:
            b.append(a[0])
        for a in s:
            if login not in b:
                return "Invalid login id"
            if a[0]==login:
                ps = a[1].encode('utf-8')# Hash the password
                salt = bcrypt.gensalt()  # Generate a salt
                hashed_password = bcrypt.hashpw(ps, salt)  # Hash the password with the salt
                input_password = passwd.encode('utf-8')
                if bcrypt.checkpw(input_password, hashed_password): #checking password given by user
                    return service_id
                else:
                    return "Invalid Password."
            
    else:
        return "Invalid service id Entered!"
#**Function to regularly update alerts table
def alert_upd():
    cursor.execute("delete from alerts")
    mycon.commit()
#***Function that will send the alert***
def send_alert(Service_id,loginID,password):
    ans=checkpass(Service_id,loginID,password)# First checking the credentials
    if type(ans)==str: # If any invalid thing is entered
        print(ans)
    else: # valid thing entered
        cursor.execute("select Name_Of_Service from list_of_services where Service_id={}".format(ans))
        name=str(cursor.fetchone()[0])
        ins="insert into alerts(Service_id, service_type) values({},'{}')".format(ans,name)
        cursor.execute(ins)
        mycon.commit()
        cursor.execute("select alert_id,alert_time from alerts ORDER BY alert_id DESC LIMIT 1")
        q=cursor.fetchone()
        time = q[1]  # Access the datetime object
        time_str = time.strftime('%Y-%m-%d %H:%M:%S')  # Convert to string
        #Final Message 
        print("CLEAR THE TRAFFIC!! EMERGENCY VEHICLE INCOMING FROM {} AlERT ID={} RECIEVED AT '{}'".format(name,q[0],time_str))
    alert_upd() # if 20 entries have exceeded the table,it will clear them all

#sql part
mycon=rome.connect(host="localhost",user="trailblazers",passwd="abc123",database="services")
cursor=mycon.cursor()
#adding the tables of all services
cursor.execute("create table list_of_services(Service_id int primary key, Name_Of_Service varchar(100))")
cursor.execute("create table Hospitals(Service_id int default 102,Login_id int primary key,Name_Of_Hospital varchar(100),Password varchar(10), Contact varchar(10),Avaliable_Vehicles int,Address varchar(100))")
cursor.execute("create table Police_stations(Service_id int default 100,Login_id int primary key,Name_Of_Station varchar(100),Password varchar(10) ,Contact varchar(10) ,Avaliable_Vehicles int,Address varchar(100))")
cursor.execute("create table Fire_Brigade(Service_id int default 101,Login_id int primary key,Name_Of_Station varchar(100),Password varchar(10), Contact varchar(10), Avaliable_Vehicles int,Address varchar(100))")
cursor.execute("create table Disaster_Managment(Service_id int default 108,Login_id int primary key,Name_Of_Service varchar(100),Password varchar(10), Contact varchar(10), Avaliable_Vehicles int,Address varchar(100))")
cursor.execute("create table Emergency_Services(Service_id int default 112,Login_id int primary key,Name_Of_Service varchar(100),Password varchar(10) ,Contact varchar(10) ,Avaliable_Vehicles int,Address varchar(100))")
#alerts table
cursor.execute("create table alerts(alert_id int auto_increment primary key ,Service_id int , service_type varchar(100),alert_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, CONSTRAINT fk_services FOREIGN KEY(Service_id) REFERENCES list_of_services(Service_id ))")
##adding values in tables
#1.table of services
values=[(100,'Police'),(101,'Firebrigade'),(102,'Ambulance'),(108,'Disaster Managment'),(112,'Emergency Medical Services')]
c=['Service_id','Name_Of_Service']
add_intable('list_of_services',c,values)

#2.hospitals
hospitals=[(4567,'City hospital','23des','9439634534',10,'123 Health Avenue, Sector 15, Delhi, 110015'),(5422,'Sunrise Medical Center','9ued','9346273459',23,'456 Wellness Street, Phase 2, Bangalore, 560034'),(3210,'LifeCare Hospital','sed34&','8493575463',32,'789 Care Road, Sector 7, Mumbai, 400061')]
col=['Login_id' ,'Name_Of_Hospital' ,'Password', 'Contact' ,'Avaliable_Vehicles' ,'Address']
add_intable('Hospitals',col,hospitals)

#3.Police
Police=[(1023,'Central Police Station','34er@','9439634534',6,'321 Law Lane, Central District, Delhi, 110001'),(3039,'Greenfield Police Station','89yth','9346273459',7,'654 Peace Park, Greenfield Colony, Noida, 201301'),(4121,'Metro City Police Station','yu45w','8937493543',5,'987 Justice Drive, Metro City, Chennai, 600020')]
col2=['Login_id','Name_Of_Station','Password','Contact','Avaliable_Vehicles','Address']
add_intable('Police_stations',col2,Police)

#4. Firebrigade
fire=[(9012,'City Fire Brigade','23des','8937493543',20,'852 Flame Street, Downtown, Mumbai, 400002'),(4956,'Northside Fire Station','4457tg','5345735876',14,'963 Blaze Boulevard, Northside, Pune, 411001'),(7829,'Rapid Response Fire Brigade','56rtg','9382738432',15,'147 Safety Crescent, Urban Area, Hyderabad, 500082')]
col3=['Login_id','Name_Of_Station','Password','Contact','Avaliable_Vehicles','Address']
add_intable('Fire_Brigade',col3,fire)

#5. Disaster Managment
dis=[(3456,'National Disaster Response Force (NDRF)','*ug45','9987655435',32,'741 Rescue Road, Disaster Management Complex, Delhi, 110048'),(3184,'Emergency Relief Operations Unit','er#45','8765423498',21,'852 Relief Avenue, Sector 10, Bangalore, 560085'),(5096,'Crisis Management Team (CMT)','67ers','9896875365',21,'963 Aid Alley, Relief Area, Kolkata, 700001')]
col4=['Login_id','Name_Of_Service','Password','Contact','Avaliable_Vehicles','Address']
add_intable('Disaster_Managment',col4,dis)

#6. emergency medical services
emer=[(7890,'City Emergency Ambulance Service','67rte','9874437654',21,' 258 First Aid Lane, City Center, Chennai, 600003'),(7834,'Quick Response Medical Services','902res','8765452674',12,' 369 Health Plaza, Downtown, Ahmedabad, 380009'),(2119,'RapidCare Emergency Medical Services','89^fes','9987653454',20,'147 Care Corner, Main Street, Jaipur, 302001')]
col5=['Login_id','Name_Of_Service','Password','Contact','Avaliable_Vehicles','Address']
add_intable('Emergency_Services',col5,emer)

##MAin Program
#values entered by user
service=int(input("enter service id"))
login=int(input("enter login id(It can never start from 0)"))
passwd=input("enter password")
#Values going to Alerts table
send_alert(service,login,passwd)











