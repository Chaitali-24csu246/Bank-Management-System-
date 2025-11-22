# BANK MANAGEMENT SYSTEM
# FINAL BOARDS PROJECT COMPUTER SCIENCE
#mysql connector installed

import mysql.connector

#for password set password of your mysql everywhere in con
#con = mysql.connector.connect(host="localhost",user="root",password="",database="bankdb")
#cur = con.cursor()
#admin details: Password: Admin

try:
    con=mysql.connector.connect(
        host="localhost",
        user="root",
        password="Csq1P@ssw-d"
    )
    cur=con.cursor()
except:
    print("error in connecting to mysql :")
#opening database
try:
    cur.execute("create database if not exists bankdb")
except Exception as e:
    print("Problem making db!!", e)
#connect to database
try:
    con=mysql.connector.connect(
        host="localhost",
        user="root",
        password="Csq1P@ssw-d",
        database="bankdb"
    )
    cur=con.cursor()
except:
    print("Could not connect to database bankdb")
#create a main table if it doesn't exist
try:
    cur.execute("create table Accounts(Account_no int primary key, Name varchar(40), Balance float)")
except:
    pass   

#Sub table accnt type if it doesn't exist
try:
    cur.execute("""
        create table if not exists AccountType(
            Account_no int,
            Type varchar(40),
            InterestRate float,
            foreign key(Account_no) references Accounts(Account_no)
        )
    """)
except:
    print("problem creating AccountType table")

#Loan table
try:
    cur.execute("""
        create table if not exists Loans(
            LoanID int auto_increment primary key,
            Account_no int,
            LoanType varchar(40),
            LoanAmount float,
            foreign key(Account_no) references Accounts(Account_no)
        )
    """)
except:
    print("problem creating Loans table")

# ------------ INTERNAL HELPERS (USED INSIDE createAcc) ----------------

def createAccType(accno):
    print("\nChoose Account Type:")
    print("1. Savings")
    print("2. Regular")
    print("3. Student")
    t = input("Enter choice 1/2/3: ")

    if t=="1":
        acct = "Savings"
        intr = 3.5
    elif t=="2":
        acct = "Regular"
        intr = 2.0
    elif t=="3":
        acct = "Student"
        intr = 1.0
    else:
        print("Wrong input, by default your account is regular.")

    try:
        q = "insert into AccountType values(%s,%s,%s)"
        cur.execute(q,(accno, acct, intr))
        con.commit()
    except Exception as e:
        print("error storing account type:", e)


def createLoan(accno):
    print("\nLoan Section (optional):")
    ln = input("Do you want a loan? (y for yes, press any key for no): ")
    if ln.lower()!="y":
        return

    loan_amt = float(input("Enter loan amount: "))
    loan_type = input("Loan type (Home/Car/Personal/etc): ")

    try:
        q = "insert into Loans(Account_no, LoanType, LoanAmount) values(%s,%s,%s)"
        cur.execute(q,(accno, loan_type, loan_amt))
        con.commit()
    except Exception as e:
        print("loan error:", e)

def createAcc():
    print("\n ***Create new Account: ***\n")
    a =int(input("Enter account no: "))
    n =input("Enter name :   ")
    b =float(input("Enter opening balance: "))
    try:
        q = "insert into Accounts values(%s,%s,%s)"
        cur.execute(q,(a,n,b))
        con.commit()
        createAccType(a)
        createLoan(a)
        print("Account Created!!")
    except Exception as e:
        print("some error occured:", e)
def deposit():
    print("\n--- Deposit money ---")
    acc = int(input("Acc number plz: "))
    amt = float(input("Enter amount: "))

    cur.execute("select Balance from Accounts where Account_no=%s"%(acc,))
    d = cur.fetchone()

    if d==None:
        print("no such acc!!!")
        return

    nb = d[0] + amt

    cur.execute("update Accounts set Balance=%s where Account_no=%s"%(nb,acc))
    con.commit()
    print("Deposited ", amt, " new bal=", nb)


