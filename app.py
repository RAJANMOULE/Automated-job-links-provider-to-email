from flask import *
from bs4 import BeautifulSoup
import requests
import time
from email.message import EmailMessage
import smtplib

app=Flask(__name__)

app.config['SECRET KEY']='caraxes!'

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/homepage' , methods=['POST','GET'])
def homepage():
    if request.method=='POST':
        result=request.form
        uname=request.form['uname'] 
        pword=request.form['pword']
        if uname=='moule' and pword=="rajan":
            return render_template("home.html",result=result)

@app.route('/wfo', methods=['POST','GET'])
def wfo():
    return render_template('wfo.html')
@app.route('/wfo_mail',methods=['POST','GET'])
def wfo_mail():
    if request.method=='POST':
        result=request.form
        _email=request.form['_email']          
        _skill=request.form['_skill']

    def find_jobs():
        html_txt=requests.get(f'https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords={_skill}&txtLocation=').text
        soup=BeautifulSoup(html_txt,'lxml')
        jobs=soup.find_all('li',class_='clearfix job-bx wht-shd-bx')
        for job in jobs:
            published_date=job.find('span',class_='sim-posted').text.strip()
            if 'few' in published_date:
                global company_name,skills,more_info
                company_name=job.find('h3',class_='joblist-comp-name').text.strip()
                skills=job.find('span',class_='srp-skills').text.strip()
                more_info=job.header.h2.a['href']
                
            msg = EmailMessage()
            msg.set_content(f'''Company name : {company_name}
Required skills : {skills}
More info : {more_info}''')

            msg['Subject'] = 'Work from office jobs'
            msg['From'] = "gmoulerajan@gmail.com"
            msg['To'] = f"{_email}"
            # Send the message via our own SMTP server.
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login("gmoulerajan@gmail.com", "yzddqrsuotakchow")
            server.send_message(msg)
            server.quit()
            
    if __name__=='__main__':
        find_jobs()

    return render_template('logout.html',result=result)

@app.route('/wfh', methods=['POST','GET'])
def wfh():
    return render_template('wfh.html')

@app.route('/wfh_mail', methods=['POST','GET'])
def wfh_mail():
    if request.method=='POST':
        result=request.form
        email=request.form['email']
        skill=request.form['skill']

    def finding_job():
        html=requests.get(f'https://www.flexjobs.com/search?search={skill}&location=').text
        soup=BeautifulSoup(html,'lxml')
        jobs=soup.find_all('li',class_='m-0 row job')
        for job in jobs:
            published_date=job.find('div',class_='col-auto text-right').text.strip()
            if 'New!' in published_date:
                name=job.find('div',class_='col text-nowrap pr-0').text.strip()
                job_description=job.find('div',class_='job-description').text.strip()
                link=job.div.div.a['href']

                msg = EmailMessage()
                msg.set_content(f'''Company name : {name}
Job description : {job_description}
Published date : {published_date}
Link : {link}''')

                msg['Subject'] = 'Work from home jobs'
                msg['From'] = "gmoulerajan@gmail.com"
                msg['To'] = f"{email}"
            # Send the message via our own SMTP server.
                server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                server.login("gmoulerajan@gmail.com", "yzddqrsuotakchow")
                server.send_message(msg)
                server.quit()
                
    if __name__=='__main__':
        finding_job()

    return render_template('logout.html',result=result)

if __name__=='__main__':
    while True:
        app.run(debug=True)
        time_wait=10
        print(f'waiting {10} minutes')
        time.sleep(time_wait*60)
