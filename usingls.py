from flask import Flask, render_template,request,redirect,url_for
from datetime import date, timedelta
#from flask_redis import Redis
from bs4 import BeautifulSoup
import urllib.request,urllib.parse,urllib.error
import requests

#REDIS_URL = "redis://:password@localhost:6379/0"
app = Flask(__name__) #creating the Flask class object   
#redis_client = Redis(app) 
@app.route('/', methods=['GET', 'POST']) #decorator drfines the   
def home():
	test_date=date.today()
	user_list=['kanakagrawal','prashantmudgal']
	last_modified=localStorage.getItem('last_modified')
	if(last_modified==NULL):
		print("kanak")
		return render_template('addnewmemeber.html') 
	#redis_client.set('last_modified','2020-05-24')
	#last_modified=redis_client.get('last_modified')
	#last_modified=last_modified.decode('utf-8')
	else:
		test_date=str(test_date)
		if(last_modified!=test_date):
			last_modified=str(date.today())
			localStorage.setItem('last_modified',last_modified)
			#redis_client.set("last_modified",last_modified)
			for i in user_list:
				i=i.decode('utf-8')
				url="https://www.codechef.com/users/%s" %i
				print(url)
				r=requests.get(url)
				print(r)
				html=BeautifulSoup(r.content,'html5lib').find(class_='sidebar-right').find('main',attrs={'class':'content'}).find('div',attrs={'class':'ns-content'})
				profile=html.find(class_='user-profile-container').find(class_='row').find(class_='sidebar')
				ranking=profile.find(class_='widget').find(class_='content').find(class_='rating-header').find(class_='rating-number').text
				prev_ranking=localStorage.getItem(i)
				if(prev_ranking==NULL):
					prev_ranking=0
				localStorage.setItem(i,ranking)	
				#prev_ranking=redis_client.get(i).decode('utf-8')
				#redis_client.set(i,ranking)	
				#redis_client.save()
				rank_diff=int(ranking)-int(prev_ranking)
				localStorage.setItem('diff'+i,rank_diff)
				#redis_client.set('diff'+i,rank_diff)
				#redis_client.save()
		scores=dict()
		diff=dict()
		for i in user_list:
			i=i.decode('utf-8')
			scores[i]=int(localStorage.getItem(i))
			#scores[i]=redis_client.get(i).decode('utf-8')
			diff[i]=int(localStorage.getItem('diff'+i))
			#diff[i]=int(redis_client.get('diff'+i).decode('utf-8'))
		scores= sorted(scores.items(), key=lambda x: x[1], reverse=True)
		return render_template('practice.html',name=scores, difference=diff)

#@app.route('/addstudents',methods=['GET', 'POST'])
#def addNewStudent():
#	if request.method=='POST':
#		newmember=request.form["codechef_id"]
#		url="https://www.codechef.com/users/%s" %newmember
#		r=requests.get(url)
#		code=r.status_code
#		if code!=200:
#			print("user not found! enter a valid user")
#		else:	
#			redis_client.sadd('includemembers',newmember)
#			redis_client.save()
#			redis_client.set(newmember,"0")
#			redis_client.save()
#			redis_client.set('diff'+newmember,'0')
#			redis_client.save()
#		return redirect(url_for('home'))
#	else:
#		return render_template('addnewmemeber.html')  


if __name__ == '__main__':  
    app.run(debug = True)  