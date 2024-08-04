from flask import *
from DBConnection import Db


app = Flask(__name__)
app.secret_key="hello"


@app.route('/')
def Home():
    db = Db()
    qry = "select * from rules"
    res = db.selectOne(qry)
    return render_template("Public/index.html", data=res)

@app.route('/Home_index')
def Home_index():
    db = Db()
    qry = "select * from rules"
    res = db.selectOne(qry)
    return render_template('Public/index2.html', data=res)

@app.route('/Login')
def Login():
    return render_template('Log-in page.html')

@app.route('/Login_post',methods=['post'])
def Login_post():
    username=request.form['textfield']
    password=request.form['textfield2']
    db=Db()
    qry_log="select * from `login` where username='"+username+"' and password='"+password+"'"
    res=db.selectOne(qry_log)
    if res is not None:
        session['login_id']=res['login_id']

        if res['type']=="admin":
            return redirect('/Admin_home')
        elif res['type']=="student":
            return redirect('/Student_home')
        else:
            return '''<script>alert('Invalid username or password'); window.location='/Login'</script>'''
    else:

        return '''<script>alert('Invalid user'); window.location='/Login'</script>'''

@app.route('/forget_pass')
def forget_pass():
    return render_template('Forget pass.html')

@app.route('/forget_pass_post',methods=['post'])
def forget_pass_post():
    db=Db()
    email = request.form['email']
    mob = request.form['mob']
    qry = "select * from student WHERE `Email`='" + email + "' and `Phone`='" + mob + "' "
    res=db.selectOne(qry)
    if res is None:
        return '''<script>alert('Email and Mobile not found');history.back()</script>'''
    else:
        return render_template('Change password.html',lid=res['Login_id'])

@app.route('/Change_pass')
def Change_pass():
    return render_template('Change password.html')

@app.route('/Change_pass_post',methods=['post'])
def Change_pass_post():
    db=Db()
    id=request.form['id']
    new=request.form['new']
    con=request.form['con']
    if new==con :
        qry="UPDATE `login` SET `password`='"+con+"' where login_id='"+id+"' "
        db.update(qry)
        return redirect('/Login')
    else:
        return '''<script>alert('new and confirm password doesnt match');history.back()</script>'''

#============================================Admin=====================================================================

@app.route('/Admin_home')
def Admin_home():
    return render_template('Admin/index.html')

@app.route('/Admin_index')
def Admin_index():
    return render_template('Admin/index2.html')



@app.route('/Course_add')
def Course_add():
    return render_template('Admin/Course Add.html')

@app.route('/Course_add_post',methods=['post'])
def Course_add_post():
    db=Db()
    name=request.form['textfield']
    duration=request.form['textfield2']
    department=request.form['textfield3']
    semester=request.form['textfield4']
    fee=request.form['fee']
    syllabus = request.files['fileField']
    from datetime import datetime
    date=datetime.now().strftime("%y%m%d-%H%M%S")
    syllabus.save("G:\\Online_Admision\\static\\Course_syllabus\\"+date+syllabus.filename)
    path="/static/Course_syllabus/"+date+syllabus.filename
    description=request.form['textarea']
    qry_course="INSERT INTO `course`(`Name`,`Duration`,`Department`,`Semester`,`fee`,`Syllabus`,`Description`)VALUES('"+name+"','"+duration+"','"+department+"','"+semester+"','"+fee+"','"+path+"','"+description+"')"
    db.insert(qry_course)
    return '''<script>alert('Course added successfully');window.location='/Course_view#tab'</script>'''

@app.route('/Course_view')
def Course_view():
    db=Db()
    qry="select * from course"
    res=db.select(qry)
    return render_template('Admin/Course View.html',data=res)

@app.route('/Course_edit/<id>')
def Course_edit(id):
    db=Db()
    qry="select * from `course` WHERE course_id='"+id+"'"
    res=db.selectOne(qry)
    return render_template('Admin/Course Edit.html',data=res)

