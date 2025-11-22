# Bank Management System

## Board project

A simple Python-based Bank Management System using MySQL and file handling. The system allows users to manage accounts, deposits, withdrawals, loans, and generate admin reports.

## Features

Create new bank accounts

Deposit and withdraw money

Check account details, including account type and loans

Take new loans or pay off existing loans

Update account details (name, account type, add loans)

Delete accounts

Generate admin reports of all accounts, account types, and loans (saved as a text file)

Input validation and error handling to prevent crashes

## Technologies Used

Python 3.x

MySQL – stores account, account type, and loan information

File Handling – generates admin reports as BankReport.txt

mysql-connector-python library for database connection

## Setup and Installation

### Install Python dependencies:

pip install mysql-connector-python


### Update MySQL credentials in the script:

con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="YOUR_PASSWORD"
)


### Run the program:

python bank_management_system.py


## Main Menu Options:

1. Create Account
2. Deposit
3. Withdraw
4. Show Details
5. Delete Account
6. Exit
7. Pay Loan
8. Admin: See Details
9. Update Account Details (Change Name, Account Type, Add Loan)


### Admin Password:
Default password: Admin

## Notes

* Ensure MySQL server is running before starting the program.

* The program automatically creates the bankdb database and required tables if they don’t exist.

* Admin reports are saved as BankReport.txt in the working directory.
