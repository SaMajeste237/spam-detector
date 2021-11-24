from flask import Flask,request,render_template,url_for,redirect
import pickle

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

app = Flask(__name__)

#chargement des modèles œ&
file1 = open("count_vectorizer_model.sav", 'rb')
vectorizer = pickle.load(file1)

file2 = open("logistic_regression_model.sav", 'rb')
lr = pickle.load(file2)

@app.route('/api/spamdetector<e_mail>', methods=["GET"])
def detector(e_mail):
    # mail = request.args.get("mail")
    mail=e_mail
    print("mail ---" +mail)
    mail_2 = vectorizer.transform([mail]).toarray()
    p = lr.predict_proba(mail_2.reshape(1, -1))[0]
    print("Ce mail est un ham à ",p[1]*100,"%")
    print("Ce mail est un spam à",p[0]*100,"%")
    message = "ce mail est un spam à " + str(p[0]*100)+ " %."
    return render_template('index.html',message=message)


@app.route("/", methods=["GET","POST"])
def root():

  if request.method=="POST":
    email = request.form.get("email_text")
    print(email) 
    if email=="":
        return render_template('index.html')
    else:
        return redirect(url_for('detector', e_mail=email)) 
  else:
       return render_template('index.html')  
  
    
if __name__ == "__main__":
    app.run(port=8001, debug=True, host="127.0.0.1")