def withdraw():
    print("\n--- Withdraw money ---")
    accno = int(input("acc: "))
    am = float(input("amount: "))

    cur.execute("select Balance from Accounts where Account_no=%s"%(accno,))
    x = cur.fetchone()

    if x is None:
        print("no account found :(")
        return

    if x[0] < am:
        print("Not enough bal!!!")
        return

    newbal = x[0] - am

    cur.execute("update Accounts set Balance=%s where Account_no=%s"%(newbal, accno))
    con.commit()
    print("Done. balance=", newbal)

def updateAcc():
    print("\n-- UPDATE ACCOUNT DETAILS --")
    ac = int(input("Enter Account Number: "))

    # Check if account exists
    cur.execute("select * from Accounts where Account_no=%s"%(ac,))
    acc = cur.fetchone()
    if not acc:
        print("Account not found!")
        return

    print("\nWhat do you want to update?")
    print("1. Name")
    print("2. Account Type")
    print("3. Take a new loan")
    choice = input("Enter choice 1/2/3: ")

    if choice == "1":
        new_name = input("Enter new name: ")
        try:
            cur.execute("update Accounts set Name=%s where Account_no=%s",(new_name, ac))
            con.commit()
            print("Name updated successfully!")
        except Exception as e:
            print("Error updating name:", e)

    elif choice == "2":
        print("\nChoose new Account Type:")
        print("1. Savings")
        print("2. Regular")
        print("3. Student")
        t = input("Enter choice 1/2/3: ")
        if t=="1":
            acct = "Savings"
            intr = 3.5
        elif t=="2":
            acct = "Regular"
            intr = 2.0
        elif t=="3":
            acct = "Student"
            intr = 1.0
        else:
            print("Invalid input, keeping previous type.")
            return

        try:
            # Update or insert if not exists
            cur.execute("select * from AccountType where Account_no=%s"%(ac,))
            exists = cur.fetchone()
            if exists:
                cur.execute("update AccountType set Type=%s, InterestRate=%s where Account_no=%s",(acct, intr, ac))
            else:
                cur.execute("insert into AccountType values(%s,%s,%s)",(ac, acct, intr))
            con.commit()
            print("Account Type updated successfully!")
        except Exception as e:
            print("Error updating account type:", e)

    elif choice == "3":
        createLoan(ac)  # Reuse the loan creation function
    else:
        print("Invalid choice!")


def showdetails():
    print("\n-- Check Balance --")
    ac = int(input("acc no?? "))

    cur.execute("select * from Accounts where Account_no=%s"%(ac,))
    info = cur.fetchone()

    if info==None:
        print("wrong acc no or not exist")
        return
    else:
        print("Acc:", info[0], " Name:", info[1], " Balance:", info[2])

    # Account Type info
    try:
        cur.execute("select Type, InterestRate from AccountType where Account_no=%s"%(ac,))
        t = cur.fetchone()
        if t:
            print("Account Type:", t[0])
            print("Interest Rate:", t[1])
    except:
        pass

    # Loans info
    try:
        cur.execute("select LoanType, LoanAmount from Loans where Account_no=%s"%(ac,))
        loans = cur.fetchall()
        if loans:
            print("\n-- LOAN DETAILS --")
            for L in loans:
                print("Loan Type:", L[0], " Amount:", L[1])
    except:
        pass



def deleteAcc():
    print("\n-- DELETE ACC --")
    a = int(input("Enter acc no: "))

    cur.execute("select * from Accounts where Account_no=%s"%(a,))
    dd = cur.fetchone()

    if dd==None:
        print("account dont exist")
        return

    # Delete from child tables first
    try:
        cur.execute("delete from AccountType where Account_no=%s"%(a,))
        cur.execute("delete from Loans where Account_no=%s"%(a,))
    except:
        pass

    cur.execute("delete from Accounts where Account_no=%s"%(a,))
    con.commit()
    print("Account deleted !!!")