@app.route('/Course_delete/<id>')
def Course_delete(id):
    db=Db()
    qry="DELETE FROM `course` WHERE `course_id`='"+id+"'"
    res=db.delete(qry)
    return '''<script>alert('Deleted');window.location='/Course_view#tab'</script>'''

@app.route('/Course_edit_post',methods=['post'])
def Course_edit_post():
    db=Db()
    id=request.form['id']
    name=request.form['textfield']
    duration=request.form['textfield2']
    department=request.form['textfield3']
    semester=request.form['textfield4']
    fee=request.form['fee']
    description = request.form['textarea']
    if 'fileField' in request.files:
        syllabus=request.files['fileField']
        if syllabus.filename!="":
            from datetime import datetime
            date=datetime.now().strftime('%y%m%d-%H%M%S')
            syllabus.save("G:\\Online_Admision\\static\\Course_syllabus\\"+date+syllabus.filename)
            path="/static/Course_syllabus/"+date+syllabus.filename
            qry="UPDATE `course` SET `Name`='"+name+"',`Duration`='"+duration+"',`Department`='"+department+"',`Semester`='"+semester+"',fee='"+fee+"',`Syllabus`='"+path+"',`Description`='"+description+"' where course_id='"+id+"'"
            db.update(qry)
        else:
            qry = "UPDATE `course` SET `Name`='" + name + "',`Duration`='" + duration + "',`Department`='" + department + "',`Semester`='" + semester + "',fee='"+fee+"',`Description`='" + description + "' where course_id='" + id + "'"
            db.update(qry)
    else:
        qry = "UPDATE `course` SET `Name`='" + name + "',`Duration`='" + duration + "',`Department`='" + department + "',`Semester`='" + semester + "',fee='"+fee+"',`Description`='" + description + "' where course_id='" + id + "'"
        db.update(qry)

    return '''<script>alert('Updated');window.location='/Course_view#tab'</script>'''

@app.route('/Rules_add')
def Rules_add():
    return render_template('Admin/Rules Add.html')

@app.route('/Rules_add_post',methods=['post'])
def Rules_add_post():
    db=Db()
    prospect=request.files['fileField']
    from datetime import datetime
    date=datetime.now().strftime("%y%m%d-%H%M%S")
    prospect.save("G:\\Online_Admision\\static\\rulesprospects\\"+date+prospect.filename)
    path="/static/rulesprospects/"+date+prospect.filename
    qry_rules="INSERT INTO `rules`(`prospectus`)VALUES('"+path+"')"
    db.insert(qry_rules)
    return '''<script>alert('Rules added successfully');window.location='/Rules_view#tab'</script>'''

@app.route('/Rules_view')
def Rules_view():
    db=Db()
    qry="select * from rules"
    res=db.select(qry)
    return render_template('Admin/Rules View.html',data=res)

@app.route('/Rules_delete/<id>')
def Rules_delete(id):
    db=Db()
    qry="DELETE FROM `rules` WHERE `rules_id`='"+id+"'"
    db.delete(qry)
    return '''<script>alert('Deleted');window.location='/Rules_view#tab'</script>'''

@app.route('/Rules_edit/<id>')
def Rules_edit(id):
    db=Db()
    qry="select * from rules where rules_id='"+id+"'"
    res=db.selectOne(qry)
    return render_template('Admin/Rules Edit.html',data=res)

@app.route('/Rules_edit_post',methods=['post'])
def Rules_edit_post():
    db=Db()
    id = request.form['rules_id']
    if 'fileField' in request.files:

        prospectus=request.files['fileField']
        if prospectus.filename!="":

            from datetime import datetime
            dt=datetime.now().strftime("%Y%m%d%H%M%S")+".jpg"
            prospectus.save("G:\\Online_Admision\static\\rulesprospects\\"+dt+prospectus.filename)
            path="/static/rulesprospects/"+dt+prospectus.filename
            qry="UPDATE `rules` SET `prospectus`='"+path+"' where rules_id='"+id+"'"
            db.update(qry)
        else:
            qry = "UPDATE `rules` SET `Rules`='" + rules + "',`Terms`='" + terms + "' where rules_id='" + id + "'"
            db.update(qry)
    else:
        qry = "UPDATE `rules` SET `Rules`='" + rules + "',`Terms`='" + terms + "' where rules_id='" + id + "'"
        db.update(qry)
    return '''<script>alert('Updated');window.location='/Rules_view#tab'</script>'''

