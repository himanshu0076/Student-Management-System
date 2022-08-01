from tkinter import*
from tkinter import ttk
from PIL import Image,ImageTk 
import mysql.connector
from tkinter import messagebox
from tkinter import filedialog
import os


def Main():
    win=Tk()
    app=Login_Window(win)
    win.mainloop()


class Login_Window:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Login")

        self.bg = ImageTk.PhotoImage(file=r"C:\Users\HIMANSHU SHARMA\Desktop\Student management system\college_images\background.jpg")
        lbl_bg= Label(self.root,image=self.bg)
        lbl_bg.place(x=0,y=0,relwidth=1,relheight=1)

        frame= Frame(self.root,bg="green")
        frame.place(x=610,y=170,width=340,height=450)

        img1= Image.open(r"C:\Users\HIMANSHU SHARMA\Desktop\Student management system\college_images\icon.png")
        img1=img1.resize((100,100),Image.ANTIALIAS)
        self.PhotoImage1=ImageTk.PhotoImage(img1)
        lblimg1=Label(image=self.PhotoImage1,bg="green",borderwidth=0)
        lblimg1.place(x=730,y=175,width=100,height=100)

        get_str=Label(frame,text="Get Started",font=("times new roman",20,"bold"),fg="white",bg="green")
        get_str.place(x=95,y=100)

        # label
        username_lbl= Label(frame,text="Username",font=("times new roman",15,"bold"),fg="white",bg="green")
        username_lbl.place(x=70,y=155)

        self.txtuser = ttk.Entry(frame,font=("times new roman",15,"bold"))
        self.txtuser.place(x=40,y=180,width=270)

        password_lbl= Label(frame,text="Password",font=("times new roman",15,"bold"),fg="white",bg="green")
        password_lbl.place(x=70,y=225)

        self.txtpass = ttk.Entry(frame,font=("times new roman",15,"bold"))
        self.txtpass.place(x=40,y=250,width=270)

        # icon images
        img2= Image.open(r"C:\Users\HIMANSHU SHARMA\Desktop\Student management system\college_images\user.png")
        img2=img2.resize((25,25),Image.ANTIALIAS)
        self.PhotoImage2=ImageTk.PhotoImage(img2)
        lblimg2=Label(image=self.PhotoImage2,bg="green",borderwidth=0)
        lblimg2.place(x=650,y=323,width=25,height=25)


        img3= Image.open(r"C:\Users\HIMANSHU SHARMA\Desktop\Student management system\college_images\password.jpg")
        img3=img3.resize((25,25),Image.ANTIALIAS)
        self.PhotoImage3=ImageTk.PhotoImage(img3)
        lblimg3=Label(image=self.PhotoImage3,bg="green",borderwidth=0)
        lblimg3.place(x=650,y=397,width=25,height=25)


        # login button
        btn_login=Button(frame,text="Login",font=("times new roman",15,"bold"),borderwidth=3,relief=RIDGE,command=self.login,cursor="hand2",fg="white",bg="red",activeforeground="white",activebackground="red")
        btn_login.place(x=110,y=300,width=120,height=35)

        # register button
        registerbtn=Button(frame,text="New User Register",command=self.register_window,font=("times new roman",10,"bold"),borderwidth=0,fg="white",bg="green",activeforeground="white",activebackground="black")
        registerbtn.place(x=15,y=350,width=160)

        # forgot password button
        forgetbtn=Button(frame,text="Forget Password",command=self.forgot_password_window,font=("times new roman",10,"bold"),border=0,fg="white",bg="green",activeforeground="white",activebackground="black")
        forgetbtn.place(x=10,y=370,width=160)


    def register_window(self):
        self.new_window=Toplevel(self.root)
        self.app=Register( self.new_window)



    def login(self):
            if self.txtuser.get()=="" or self.txtpass.get()=="":
                messagebox.showerror("Error","All fields are required")
            # elif self.txtuser.get()=="himanshu" and self.txtpass.get()=="1234":
            #     messagebox.showinfo("Success","Welcome to Student Management System")
            else:
                conn=mysql.connector.connect(host="localhost",user="root",password="him@nshu0809",database="mydata")
                my_cursor=conn.cursor()
                my_cursor.execute("select * from register where email=%s and password=%s",(
                                                                                           self.txtuser.get(),
                                                                                           self.txtpass.get()
                                                                                    ))

                row= my_cursor.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Username & Password")
                else:
                    open_main=messagebox.askyesno("YesNO","Access only Admin")
                    if open_main>0:
                        self.new_window=Toplevel(self.root)
                        self.app=Student(self.new_window)
                    else:
                        if not open_main:
                            return
                        
                conn.commit()
                conn.close()

    

    # *********** reset password ********************
    def reset_pass(self):
        if self.combo_security_Q.get()=="Select":
            messagebox.showerror("Error","Select the Security Question",parent=self.root2)
        elif self.txt_security.get()=="":
            messagebox.showerror("Error","Please Enter the Answer",parent=self.root2)
        elif self.txt_newpass.get()=="":
            messagebox.showerror("Error","Please Enter the New Password",parent=self.root2)
        else:
            conn=mysql.connector.connect(host="localhost",user="root",password="him@nshu0809",database="mydata")
            my_cursor=conn.cursor()
            query=("select * from register where email=%s and securityQ=%s and securityA=%s")
            value=(self.txtuser.get(),self.combo_security_Q.get(),self.txt_security.get(),)
            my_cursor.execute(query,value)
            row=my_cursor.fetchone()
            if row==None:
                messagebox.showerror("Error","Please Enter the correct Answer",parent=self.root2)
            else:
                query=("update register set password=%s where email=%s")
                value=(self.txt_newpass.get(),self.txtuser.get())
                my_cursor.execute(query,value)

                conn.commit()
                conn.close()
                messagebox.showinfo("Info","Your Password has been reset, Please login to new Password",parent=self.root2)
                self.root2.destroy()



    # **********************  forgot password window *************************
    def forgot_password_window(self):
        if self.txtuser.get()=="":
            messagebox.showerror("Error","Please enter the Email address to reset password")

        else:
            conn=mysql.connector.connect(host="localhost",user="root",password="him@nshu0809",database="mydata")
            my_cursor=conn.cursor()
            query=("select * from register where email=%s")
            value=(self.txtuser.get(),)
            my_cursor.execute(query,value)
            row=my_cursor.fetchone()
            # print(row)

            if row==None:
                messagebox.showerror("Error","Please Enter the valid uername")
            else:
                conn.close()
                self.root2=Toplevel()
                self.root2.title("Forget Password")
                self.root2.geometry("340x450+610+170")

                l=Label(self.root2,text="Forgot Password",font=("times new roman",20,"bold"),fg="red",bg="white")
                l.place(x=0,y=10,relwidth=1)

                security_Q=Label(self.root2,text="Selected Security Questions",font=("times new roman",15,"bold"),fg="black")
                security_Q.place(x=50,y=80)

                self.combo_security_Q=ttk.Combobox(self.root2,font=("times new roman",15,"bold"),state="readonly")
                self.combo_security_Q["values"]=("Select", "Your Birth Place","Your Friend Name","Your Pet Name")
                self.combo_security_Q.place(x=50,y=110,width=250)
                self.combo_security_Q.current(0)



                security_A= Label(self.root2,text="Security Answer",font=("times new roman",15,"bold"),fg="black")
                security_A.place(x=50,y=150)

                self.txt_security=ttk.Entry(self.root2,font=("times new roman",15))
                self.txt_security.place(x=50,y=180,width=250)

                new_pass= Label(self.root2,text="New Password",font=("times new roman",15,"bold"),fg="black")
                new_pass.place(x=50,y=220)

                self.txt_newpass=ttk.Entry(self.root2,font=("times new roman",15))
                self.txt_newpass.place(x=50,y=250,width=250)

                btn=Button(self.root2,text="Reset",command=self.reset_pass,font=("times new roman",15,"bold"),fg="white",bg="green")
                btn.place(x=100,y=290)



               