def payLoan():
    print("\n -- Pay Loan --")
    try:
        a = int(input("Enter account number: "))
    except ValueError:
        print("Invalid input! Account number must be an integer.")
        return

    cur.execute("select LoanID, LoanType, LoanAmount from Loans where Account_no=%s", (a,))
    data = cur.fetchall()

    if not data:
        print("No loans found for this account!")
        return

    print("\nLoans for this account:")
    for d in data:
        print(f"LoanID: {d[0]} | Type: {d[1]} | Amount: {d[2]}")

    try:
        lid = int(input("\nEnter LoanID to pay: "))
    except ValueError:
        print("Invalid input! LoanID must be an integer.")
        return

    try:
        amt = float(input("Enter amount paying: "))
    except ValueError:
        print("Invalid input! Amount must be a number.")
        return

    cur.execute("select LoanAmount from Loans where LoanID=%s", (lid,))
    old = cur.fetchone()

    if old is None:
        print("Invalid LoanID!")
        return

    newamt = old[0] - amt
    if newamt < 0:
        newamt = 0

    cur.execute("update Loans set LoanAmount=%s where LoanID=%s", (newamt, lid))
    con.commit()
    print("Loan Updated. Remaining Amount =", newamt)
#file handling part
def adminReport():
    print("\n--- Generating Bank Report ---")
    filename = "BankReport.txt"
    try:
        with open(filename, "w") as f:
            f.write("========= BANK DATABASE REPORT =========\n\n")

            # Accounts Table
            f.write("---- ACCOUNTS TABLE ----\n")
            cur.execute("select * from Accounts")
            accounts = cur.fetchall()
            if accounts:
                for a in accounts:
                    f.write(f"Account_no: {a[0]}, Name: {a[1]}, Balance: {a[2]}\n")
            else:
                f.write("No records in Accounts table\n")
            f.write("\n")

            # AccountType Table
            f.write("---- ACCOUNTTYPE TABLE ----\n")
            cur.execute("select * from AccountType")
            types = cur.fetchall()
            if types:
                for t in types:
                    f.write(f"Account_no: {t[0]}, Type: {t[1]}, InterestRate: {t[2]}\n")
            else:
                f.write("No records in AccountType table\n")
            f.write("\n")

            # Loans Table
            f.write("---- LOANS TABLE ----\n")
            cur.execute("select * from Loans")
            loans = cur.fetchall()
            if loans:
                for l in loans:
                    f.write(f"LoanID: {l[0]}, Account_no: {l[1]}, LoanType: {l[2]}, LoanAmount: {l[3]}\n")
            else:
                f.write("No records in Loans table\n")
            f.write("\n")

        print(f"Report generated successfully! Saved as {filename}")
    except Exception as e:
        print("Error generating report:", e)

#function in function nesting using choice and mainmenu
def choice(ch):
    if ch=='1':
        createAcc()
    elif ch=='2':
        deposit()
    elif ch=='3':
        withdraw()
    elif ch=='4':
        showdetails()
    elif ch=='5':
        deleteAcc()
    elif ch=='6':
        print("Thank you \n Program Ending\n ****************************************")
        exit()
    elif ch=='7':
        payLoan()
    elif ch=='8':
        admin_password = input("Enter Admin password: ")
        if admin_password == "Admin":  
            adminReport()
        else:
            print("Incorrect password!")
    elif ch=='9':
        updateAcc()
    else:
        print("invalid choice, try again!!")


# main menu
def mainmenu():
    print("\n=========== BANK MENU ===========")
    print("1. Create Account")
    print("2. Deposit")
    print("3. Withdraw")
    print("4. Show Details")
    print("5. Delete Account")
    print("6. EXIT")
    print("7. Pay Loan")
    print("8. Admin: See details")
    print("9. Account details update(Add loan, change accnt type, change name)")  
    print("================================")

    ch = input("enter choice: ")
    choice(ch)

while True:
    mainmenu()


#to do
#note: add exception handling (done)
#note: databse \importing google
#note:report by 19 dec extended (done)
#note: remove Bhoomika's section )(done)
#note: make mainmenu a func(done)
#note:show nested functions(done)
#note: add formatting (done)
#note: add dependent tables and show fk(done)
#note: add admin setting for all details use file handling.