@app.route('/Vacancy_add')
def Vacancy_add():
    db=Db()
    qry="SELECT * FROM `course`"
    res=db.select(qry)
    return render_template('Admin/Vacancy Add.html',data=res)

@app.route('/Vacancy_add_post',methods=['post'])
def Vacancy_add_post():
    db=Db()
    course=request.form['select']
    seat=request.form['textfield']
    qry_Vacancy="INSERT INTO `vacancy`(`Course_id`,`Vacant_seat`)VALUES ('"+course+"','"+seat+"')"
    db.insert(qry_Vacancy)
    return '''<script>alert('Seat added successfully');window.location='/Vacancy_view#tab'</script>'''

@app.route('/Vacancy_view')
def Vacancy_view():
    db=Db()
    qry="select * from vacancy INNER JOIN course ON course.course_id=vacancy.Course_id"
    res=db.select(qry)
    return render_template('Admin/Vacancy View.html',data=res)

@app.route('/Vacancy_delete/<id>')
def Vacancy_delete(id):
    db=Db()
    qry="DELETE FROM `vacancy` WHERE `Vacancy_id`='"+id+"'"
    db.delete(qry)
    return '''<script>alert('Deleted');window.location='/Vacancy_view#tab'</script>'''

@app.route('/Vacancy_edit/<id>')
def Vacancy_edit(id):
    db=Db()
    qry="select * from vacancy INNER JOIN course ON course.course_id=vacancy.Course_id where Vacancy_id='"+id+"'"
    res=db.selectOne(qry)
    return render_template('Admin/Vacancy Edit.html',data=res)

@app.route('/Vacancy_edit_post',methods=['post'])
def Vacancy_edit_post():
    db=Db()
    id=request.form['id']
    seat=request.form['textfield']
    qry="UPDATE `vacancy` SET `Vacant_seat`='"+seat+"' WHERE `Vacancy_id`='"+id+"'"
    db.update(qry)
    return '''<script>alert('Updated');window.location='/Vacancy_view#tab'</script>'''





@app.route('/Course_application')
def Course_application():
    db=Db()
    qry="SELECT * , `course`.`Name` AS C_name , `student`.`Name` AS S_name FROM `application` INNER JOIN `vacancy` ON `vacancy`.`Vacancy_id`=`application`.`Vacancy_id` INNER JOIN `course` ON `course`.`course_id`=`vacancy`.`Course_id` INNER JOIN `student` ON `student`.`Login_id`=`application`.`Student_id` where Status='pending'"
    res=db.select(qry)
    return render_template('Admin/application.html',data=res)

@app.route('/Search_application',methods=['post'])
def Search_application():
    db=Db()
    frm=request.form['from']
    to=request.form['to']
    qry="SELECT * , `course`.`Name` AS C_name , `student`.`Name` AS S_name FROM `application` INNER JOIN `vacancy` ON `vacancy`.`Vacancy_id`=`application`.`Vacancy_id` INNER JOIN `course` ON `course`.`course_id`=`vacancy`.`Course_id` INNER JOIN `student` ON `student`.`Login_id`=`application`.`Student_id` where Status='pending' and date BETWEEN '"+frm+"' and '"+to+"' "
    res=db.select(qry)
    return render_template('Admin/application.html',data=res)


@app.route('/Approve_course/<id>')
def Approve_course(id):
    db=Db()
    qry="update application set Status='Approved' where Application_id='"+id+"' "
    res=db.update(qry)

    qry1="select * from application INNER JOIN `vacancy` ON `vacancy`.`Vacancy_id`=`application`.`Vacancy_id` where Application_id='"+id+"'"
    res1=db.selectOne(qry1)
    st_id=str(res1['Student_id'])

    qry2="update application set Status='Rejected' where Student_id='"+st_id+"' and Application_id!='"+id+"' "
    res2=db.update(qry2)

    seat=(res1['Vacant_seat'])
    new_seat=int(seat)-1
    qry3="update vacancy set Vacant_seat='"+str(new_seat)+"' where Vacancy_id='"+str(res1['Vacancy_id'])+"'  "
    db.update(qry3)

    return '''<script>alert('Approved');window.location="/Course_application#tab" </script>'''