class Register:
    def __init__(self,root):
        self.root=root
        self.root.title("Register")
        self.root.geometry("1600x900+0+0")

        # Variables*****************
        self.var_fname=StringVar()
        self.var_lname=StringVar()
        self.var_contact=StringVar()
        self.var_email=StringVar()
        self.var_securityQ=StringVar()
        self.var_securityA=StringVar()
        self.var_pass=StringVar()
        self.var_confpass=StringVar()



           # background image
        self.bg=ImageTk.PhotoImage(file=r"C:\Users\HIMANSHU SHARMA\Desktop\Student management system\college_images\background2.jpg")

        bg_lbl=Label(self.root,image=self.bg)
        bg_lbl.place(x=0,y=0,relwidth=1,relheight=1)

        # Left side image
        self.bg1=ImageTk.PhotoImage(file=r"C:\Users\HIMANSHU SHARMA\Desktop\Student management system\college_images\leftimage.jpg")
        left_lbl=Label(self.root,image=self.bg1)
        left_lbl.place(x=50,y=100,width=470,height=550)

      # *********** Main Frame ***********
        frame= Frame(self.root,bg="white")
        frame.place(x=520,y=100,width=800,height=550)

        Register_lbl=Label(frame,text="REGISTER HERE",font=("times new roman",20,"bold"),fg="darkgreen",bg="white")
        Register_lbl.place(x=20,y=20)

        # ********* Label and Entry *******

        # row 1
        fname= Label(frame,text="First Name",font=("times new roman",15,"bold") ,bg="white")
        fname.place(x=50,y=100)

        fname_entry= ttk.Entry(frame,textvariable=self.var_fname,font=("times new roman",15,"bold"))
        fname_entry.place(x=50,y=130,width=250)

        l_name= Label(frame,text="Last Name",font=("times new roman",15,"bold"),fg="black",bg="white")
        l_name.place(x=370,y=100)

        self.txt_lname=ttk.Entry(frame,textvariable=self.var_lname,font=("times new roman",15))
        self.txt_lname.place(x=370,y=130,width=250)

        # row 2

        contact= Label(frame,text="Contact No",font=("times new roman",15,"bold"),fg="black",bg="white")
        contact.place(x=50,y=170)

        self.txt_contact=ttk.Entry(frame,textvariable=self.var_contact,font=("times new roman",15))
        self.txt_contact.place(x=50,y=200,width=250)

        email=Label(frame,text="Email",font=("times new roman",15,"bold"),bg="white",fg="black")
        email.place(x=370,y=170)

        self.txt_email=ttk.Entry(frame,textvariable=self.var_email,font=("times new roman",15))
        self.txt_email.place(x=370,y=200,width=250)

        # # row 3

        security_Q=Label(frame,text="Selected Security Questions",font=("times new roman",15,"bold"),fg="black",bg="white")
        security_Q.place(x=50,y=240)

        self.combo_security_Q=ttk.Combobox(frame,textvariable=self.var_securityQ,font=("times new roman",15,"bold"),state="readonly")
        self.combo_security_Q["values"]=("Select", "Your Birth Place","Your Friend Name","Your Pet Name")
        self.combo_security_Q.place(x=50,y=270,width=250)
        self.combo_security_Q.current(0)




        security_A= Label(frame,text="Security Answer",font=("times new roman",15,"bold"),fg="black",bg="white")
        security_A.place(x=370,y=240)

        self.txt_security=ttk.Entry(frame,textvariable=self.var_securityA,font=("times new roman",15))
        self.txt_security.place(x=370,y=270,width=250)

        # row 4

        pswd= Label(frame,text="Password",font=("times new roman",15,"bold"),fg="black",bg="white")
        pswd.place(x=50,y=310)

        self.txt_pswd=ttk.Entry(frame,textvariable=self.var_pass,font=("times new roman",15))
        self.txt_pswd.place(x=50,y=340,width=250)

        confirm_pswd= Label(frame,text="Confirm Password",font=("times new roman",15,"bold"),fg="black",bg="white")
        confirm_pswd.place(x=370,y=310)

        self.txt_confirm_pswd=ttk.Entry(frame,textvariable=self.var_confpass,font=("times new roman",15))
        self.txt_confirm_pswd.place(x=370,y=340,width=250)

        # ************** check button *****************
        self.var_check=IntVar()
        checkbtn=Checkbutton(frame,variable=self.var_check,text="I agree the terms & conditions",font=("times new roman",12,"bold"),onvalue=1,offvalue=0)
        checkbtn.place(x=50,y=380)

        # Buttons
        img=Image.open(r"C:\Users\HIMANSHU SHARMA\Desktop\Student management system\college_images\register.jpg")
        img=img.resize((200,50),Image.ANTIALIAS)
        self.photoimage=ImageTk.PhotoImage(img)
        b1=Button(frame,image=self.photoimage,command=self.register_data,borderwidth=0,cursor="hand2")
        b1.place(x=10,y=420,width=200)

        img1=Image.open(r"C:\Users\HIMANSHU SHARMA\Desktop\Student management system\college_images\login.jpg")
        img1=img1.resize((200,50),Image.ANTIALIAS)
        self.photoimage1=ImageTk.PhotoImage(img1)
        b2=Button(frame,image=self.photoimage1,command=self.return_login,borderwidth=0,cursor="hand2")
        b2.place(x=330,y=420,width=200)


    # Function decleration 


    def register_data(self):
        if self.var_fname.get()=="" or self.var_email.get()=="" or self.var_securityQ.get()=="Select":
            messagebox.showerror("Error","All fields are required",parent=self.root)
        elif self.var_pass.get()!=self.var_confpass.get():
            messagebox.showerror("Error","Password & Confirm Password must be same",parent=self.root)
        elif self.var_check.get()==0:
            messagebox.showerror("Error","Please agree terms & condition",parent=self.root)
        else:
            conn=mysql.connector.connect(host="localhost",user="root",password="him@nshu0809",database="mydata")
            my_cursor=conn.cursor()
            query=("select * from register where email=%s")
            value=(self.var_email.get(),)
            my_cursor.execute(query,value)
            row=my_cursor.fetchone()
            if row!=None:
                messagebox.showerror("Error","User already exist please use another email",parent=self.root)
            else:
                my_cursor.execute("insert into register values(%s,%s,%s,%s,%s,%s,%s)",(
                                                                                           self.var_fname.get(),
                                                                                           self.var_lname.get(),
                                                                                           self.var_contact.get(),
                                                                                           self.var_email.get(),
                                                                                           self.var_securityQ.get(),
                                                                                           self.var_securityA.get(),
                                                                                           self.var_pass.get()

                                                                                             ))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success","Registered Successfully",parent=self.root)

    def return_login(self):
        self.root.destroy()
            


