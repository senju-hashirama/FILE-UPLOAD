from flask import Flask,render_template,request,url_for,flash,redirect
from werkzeug.utils import secure_filename
import os

app=Flask(__name__)
movies_lis={}

app.secret_key="qwertyuplkjhgfdsazcvbnnm"
app.config['movies_upload_folder']="/media/series"
app.config['series_upload_folder']="/media/series"

def convert_to_mp4(file):
    os.system("ffmpeg -i {} -codec copy {}".format(file,file.replace("mkv","mp4")))
    return 
    
@app.route("/")
def home():
    if "user" not in app.config:
        return render_template("login.html")

    else:
        

        return render_template("home.html")

@app.route("/series")
def series():
    return render_template("series.html")

@app.route("/upload_file",methods=["POST","GET"])
def movies():

    if request.method=="POST":
        if "user" not in app.config:
            flash("Login first to upload files")
            return redirect("/login")

        else:

                if "file" not in request.files:
                    flash("NO file uploaded")
                    return redirect("/")

                else:
                    file=request.files["file"]

                    if file.filename=="":
                        flash("No file selected")
                        return redirect("/")
                    else:
                        if request.form.get("type")=="movie":
                                    
                                filename=secure_filename(file.filename)
                                file.save(os.path.join(app.config['movies_upload_folder'],filename))
                                if filename[-3:]=="mkv":
                                    convert_to_mp4(os.path.join(app.config['movies_upload_folder'],filename))
                                flash("File Uploaded")
                                return redirect("/upload")
                        elif reques.form.get("type")=="series":
                                
                                filename=secure_filename(file.filename)
                                file.save(os.path.join(app.config['series_upload_folder'],filename))
                                if filename[-3:]=="mkv":
                                    convert_to_mp4(os.path.join(app.config['series_upload_folder'],filename))
                                flash("File Uploaded")
                                return redirect("/upload")
                            

@app.route("/upload")
def upload():
    if "user" in app.config:
        
        return render_template("upload.html")
    else:
        return redirect("/login")
    
        
@app.route("/login")
def login():
    return render_template("login.html")
@app.route("/logout")
def logout():
    if "user" in app.config:
            
        app.config.pop("user")
        return redirect("/")
    else:
        return redirect("/login")
@app.route("/login_user",methods=["POST"])
def login_user():
    user_name=request.form.get("user_name")
    passwd=request.form.get("passwd")

    if (user_name=="admin")and(passwd=="anton@072003"):
        app.config["user"]="admin"
        return redirect("/")
    else:
        flash("incorrect credentials")
        return redirect("/login")
        
if __name__=="__main__":
    app.run(debug=True,host="0.0.0.0")