@app.route('/Reject_application/<id>')
def Reject_application(id):
    db=Db()
    qry="update application set Status='Rejected' where Application_id='"+id+"' "
    db.update(qry)
    return '''<script>alert('Rejected');window.location="/Course_application" </script>'''

@app.route('/Approved_application')
def Approved_application():
    db=Db()
    qry="SELECT * , `course`.`Name` AS C_name , `student`.`Name` AS S_name FROM `application` INNER JOIN `vacancy` ON `vacancy`.`Vacancy_id`=`application`.`Vacancy_id` INNER JOIN `course` ON `course`.`course_id`=`vacancy`.`Course_id` INNER JOIN `student` ON `student`.`Login_id`=`application`.`Student_id` where Status='approved'"
    res=db.select(qry)
    return render_template('Admin/Approved application.html', data=res)





@app.route('/Search_approval',methods=['post'])
def Search_approval():
    db=Db()
    frm=request.form['from']
    to=request.form['to']
    qry="SELECT * , `course`.`Name` AS C_name , `student`.`Name` AS S_name FROM `application` INNER JOIN `vacancy` ON `vacancy`.`Vacancy_id`=`application`.`Vacancy_id` INNER JOIN `course` ON `course`.`course_id`=`vacancy`.`Course_id` INNER JOIN `student` ON `student`.`Login_id`=`application`.`Student_id` where Status='approved' and date BETWEEN '"+frm+"' and '"+to+"' "
    res=db.select(qry)
    return render_template('Admin/Approved application.html',data=res)


@app.route('/Rejected_application')
def Rejected_application():
    db=Db()
    qry="SELECT * , `course`.`Name` AS C_name , `student`.`Name` AS S_name FROM `application` INNER JOIN `vacancy` ON `vacancy`.`Vacancy_id`=`application`.`Vacancy_id` INNER JOIN `course` ON `course`.`course_id`=`vacancy`.`Course_id` INNER JOIN `student` ON `student`.`Login_id`=`application`.`Student_id` where Status='rejected'"
    res=db.select(qry)
    return render_template('Admin/Rejected application.html',data=res)

@app.route('/Search_rejection',methods=['post'])
def Search_rejection():
    db=Db()
    frm=request.form['from']
    to=request.form['to']
    qry="SELECT * , `course`.`Name` AS C_name , `student`.`Name` AS S_name FROM `application` INNER JOIN `vacancy` ON `vacancy`.`Vacancy_id`=`application`.`Vacancy_id` INNER JOIN `course` ON `course`.`course_id`=`vacancy`.`Course_id` INNER JOIN `student` ON `student`.`Login_id`=`application`.`Student_id` where Status='rejected' and date BETWEEN '"+frm+"' and '"+to+"' "
    res=db.select(qry)
    return render_template('Admin/Rejected application.html',data=res)

@app.route('/Paid_application')
def Paid_application():
    db=Db()
    qry="select *,`course`.`Name` AS C_name , `student`.`Name` AS S_name from payment inner JOIN application on application.Application_id = payment.application_id INNER JOIN `vacancy` ON `vacancy`.`Vacancy_id`=`application`.`Vacancy_id` INNER JOIN `course` ON `course`.`course_id`=`vacancy`.`Course_id` INNER JOIN `student` ON `student`.`Login_id`=`application`.`Student_id` where payment.status='Paid'"
    res=db.select(qry)
    return render_template('Admin/Paid application.html',data=res)