class Student:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("STUDENT MANAGEMENT SYSTEM")

        # Variables
        self.var_dep=StringVar()
        self.var_course=StringVar()
        self.var_year=StringVar()
        self.var_semester=StringVar()
        self.var_std_id=StringVar()
        self.var_std_name=StringVar()
        self.var_div=StringVar()
        self.var_roll=StringVar()
        self.var_gender=StringVar()
        self.var_dob=StringVar()
        self.var_email=StringVar()
        self.var_phone=StringVar()
        self.var_address=StringVar()
        self.var_teacher=StringVar()




        # first image
        img= Image.open(r"college_images\7th.jpg")
        img = img.resize((540,160),Image.ANTIALIAS)
        self.photoimg = ImageTk.PhotoImage(img)

        self.btn_1=Button(self.root,command=self.open_img,image=self.photoimg,cursor="hand2")
        self.btn_1.place(x=0,y=0,width=540,height=160)

        # second image
        img_2= Image.open(r"college_images\6th.jpg")
        img_2=img_2.resize((540,160),Image.ANTIALIAS)
        self.photoimg_2 = ImageTk.PhotoImage(img_2)

        self.btn_2=Button(self.root,command=self.open_img_2,image=self.photoimg_2,cursor="hand2")
        self.btn_2.place(x=540,y=0,width=540,height=160)
        
        # third image
        img_3= Image.open(r"college_images\5th.jpg")
        img_3= img_3.resize((540,160),Image.ANTIALIAS)
        self.photoimg_3 = ImageTk.PhotoImage(img_3)

        self.btn_3=Button(self.root,command=self.open_img_3,image=self.photoimg_3,cursor="hand2")
        self.btn_3.place(x=1000,y=0,width=540,height=160)

        # background image
        img_4= Image.open(r"college_images\university.jpg")
        img_4= img_4.resize((1530,710),Image.ANTIALIAS)
        self.photoimg_4 = ImageTk.PhotoImage(img_4)

        bg_lbl= Label(self.root,image=self.photoimg_4,bd=2,relief=RIDGE)
        bg_lbl.place(x=0,y=160,width=1530,height=710)

        lbl_title=Label(bg_lbl,text="STUDENT MANAGEMENT SYSTEM",font=("times new roman",37,"bold"),fg="blue",bg="white")
        lbl_title.place(x=0,y=0,width=1530,height=50)

        Manage_frame= Frame(bg_lbl,bd=2,relief=RIDGE,bg="white")
        Manage_frame.place(x=15,y=55,width=1500,height=560)


        # left frame
        DataLeftframe= LabelFrame(Manage_frame,bd=4,relief=RIDGE,padx=2,text="Student Information",font=("times new roman",12,"bold"),fg="red",bg="white")
        DataLeftframe.place(x=10,y=10,width=660,height=540)
        
        # image in left frame
        img_5= Image.open(r"college_images\3rd.jpg")
        img_5= img_5.resize((650,120),Image.ANTIALIAS)
        self.photoimg_5 = ImageTk.PhotoImage(img_5)

        my_img= Label(DataLeftframe,image=self.photoimg_5,bd=2,relief=RIDGE)
        my_img.place(x=0,y=0,width=650,height=120)

        # current course label frame Information
        std_lbl_info_frame= LabelFrame(DataLeftframe,bd=4,relief=RIDGE,padx=2,text="Current Course Information",font=("times new roman",12,"bold"),fg="red",bg="white")
        std_lbl_info_frame.place(x=0,y=120,width=650,height=115)

        DataRightframe=LabelFrame(Manage_frame,bd=4,relief=RIDGE,padx=2,text="Student Information",font=("times new roman",12,"bold"),fg="red",bg="white")
        DataRightframe.place(x=680,y=10,width=800,height=540)

         # current course label frame Information
        std_lbl_info_frame= LabelFrame(DataLeftframe,bd=4,relief=RIDGE,padx=2,text="Current Course Information",font=("times new roman",12,"bold"),fg="red",bg="white")
        std_lbl_info_frame.place(x=0,y=120,width=650,height=115)

        # labels and combobox
        # department
        lbl_dep= Label(std_lbl_info_frame,text="department",font=("arial",12,"bold"),bg="white")
        lbl_dep.grid(row=0,column=0,padx=2,sticky=W)

        combo_dep=ttk.Combobox(std_lbl_info_frame,textvariable=self.var_dep,font=("arial",12,"bold"),width=17,state="readonly")
        combo_dep["value"]=("Select Department","Computer Sc.","IT","Mechanical","Electrical","Civil")
        combo_dep.current(0)
        combo_dep.grid(row=0,column=1,padx=2,pady=10,sticky=W)

        # course
        course_std= Label(std_lbl_info_frame,font=("arial",12,"bold"),text="Courses:",bg="white")
        course_std.grid(row=0,column=2,sticky=W,padx=2,pady=10)

        com_txtcourse_std=ttk.Combobox(std_lbl_info_frame,textvariable=self.var_course,font=("arial",12,"bold"),width=17,state="readonly")
        com_txtcourse_std["value"]=("Select Courses:","B.Tech","MCA","B.E","M.TECH",)
        com_txtcourse_std.current(0)
        com_txtcourse_std.grid(row=0,column=3,padx=2,pady=10,sticky=W)

        
        #year
        cuurent_year= Label(std_lbl_info_frame,text="Year:",font=("arial",12,"bold"),bg="white")
        cuurent_year.grid(row=1,column=0,padx=2,pady=2,sticky=W)

        com_txt_cuurent_year=ttk.Combobox(std_lbl_info_frame,textvariable=self.var_year,font=("arial",12,"bold"),width=17,state="readonly")
        com_txt_cuurent_year["value"]=("Select Year","2020-2021","2021-2022","2022-2023")
        com_txt_cuurent_year.current(0)
        com_txt_cuurent_year.grid(row=1,column=1,padx=2,sticky=W)

        # Semester
        label_semester= Label(std_lbl_info_frame,text="Semester:",font=("arial",12,"bold"),bg="white")
        label_semester.grid(row=1,column=2,padx=2,pady=10,sticky=W)

        comSemester=ttk.Combobox(std_lbl_info_frame,textvariable=self.var_semester,font=("arial",12,"bold"),width=12,state="readonly")
        comSemester["value"]=("Select Semster","Sem-1","Sem-2")
        comSemester.current(0)
        comSemester.grid(row=1,column=3,padx=2,pady=10,sticky=W)

        # student class label information
        std_lbl_class_frame= LabelFrame(DataLeftframe,bd=4,relief=RIDGE,padx=2,text="Class Course Information",font=("times new roman",12,"bold"),fg="red",bg="white")
        std_lbl_class_frame.place(x=0,y=235,width=650,height=250)

        # Labels entry
        # ID
        lbl_id= Label(std_lbl_class_frame,text="StudentID:",font=("arial",12,"bold"),bg="white")
        lbl_id.grid(row=0,column=0,padx=2,pady=7,sticky=W)

        id_entry=ttk.Entry(std_lbl_class_frame,textvariable=self.var_std_id,font=("arial",12,"bold"),width=22)
        id_entry.grid(row=0,column=1,padx=2,pady=7,sticky=W)

        # Name
        lbl_name= Label(std_lbl_class_frame,text="Student Name:",font=("arial",11,"bold"),bg="white")
        lbl_name.grid(row=0,column=2,padx=2,pady=7,sticky=W)

        txt_name=ttk.Entry(std_lbl_class_frame,textvariable=self.var_std_name,font=("arial",11,"bold"),width=22)
        txt_name.grid(row=0,column=3,padx=2,pady=7,sticky=W)


        # Division
        lbl_div= Label(std_lbl_class_frame,text="Class Division:",font=("arial",11,"bold"),bg="white")
        lbl_div.grid(row=1,column=0,padx=2,pady=7,sticky=W)

        com_txt_div=ttk.Combobox(std_lbl_class_frame,textvariable=self.var_div,font=("arial",12,"bold"),width=18,state="readonly")
        com_txt_div["value"]=("Select Division","A","B","C")
        com_txt_div.current(0)
        com_txt_div.grid(row=1,column=1,padx=2,pady=7,sticky=W)

        # Roll No.
        lbl_roll= Label(std_lbl_class_frame,text="Roll No:",font=("arial",11,"bold"),bg="white")
        lbl_roll.grid(row=1,column=2,padx=2,pady=7,sticky=W)

        txt_roll=ttk.Entry(std_lbl_class_frame,textvariable=self.var_roll,font=("arial",11,"bold"),width=22)
        txt_roll.grid(row=1,column=3,padx=2,pady=7,sticky=W)
        
        # Gender
        lbl_gender= Label(std_lbl_class_frame,text="Gender:",font=("arial",11,"bold"),bg="white")
        lbl_gender.grid(row=2,column=0,padx=2,pady=7,sticky=W)

        com_txt_gender=ttk.Combobox(std_lbl_class_frame,textvariable=self.var_gender,font=("arial",12,"bold"),width=18,state="readonly")
        com_txt_gender["value"]=("Select Gender","Male","Female","Other")
        com_txt_gender.current(0)
        com_txt_gender.grid(row=2,column=1,padx=2,pady=7,sticky=W)

        # DOB
        lbl_dob= Label(std_lbl_class_frame,text="DOB:",font=("arial",11,"bold"),bg="white")
        lbl_dob.grid(row=2,column=2,padx=2,pady=7,sticky=W)

        txt_dob=ttk.Entry(std_lbl_class_frame,textvariable=self.var_dob,font=("arial",11,"bold"),width=22)
        txt_dob.grid(row=2,column=3,padx=2,pady=7,sticky=W)

        # E-Mail
        lbl_email= Label(std_lbl_class_frame,text="Email:",font=("arial",11,"bold"),bg="white")
        lbl_email.grid(row=3,column=0,padx=2,pady=7,sticky=W)

        txt_email=ttk.Entry(std_lbl_class_frame,textvariable=self.var_email,font=("arial",11,"bold"),width=22)
        txt_email.grid(row=3,column=1,padx=2,pady=7,sticky=W)

        # Phone Number
        lbl_phone= Label(std_lbl_class_frame,text="Phone No:",font=("arial",11,"bold"),bg="white")
        lbl_phone.grid(row=3,column=2,padx=2,pady=7,sticky=W)

        txt_phone=ttk.Entry(std_lbl_class_frame,textvariable=self.var_phone,font=("arial",11,"bold"),width=22)
        txt_phone.grid(row=3,column=3,padx=2,pady=7,sticky=W)

        # address
        lbl_adderss= Label(std_lbl_class_frame,text="Address:",font=("arial",11,"bold"),bg="white")
        lbl_adderss.grid(row=4,column=0,padx=2,pady=7,sticky=W)

        txt_adderss=ttk.Entry(std_lbl_class_frame,textvariable=self.var_address,font=("arial",11,"bold"),width=22)
        txt_adderss.grid(row=4,column=1,padx=2,pady=7,sticky=W)

        # teacher
        lbl_teacher= Label(std_lbl_class_frame,text="Teacher Name:",font=("arial",11,"bold"),bg="white")
        lbl_teacher.grid(row=4,column=2,padx=2,pady=7,sticky=W)

        txt_teacher=ttk.Entry(std_lbl_class_frame,textvariable=self.var_teacher,font=("arial",11,"bold"),width=22)
        txt_teacher.grid(row=4,column=3,padx=2,pady=7,sticky=W)

         # button frame
        Btn_frame= Frame(DataLeftframe,bd=2,relief=RIDGE,bg="white")
        Btn_frame.place(x=0,y=470,width=650,height=38)

        btn_Add= Button(Btn_frame,text="Save",command=self.add_data,font=("arial",11,"bold"),width=17,fg="white",bg="blue")
        btn_Add.grid(row=0,column=0,padx=1)

        btn_update=Button(Btn_frame,text="Update",command=self.Update_data,font=("arial",11,"bold"),width=17,fg="white",bg="blue")
        btn_update.grid(row=0,column=1,padx=1)

        btn_delete= Button(Btn_frame,text="Delete",command=self.delete_data,font=("arial",11,"bold"),width=17,fg="white",bg="blue")
        btn_delete.grid(row=0,column=2,padx=1)

        btn_reset= Button(Btn_frame,text="Reset",command=self.reset_data,font=("arial",11,"bold"),width=17,fg="white",bg="blue")
        btn_reset.grid(row=0,column=3,padx=1)

        
       
        # right frame
        DataRightframe=LabelFrame(Manage_frame,bd=4,relief=RIDGE,padx=2,text="Student Information",font=("times new roman",12,"bold"),fg="red",bg="white")
        DataRightframe.place(x=680,y=10,width=800,height=540)

        # Img 1st
        img_6= Image.open(r"college_images\6th.jpg")
        img_6 = img_6.resize((780,200),Image.ANTIALIAS)
        self.photoimg_6 = ImageTk.PhotoImage(img_6)

        my_img=Label(DataRightframe,image=self.photoimg_6,bd=2,relief=RIDGE)
        my_img.place(x=0,y=0,width=790,height=200)

        # search frame
        Search_frame=LabelFrame(DataRightframe,bd=4,relief=RIDGE,padx=2,text="Search Student Information",font=("times new roman",12,"bold"),fg="red",bg="white")
        Search_frame.place(x=0,y=200,width=790,height=60)


        Search_by= Label(Search_frame,text="Search By:",font=("arial",11,"bold"),bg="black",fg="red")
        Search_by.grid(row=0,column=0,padx=5,sticky=W)

        # search 
        self.var_com_search=StringVar()
        
        com_txt_search=ttk.Combobox(Search_frame,textvariable=self.var_com_search,font=("arial",12,"bold"),width=18,state="readonly")
        com_txt_search["value"]=("Select Option ","Roll","Phone","student_id")
        com_txt_search.current(0)
        com_txt_search.grid(row=0,column=1,padx=5,sticky=W)

        self.var_search=StringVar()

        txt_search=ttk.Entry(Search_frame,textvariable=self.var_search,font=("arial",11,"bold"),width=22)
        txt_search.grid(row=0,column=2,padx=5,sticky=W)

        
        btn_search= Button(Search_frame,command=self.search_data,text="Search",font=("arial",11,"bold"),width=14,fg="white",bg="blue")
        btn_search.grid(row=0,column=3,padx=5)

        btn_showAll= Button(Search_frame,command=self.fetch_data,text="Show All",font=("arial",11,"bold"),width=14,fg="white",bg="blue")
        btn_showAll.grid(row=0,column=4,padx=5)

        # *************** Student Table and Scroll bar **************
        table_frame= Frame(DataRightframe,bd=4,relief=RIDGE)
        table_frame.place(x=0,y=260,width=790,height=250)

        scroll_x= ttk.Scrollbar(table_frame,orient=HORIZONTAL)
        scroll_y=ttk.Scrollbar(table_frame,orient=VERTICAL)
        self.student_table=ttk.Treeview(table_frame,column=("dep","course",'year',"sem","id","name","div","roll","gender","dob","email","phone","address","teacher",),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)
        
        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)

        scroll_x.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)

        self.student_table.heading("dep",text="Department")
        self.student_table.heading("course",text="course")
        self.student_table.heading("year",text="Year")
        self.student_table.heading("sem",text="Semester")
        self.student_table.heading("id",text="StudentID")
        self.student_table.heading("name",text="Student Name")
        self.student_table.heading("div",text="Class Div")
        self.student_table.heading("roll",text="Roll No")
        self.student_table.heading("gender",text="Gender")
        self.student_table.heading("dob",text="DOB")
        self.student_table.heading("email",text="Email")
        self.student_table.heading("phone",text="Phone No")
        self.student_table.heading("address",text="Address")
        self.student_table.heading("teacher",text="Teacher Name")
       
        self.student_table["show"]="headings"


        self.student_table.column("dep",width=100)
        self.student_table.column("course",width=100)
        self.student_table.column("year",width=100)
        self.student_table.column("sem",width=100)
        self.student_table.column("id",width=100)
        self.student_table.column("name",width=100)
        self.student_table.column("div",width=100)
        self.student_table.column("roll",width=100)
        self.student_table.column("gender",width=100)
        self.student_table.column("dob",width=100)
        self.student_table.column("email",width=100)
        self.student_table.column("phone",width=100)
        self.student_table.column("address",width=100)
        self.student_table.column("teacher",width=100)

        self.student_table.pack(fill=BOTH,expand=1)
        self.student_table.bind("<ButtonRelease>",self.get_cursor)
        self.fetch_data()
        
    def add_data(self):
        if (self.var_dep.get()=="" or self.var_email.get()=="" or self.var_std_id.get()==""):
            messagebox.showerror("Error","All Fields are required",parent = self.root)
        else:
            try:
                conn=mysql.connector.connect(host="localhost",username="root",password="him@nshu0809",database="mydata")
                my_cursur=conn.cursor()
                my_cursur.execute("insert into student values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(
                                                                                                            self.var_dep.get(),
                                                                                                            self.var_course.get(),
                                                                                                            self.var_year.get(),
                                                                                                            self.var_semester.get(),
                                                                                                            self.var_std_id.get(),
                                                                                                            self.var_std_name.get(),
                                                                                                            self.var_div.get(),
                                                                                                            self.var_roll.get(),
                                                                                                            self.var_gender.get(),
                                                                                                            self.var_dob.get(),
                                                                                                            self.var_email.get(),
                                                                                                            self.var_phone.get(),
                                                                                                            self.var_address.get(),
                                                                                                            self.var_teacher.get()

                                                                                                    ))

                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Success","Student has been added!",parent=self.root)
            except Exception as es:
                messagebox.showerror("Error",f"Due To:{str(es)}",parent=self.root)

    # fetch function, to fetch the data from database and show to the screen
    def fetch_data(self):
        conn= mysql.connector.connect(host="localhost",username="root",password="him@nshu0809",database="mydata")
        my_cursur=conn.cursor()
        my_cursur.execute("select * from student")
        data = my_cursur.fetchall()
        if len(data)!=0:
            self.student_table.delete(*self.student_table.get_children())
            for i in data:
                self.student_table.insert("",END,values=i)
            conn.commit()
        conn.close()


     # Get cursor
    def get_cursor(self,event=""):
        cursor_row = self.student_table.focus()
        content = self.student_table.item(cursor_row)
        data = content["values"]

        self.var_dep.set(data[0])
        self.var_course.set(data[1])
        self.var_year.set(data[2])
        self.var_semester.set(data[3])
        self.var_std_id.set(data[4])
        self.var_std_name.set(data[5])
        self.var_div.set(data[6])
        self.var_roll.set(data[7])
        self.var_gender.set(data[8])
        self.var_dob.set(data[9])
        self.var_email.set(data[10])
        self.var_phone.set(data[11])
        self.var_address.set(data[12])
        self.var_teacher.set(data[13])



    def Update_data(self):
        if (self.var_dep.get()=="" or self.var_email.get()=="" or self.var_std_id.get()==""):
            messagebox.showerror("Error","All Fields are required",parent = self.root)
        else:
            try:
                update=messagebox.askyesno("update","Are you sure update this student data",parent = self.root)
                if update>0:
                      conn= mysql.connector.connect(host="localhost",username="root",password="him@nshu0809",database="mydata")
                      my_cursur=conn.cursor()
                      my_cursur.execute("update student set Dep=%s,course=%s,Year=%s,Semester=%s,Name=%s,Division=%s,Roll=%s,Gender=%s,Dob=%s,Email=%s,Phone=%s,Address=%s,Teacher=%s where student_id=%s",(
                                                                                                                                                                    self.var_dep.get(),
                                                                                                                                                                    self.var_course.get(),
                                                                                                                                                                    self.var_year.get(),
                                                                                                                                                                    self.var_semester.get(),
                                                                                                                                                                    self.var_std_name.get(),
                                                                                                                                                                    self.var_div.get(),
                                                                                                                                                                    self.var_roll.get(),
                                                                                                                                                                    self.var_gender.get(),
                                                                                                                                                                    self.var_dob.get(),
                                                                                                                                                                    self.var_email.get(),
                                                                                                                                                                    self.var_phone.get(),
                                                                                                                                                                    self.var_address.get(),
                                                                                                                                                                    self.var_teacher.get(),
                                                                                                                                                                    self.var_std_id.get()                                      
                                                                                                                                                                     ))
                else:
                    if not update:
                        return
                conn.commit()
                self.fetch_data()
                conn.close()

                messagebox.showinfo("Success","student successfully updated",parent=self.root)
            except Exception as es:
                messagebox.showerror("Error",f"Due To:{str(es)}",parent=self.root)

    # delete
    def delete_data(self):
        if self.var_std_id.get()=="":
             messagebox.showerror("Error","All Fields are required",parent = self.root)
        else:
            try:
                Delete = messagebox.askyesno("Delete","Are you sure to delete this student data",parent=self.root)
                if Delete>0:
                    conn= mysql.connector.connect(host="localhost",username="root",password="him@nshu0809",database="mydata")
                    my_cursur=conn.cursor()
                    sql="delete from student where student_id=%s"
                    value = (self.var_std_id.get()),
                    my_cursur.execute(sql,value)
                else:
                    if not Delete:
                        return
                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Delete","Your student data has been deleted",parent=self.root)
            except Exception as es:
                messagebox.showerror("Error",f"Due To:{str(es)}",parent=self.root)

    # Reset Button
    def reset_data(self):
        self.var_dep.set("Select Department")
        self.var_course.set("Select Course")
        self.var_year.set("Select Year")
        self.var_semester.set("Select Semester")
        self.var_std_id.set("")
        self.var_std_name.set("")
        self.var_div.set("Select Division")
        self.var_roll.set("")
        self.var_gender.set("")
        self.var_dob.set("")
        self.var_email.set("")
        self.var_phone.set("")
        self.var_address.set("")
        self.var_teacher.set("")

    # search data
    def search_data(self):
        if self.var_com_search.get()=="" or self.var_search.get()=="":
          messagebox.showerror("Error","All Fields are required",parent = self.root)
        else:
            try:
                conn= mysql.connector.connect(host="localhost",username="root",password="him@nshu0809",database="mydata")
                my_cursur=conn.cursor()
                my_cursur.execute("select * from student where " +str(self.var_com_search.get())+" LIKE '%"+str(self.var_search.get())+"%'")
                data = my_cursur.fetchall()

                if len(data)!=0:
                    self.student_table.delete(*self.student_table.get_children())
                    for i in data:
                        self.student_table.insert("",END,values=i)
                        conn.commit()
                conn.close()
            except Exception as es:
                messagebox.showerror("Error",f"Due To:{str(es)}",parent=self.root)


    # open image
    def open_img(self):
        fln= filedialog.askopenfilename(initialdir=os.getcwd(),title="open Images",filetypes=(("JPG File","*.jpg"),("PNG File","*.png"),("All Files","*.*")),parent=self.root)
        img= Image.open(fln)
        img_browse=img.resize((540,160),Image.ANTIALIAS)
        self.photoimg_browse = ImageTk.PhotoImage(img_browse)
        self.btn_1.config(image=self.photoimg_browse)

    def open_img_2(self):
        fln= filedialog.askopenfilename(initialdir=os.getcwd(),title="open Images",filetypes=(("JPG File","*.jpg"),("PNG File","*.png"),("All Files","*.*")),parent=self.root)
        img_1= Image.open(fln)
        img_browse_1=img_1.resize((540,160),Image.ANTIALIAS)
        self.photoimg_browse_1 = ImageTk.PhotoImage(img_browse_1)
        self.btn_2.config(image=self.photoimg_browse_1)


    def open_img_3(self):
        fln= filedialog.askopenfilename(initialdir=os.getcwd(),title="open Images",filetypes=(("JPG File","*.jpg"),("PNG File","*.png"),("All Files","*.*")),parent=self.root)
        img_2= Image.open(fln)
        img_browse_2=img_2.resize((540,160),Image.ANTIALIAS)
        self.photoimg_browse_2 = ImageTk.PhotoImage(img_browse_2)
        self.btn_3.config(image=self.photoimg_browse_2)
        














if __name__=="__main__":
    Main()
    
   
    