@app.route('/Search_paid',methods=['post'])
def Search_paid():
    db=Db()
    frm=request.form['from']
    to=request.form['to']
    qry="SELECT *,`course`.`Name` AS C_name , `student`.`Name` AS S_name FROM payment INNER JOIN application ON application.Application_id = payment.application_id INNER JOIN `vacancy` ON `vacancy`.`Vacancy_id`=`application`.`Vacancy_id` INNER JOIN `course` ON `course`.`course_id`=`vacancy`.`Course_id` INNER JOIN `student` ON `student`.`Login_id`=`application`.`Student_id` WHERE payment.status='Paid' AND `payment`.`p_date` BETWEEN '"+frm+"' AND '"+to+"' "
    res=db.select(qry)
    return render_template('Admin/Paid application.html',data=res)


@app.route('/Student_detail/<id>')
def Student_detail(id):
    db=Db()
    qry="select * from student where Login_id='"+id+"' "
    res=db.selectOne(qry)
    return render_template('Admin/Student view.html',data=res)

@app.route('/View_payment/<id>')
def View_payment(id):
    db=Db()
    qry="SELECT * FROM `payment` INNER JOIN `application` ON `application`.`Application_id`=`payment`.`application_id` where payment.`application_id`='"+id+"'"
    res=db.select(qry)
    return render_template('Admin/Payment.html',data=res)


#-----------------------------------Student---------------------------------

@app.route('/Student_home')
def Student_home():
    db=Db()
    qry="select * from rules"
    res=db.selectOne(qry)
    return render_template("User/index.html",data=res)

@app.route('/Student_index')
def Student_index():
    db=Db()
    qry="select * from rules"
    res=db.selectOne(qry)
    return render_template('User/index2.html',data=res)


@app.route('/Student')
def Student():

    return render_template('User/Sign up.html',date="2006-01-01")

@app.route('/Student_post',methods=['post'])
def Student_post():
    db=Db()
    cap_id=request.form['cap']
    name=request.form['name']
    birth=request.form['dob']
    phone=request.form['mob']
    email=request.form['mail']
    add1 = request.form['ad1']
    add3 = request.form['ad3']
    add4 = request.form['ad4']
    post = request.form['post']
    pin = request.form['pin']
    gender = request.form['gender']
    qualification = request.form['qual']
    sslc_percent = request.form['sslc_per']
    plus_percent = request.form['plus2_per']

    sslc = request.files['sslc']
    from datetime import datetime
    date = datetime.now().strftime('%y%m%d-%H%M%S')
    sslc.save("G:\\Online_Admision\\static\\sslcbook\\" + "sslc-" + date + sslc.filename)
    path_sslc = "/static/sslcbook/" + "sslc-" + date + sslc.filename

    marklist = request.files['plus2']

    qry_val="select * from login where username='"+email+"' "
    res1=db.selectOne(qry_val)
    if res1 is None :

        from datetime import datetime
        date = datetime.now().strftime('%y%m%d-%H%M%S')
        marklist.save("G:\\Online_Admision\\static\\marklist\\" + "marklist-" + date + marklist.filename)
        path_marklist = "/static/marklist/" + "marklist-" + date + marklist.filename

        photo = request.files['photo']
        from datetime import datetime
        date = datetime.now().strftime('%y%m%d-%H%M%S')
        photo.save("G:\\Online_Admision\\static\\photo\\" + "photo-" + date + photo.filename)
        path_photo = "/static/photo/" + "photo-" + date + photo.filename


        qry_log="insert into login (username,password,type) values ('"+email+"','"+birth+"','student') "
        res=db.insert(qry_log)

        qry_stud="INSERT INTO `student`(`Cap_id`,`Name`,`Date_of_Birth`,`Phone`,`Email`,`Add1`,`Add3`,`Add4`,`Post`,`Pin`,`Gender`,`Qualification`,`SSLC_Book`,`SSLC_Percentage`,`+2_marklist`,`+2_Percentage`,`Photo`,Login_id) VALUES('"+cap_id+"','"+name+"','"+birth+"','"+phone+"','"+email+"','"+add1+"','"+add3+"','"+add4+"','"+post+"','"+pin+"','"+gender+"','"+qualification+"','"+path_sslc+"','"+sslc_percent+"','"+path_marklist+"','"+plus_percent+"','"+path_photo+"','"+str(res)+"')"
        db.insert(qry_stud)
        return '''<script>alert('Password always Date of Birth');window.location='/Login'</script>'''
    else:
        return '''<script>alert('Email is already taken');history.back()</script>'''

@app.route('/Register_view')
def Register_view():
    db=Db()
    qry="select * from student where Login_id='"+str(session['login_id'])+"' "
    res=db.selectOne(qry)
    return render_template('User/Student view.html',data=res)


@app.route('/Register_edit/<id>')
def Register_edit(id):
    db=Db()
    qry="select * from student where Student_id='"+id+"'"
    res=db.selectOne(qry)
    return render_template('User/Register edit.html',data=res)

@app.route('/Register_edit_post',methods=['post'])
def Register_edit_post():
    db=Db()
    add1 = request.form['ad1']
    add3 = request.form['ad3']
    add4 = request.form['ad4']
    post = request.form['post']
    pin = request.form['pin']
    gender = request.form['gender']
    qualification = request.form['qual']
    sslc_percent = request.form['sslc_per']
    plus_percent = request.form['plus2_per']

    sslc = request.files['sslc']
    from datetime import datetime
    date = datetime.now().strftime('%y%m%d-%H%M%S')
    sslc.save("G:\\Online_Admision\\static\\sslcbook\\" + "sslc-" + date + sslc.filename)
    path_sslc = "/static/sslcbook/" + "sslc-" + date + sslc.filename

    marklist = request.files['plus2']
    from datetime import datetime
    date = datetime.now().strftime('%y%m%d-%H%M%S')
    marklist.save("G:\\Online_Admision\\static\\marklist\\" + "marklist-" + date + marklist.filename)
    path_marklist = "/static/marklist/" + "marklist-" + date + marklist.filename

    photo = request.files['photo']
    from datetime import datetime
    date = datetime.now().strftime('%y%m%d-%H%M%S')
    photo.save("G:\\Online_Admision\\static\\photo\\" + "photo-" + date + photo.filename)
    path_photo = "/static/photo/" + "photo-" + date + photo.filename
    qry1="UPDATE `student` SET `Add1`='"+add1+"',`Add3`='"+add3+"',`Add4`='"+add4+"',`Post`='"+post+"',`Pin`='"+pin+"',`Gender`='"+gender+"',`Qualification`='"+qualification+"',`SSLC_Book`='"+path_sslc+"',`SSLC_Percentage`='"+sslc_percent+"',`+2_marklist`='"+path_marklist+"',`+2_Percentage`='"+plus_percent+"',`Photo`='"+path_photo+"' where `Login_id`='"+str(session['login_id'])+"' "
    db.update(qry1)
    return '''<script>alert('Edited successfully');window.location='/Register_view'</script>'''


@app.route('/Student_course')
def Student_course():
    db=Db()
    qry="select * from course INNER JOIN vacancy on vacancy.Course_id=course.course_id"
    res=db.select(qry)
    return render_template('User/Course User View.html',data=res)


@app.route('/Apply/<id>')
def Apply(id):
    db=Db()
    qry="INSERT INTO `application` (`Student_id`,`Vacancy_id`,`Status`,`date`) VALUES('"+str(session['login_id'])+"','"+id+"','pending',curdate()) "
    db.insert(qry)
    return '''<script>alert('Applied');window.location="/Student_home"</script>'''


@app.route('/Student_application')
def Student_application():
    db=Db()
    qry="SELECT * , `course`.`Name` AS C_name , `student`.`Name` AS S_name FROM `application` INNER JOIN `vacancy` ON `vacancy`.`Vacancy_id`=`application`.`Vacancy_id` INNER JOIN `course` ON `course`.`course_id`=`vacancy`.`Course_id` INNER JOIN `student` ON `student`.`Login_id`=`application`.`Student_id` where student.Login_id='"+str(session['login_id'])+"'"
    res=db.select(qry)
    qry_1="select * from payment INNER  JOIN application ON application.Application_id=payment.application_id where application.Student_id='"+str(session['login_id'])+"'"
    res_1=db.selectOne(qry_1)
    print(res_1)
    if res_1 is not None :
        if res_1['status']=='Paid':
            return render_template('User/application.html', data=res,status='Paid',data_1=res_1)
        else :
            return render_template('User/application.html',data=res,status='Not paid')
    else :
        return render_template('User/application.html',data=res,status='Not paid',data_1=res_1)

@app.route('/Search_myapplication',methods=['post'])
def Search_myapplication():
    db=Db()
    frm=request.form['from']
    to=request.form['to']
    qry="SELECT * , `course`.`Name` AS C_name , `student`.`Name` AS S_name FROM `application` INNER JOIN `vacancy` ON `vacancy`.`Vacancy_id`=`application`.`Vacancy_id` INNER JOIN `course` ON `course`.`course_id`=`vacancy`.`Course_id` INNER JOIN `student` ON `student`.`Login_id`=`application`.`Student_id` where student.Login_id='"+str(session['login_id'])+"' and date BETWEEN '"+frm+"' and '"+to+"' "
    res=db.select(qry)
    qry_1 = "select * from payment INNER  JOIN application ON application.Application_id=payment.application_id where application.Student_id='" + str(session['login_id']) + "'"
    res_1 = db.selectOne(qry_1)
    print(res_1)
    if res_1 is not None:
        if res_1['status'] == 'Paid':
            return render_template('User/application.html', data=res, status='Paid', data_1=res_1)
        else:
            return render_template('User/application.html', data=res, status='Not paid')
    else:
        return render_template('User/application.html', data=res, status='Not paid', data_1=res_1)


@app.route('/Make_payment/<id>')
def Make_payment(id):
    db=Db()
    qry="SELECT * , `course`.`Name` AS C_name FROM `application` INNER JOIN `vacancy` ON `vacancy`.`Vacancy_id`=`application`.`Vacancy_id` INNER JOIN `course` ON `course`.`course_id`=`vacancy`.`Course_id` where Application_id='"+str(id)+"'"
    res=db.selectOne(qry)
    return render_template('User/Make payment.html',data=res)

@app.route('/Challan',methods=['post'])
def Challan():
    db=Db()
    id=request.form['id']
    amnt=request.form['amount']
    acc=request.form['account']
    ifsc=request.form['ifsc']
    card=request.form['card']
    cvv=request.form['cvv']
    expiry=request.form['expiry']
    pin=request.form['pin']
    qry="SELECT * FROM `bank` WHERE `accont_number`='"+acc+"' and `ifsc`='"+ifsc+"' and `card_no`='"+card+"' and `cvv`='"+cvv+"' and `expiry`='"+expiry+"' and pin='"+pin+"'"
    res=db.selectOne(qry)
    if res is not None:
        bal=res['balance']
        if bal > int(amnt):
            qry1="INSERT INTO`payment` (`application_id`,`amount`,`p_date`,`account_number`,`status`) VALUES ('"+id+"','"+amnt+"', curdate() ,'"+acc+"','Paid') "
            db.insert(qry1)
            new_bal=bal-int(amnt)
            qry2="update bank set balance='"+str(new_bal)+"' where accont_number='"+acc+"'"
            db.update(qry2)
            return '''<script>alert('Payment done successfully');window.location='/Student_application'</script>'''
        else :
            return '''<script>alert('Insufficient balance');history.back()</script>'''
    else :
        return '''<script>alert('Invalid credentials');history.back()</script>'''


    #------------------------------------------ Public-----------------------------------------------


@app.route('/Public')
def Public():
    db = Db()
    qry = "select * from rules"
    res = db.selectOne(qry)
    return render_template("Public/index.html", data=res)

@app.route('/Public_course')
def Public_course():
    db=Db()
    qry = "select * from course INNER JOIN vacancy on vacancy.Course_id=course.course_id"
    res = db.select(qry)
    return render_template('Public/Course Public View.html', data=res)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")