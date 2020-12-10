import redis
import time
from random import randint
from datetime import datetime, date, timedelta
from clear_screen import clear
import base64
import os


# WIP
def get_Interest():
    time.sleep(2)
    input("* Press Enter to continue...")
    menu()


def checkDuplicateAccount():
    if r.exists(str(name)):
        r.mset({gather_Email: time.time(), gather_Mobile: time.time()})
        print('* Duplicate Accounts are not Permitted, Goodbye!')
        time.sleep(1)
        exit()
    else:
        pass
    if r.exists(gather_Email) or r.exists(gather_Mobile):
        r.set(str(name), time.time())
        print('* Duplicate Accounts are not Permitted, Goodbye!')
        time.sleep(1)
        exit()
    else:
        r.mset({gather_Email: time.time(), gather_Mobile: time.time()})


def logOut():
    clear()
    now = datetime.now()
    r.mset({
        str(name) + '_lastLoginDate': str(date.today()),
        str(name) + '_lastLoginTime': now.strftime("%H:%M:%S"),
        str(name) + '_lastLogin': time.time()
    })
    time.sleep(1)
    print('* Your session lasted:', round(time.time() - login_Start),
          'Seconds.')
    time.sleep(1)
    print('* Closing Balance:',
          "${:,.2f}".format(float(r.get(str(name) + '_balance'))) + ',',
          '* Savings Balance is:', "${:,.2f}".format(
              float(r.get(str(name) + '_savings'))))
    time.sleep(1)
    print('* Thank You for banking with WAIO Bank *,', str(name).title() + '.')
    time.sleep(1)
    print("{:*^20}".format('ＷＡＩＯ Ｂａｎｋ ｖ１.０'))
    exit()


# WIP
def run_Loan():
    print('A WIP')


def run_Delete():
    print('* Alert * Reset in progress, please wait... ')
    mobile = r.get(str(name) + '_mobile')
    email = r.get(str(name) + '_email')
    if r.exists(email):
        r.delete(str(email))
    if r.exists(mobile):
        r.delete(str(mobile))
    for key in r.scan_iter(match=f"*{str(name)}*"):
        time.sleep(0.2)
        r.delete(key)
    print('* Account, reset, please click "Run" and sign up!')
    print('* Your session lasted:', round(time.time() - login_Start),
          'Seconds.')
    time.sleep(1)
    exit()


def menu():
    clear()
    menu = True
    while menu == True:
        if float(r.get(str(name) + '_balance')) <= 0 and float(
                r.get(str(name) + '_savings')) <= 0:
            print('* ALERT *: Oh No, You have no money left,',
                  str(str(name)) + '!')
            time.sleep(1)
            print('* Emergency Option *')
            time.sleep(0.5)
            print(
                '* Enter[1]-Reset or [2]-Request a loan based on your Transactions.'
            )
            time.sleep(0.5)
            relief_Option = int(input('* or [3] to Exit : '))
            if relief_Option == 1:
                print('* You have Opted for a Reset.')
                time.sleep(1)
                reset_Confirm = int(
                    input("* Enter[1] to Confirm Reset account...: "))
                if reset_Confirm == 1:
                    run_Delete()
                else:
                    pass
            elif relief_Option == 2:
                print('* You have Opted for a Loan')
                time.sleep(2)
                input("* Press Enter to apply for Loan.")
                loan_Confirm = input(
                    "* Enter[1] to Confirm Request for a Loan...")
                if loan_Confirm == 1:
                    run_Loan()
                else:
                    pass
            elif relief_Option == 3:
                logOut()
            else:
                print('* That is an invalid option, try again please.')
        print('* Your Account Balance is:', "${:,.2f}".format(
            float(r.get(str(name) + '_balance'))), 'and Savings Balance is:',
              "${:,.2f}".format(float(r.get(str(name) + '_savings'))))
        time.sleep(1)
        print(
            '* MAIN MENU * [1]-Help, [2]-Savings, [3]-Statement, [4]-Gamble, [5]-Log Out *: '
        )
        if r.get(str(name) + '_status') == "admin":
            print('* For Administrator Menu, use Admin or admin * :')
        choice = input("* Please select an option: ").strip()
        if choice == "1" or choice == "Help" or choice == "help":
            menu = False
            Help()
        elif choice == "2" or choice == "Savings" or choice == "savings":
            menu = False
            Savings()
        elif choice == "3" or choice == "Statement" or choice == "statement":
            menu = False
            Statement()
        elif choice == "4" or choice == "Gamble" or choice == "gamble":
            menu = False
            Gamble()
        elif choice == "5" or choice == "Quit" or choice == "quit" or choice == "Logout" or choice == "logout" or choice == "Log Out" or choice == "log out" or choice == "Exit" or choice == "exit":
            menu = False
            logOut()
        elif choice == "Admin" or choice == "admin" and r.get(
                str(name) + '_status') == "admin":
            # Admin Menu
            print('* Secret Admin Menu')
            time.sleep(2)
            Admin()
        else:
            print('* Invalid input. Please try again.')


# Admin system - WIP
def Admin():
    print('* A WIP')
    time.sleep(2)
    menu()


# Gamble System
def Gamble():
    balance = r.get(str(name) + '_balance')
    print('* You have a 40% chance in winning,')
    time.sleep(0.5)
    print('* If you lose, you lose the amount gambled,')
    time.sleep(0.5)
    print('* If you win, you can win between 1-3 times the amount bet.')
    time.sleep(0.5)
    gamble_Amount = int(
        input(
            '* How much would you like to Gamble ? or (9) - Back to Main Menu: '
        ))
    if gamble_Amount == 9:
        menu()
    while gamble_Amount > int(balance):
        print('* You cannot gamble more than you have', 'You entered,',
              "${:,.2f}".format(float(gamble_Amount)), 'but only have,',
              "${:,.2f}".format(float(balance)))
        time.sleep(2)
        gamble_Amount = int(input('* How much would you like to Gamble ?: '))
    else:
        rand_Check = randint(1, 10)
        r.incr(str(name) + '_transactions')
        if rand_Check >= 6:
            rand_Win = randint(1, 3)
            winnings = gamble_Amount * rand_Win
            print('* Congratulations, You won', "${:,.2f}".format(
                float(winnings)))
            r.incr(str(name) + '_balance', winnings)
            time.sleep(2)
            input("* Press Enter to continue...")
        else:
            print('* Bad luck, You lost', "${:,.2f}".format(
                float(gamble_Amount)))
            r.decr(str(name) + '_balance', gamble_Amount)
            time.sleep(2)
            input("* Press Enter to continue...")
    menu()


# Savings System
def Savings():
    savings = r.get(str(name) + '_savings')
    balance = r.get(str(name) + '_balance')
    print('* You have',
          "${:,.2f}".format(float(savings)), 'in your savings account earning',
          r.get(str(name) + '_interestRate'), '% daily Compound interest.')
    # get_Interest()
    print('* You have', "${:,.2f}".format(float(balance)),
          'in your current bank account.')
    time.sleep(2)
    print('* SAVINGS MENU * ')
    n = int(
        input(
            '* Press [1]-Add to Savings, [2] Withdraw from Savings, [3]-Main Menu: '
        ))
    if n == 1:
        print('* Current Available Balance:', "${:,.2f}".format(
            float(balance)))
        savings_Amount = int(input('* Enter Amount to add to Savings ?: '))
        if savings_Amount > int(balance):
            print('* You have insufficient funds, please try a lesser amount')
            time.sleep(2)
        else:
            r.incr(str(name) + '_transactions')
            r.incr(str(name) + '_savings', savings_Amount)
            r.decr(str(name) + '_balance', savings_Amount)
            print('* Savings Balance is now', "${:,.2f}".format(
                float(r.get(str(name) + '_savings'))))
            time.sleep(2)
    if n == 2:
        print('* Current Savings Balance:', "${:,.2f}".format(float(savings)))
        savings_Withdraw = int(
            input('*** Enter Amount to Withdraw from Savings ?: '))
        if savings_Withdraw > int(savings):
            print(
                '* You have insufficient funds in Savings, please try a lesser amount'
            )
            time.sleep(2)
            input("* Press Enter to continue...")
        else:
            r.incr(str(name) + '_transactions')
            r.decr(str(name) + '_savings', savings_Withdraw)
            r.incr(str(name) + '_balance', savings_Withdraw)
            print('* Savings Balance is now', "${:,.2f}".format(
                float(r.get(str(name) + '_savings'))))
            time.sleep(2)
    menu()


# Statement System - WIP
def Statement():
    savings = r.get(str(name) + '_savings')
    balance = r.get(str(name) + '_balance')
    interestRate = r.get(str(name) + '_interestRate')
    transactions = r.get(str(name) + '_transactions')
    signUpDate = r.get(str(name) + '_signUpDate')
    signUpTime = r.get(str(name) + '_signUpTime')
    lastLoginDate = r.get(str(name) + '_lastLoginDate')
    lastLoginTime = r.get(str(name) + '_lastLoginTime')
    logins = r.get(str(name) + '_logins')
    print('* Available Balance:', "${:,.2f}".format(float(balance)) + ',',
          'Savings Balance:', "${:,.2f}".format(float(savings)), 'earning',
          interestRate, '% daily Compound interest.')
    time.sleep(1)
    # Calculate Interest
    print('---')
    # get_Interest()
    time.sleep(1)
    print('---')
    print('* Number of Transactions:',
          str(transactions) + ',', 'Number of Logged Logins:', logins)
    time.sleep(1)
    print('---')
    print('* Last Login Date and Time:', lastLoginDate,
          str(lastLoginTime) + ',', 'Registration Date and Time:', signUpDate,
          signUpTime)
    time.sleep(2)
    input("* Press Enter to continue...")
    menu()


# Help System - WIP
def Help():
    print('* Welcome to the Help System')
    time.sleep(2)
    input("* Press Enter to continue...")
    menu()


def welcome():
    print("-----------------------------------------------")
    print("********** 𝚆𝚎𝚕𝚌𝚘𝚖𝚎 𝚝𝚘 𝚆𝙰𝙸𝙾 𝙱𝚊𝚗𝚔 ********** ")
    print("-----------------------------------------------")
    code = randint(1, 10)
    code1 = randint(1, 10)
    code_ans = code + code1
    code_Error = 0
    code_Check = 0
    while code_ans != code_Check:
        print('* Security Code is:', code, '+', code1, '= ?')
        code_Check = int(
            input('* Calculate Security Code Correctly to continue: '))
        code_Error += 1
        if code_Check == code_ans:
            print('* Security Code Correctly Calculated.')
        else:
            if code_Error == 3:
                print('* Incorrect Security Code, Goodbye!')
                print('* Your session lasted:',
                      round(time.time() - login_Start), 'Seconds.')
                exit()
            print('* Incorrect Security Code, You have', 3 - code_Error,
                  'attempts left.')
    pin = 0
    pin_Error = 0
    if r.exists(str(name) + '_pin'):
        print('*', str(name).title(),'is registered, if this is you...')
        while pin != r.get(str(name) + '_pin'):
            pin = input('* Please Enter Your Pin to continue: ')
            pin_Error += 1
            if pin == r.get(str(name) + '_pin'):
                r.incr(str(name) + '_logins')
                print('* Pin Accepted, Welcome back', str(name).title())
                time.sleep(2)
                menu()
            else:
                if pin_Error == 3:
                    print('* Incorrect Pin Code, Goodbye!')
                    print('* Your session lasted:',
                          round(time.time() - login_Start), 'Seconds.')
                    exit()
                print('* Incorrect Pin Code, You have', 3 - pin_Error,
                      'attempts left.')
    else:
        decide = False
        while decide == False:
            print('* Notice: * No Bank Account Detected.')
            time.sleep(0.5)
            print('* Would you like one ?')
            decision = input('* Y/y/Yes/yes or N/n/No/no: ')
            if decision == 'N' or decision == 'n' or decision == 'no' or decision == 'No':
                print('* No problem, Goodbye!')
                exit()
            elif decision == 'Y' or decision == 'y' or decision == 'yes' or decision == 'Yes':
                clear()
                print('* Good choice and welcome to WAIO Bank,',
                      str(name).title() + '!')
                decide = True
            else:
                print(
                    "* Invalid input. Select one of the options correctly please."
                )
        pin = input('* Setup a Pin to Register: ')
        pin_Check = 0
        while pin_Check != pin:
            pin_Check = input('* Please Confirm Pin: ')
            clear()
        print('* Pin saved successfully.')
        global gather_Email
        gather_Email = input('* Please Enter your Email Address: ')
        email_Check = 0
        while email_Check != gather_Email:
            email_Check = input('* Please Confirm Email: ')
        print('* Email address saved successfully.')
        clear()
        global gather_Mobile
        gather_Mobile = input('* Please Enter your Mobile Number: ')
        mobile_Check = 0
        while mobile_Check != gather_Mobile:
            mobile_Check = input('* Please Confirm Mobile: ')
        print('* Mobile number saved successfully.')
        checkDuplicateAccount()
        gift = randint(1, 100)
        print('* You have been gifted:', "${:,.2f}".format(float(gift)),
              'to start your Account Balance.')
        now = datetime.now()
        r.mset({
            str(name) + '_pin': pin,
            str(name) + '_balance': gift,
            str(name) + '_transactions': 0,
            str(name) + '_savings': 0,
            str(name) + '_interestRate': randint(1, 5),
            str(name) + '_signUpDate': str(date.today()),
            str(name) + '_lastLoginDate': str(date.today()),
            str(name) + '_signUpTime': now.strftime("%H:%M:%S"),
            str(name) + '_lastLoginTime': now.strftime("%H:%M:%S"),
            str(name) + '_lastLogin': time.time(),
            str(name) + '_lastBatchRun': time.time(),
            str(name) + '_logins': 1,
            str(name) + '_email': gather_Email,
            str(name) + '_mobile': gather_Mobile,
            str(name) + '_status': 'member'
        })
        time.sleep(1)
        input("* Press Enter to continue...")
        menu()


def main():
    host_message = 'cmVkaXMtMTQ3MjYuYzg0LnVzLWVhc3QtMS0yLmVjMi5jbG91ZC5yZWRpc2xhYnMuY29t'
    host_bytes = host_message.encode('ascii')
    hostm_bytes = base64.b64decode(host_bytes)
    global ghost
    ghost = hostm_bytes.decode('ascii')
    port_message = 'MTQ3MjY='
    port_bytes = port_message.encode('ascii')
    portm_bytes = base64.b64decode(port_bytes)
    global gport
    gport = portm_bytes.decode('ascii')
    db_message = 'WjByRnZ0OEwzdVBUMTV3eFBGQndDY1NCaW9KT25BcVU='
    db_bytes = db_message.encode('ascii')
    dbm_bytes = base64.b64decode(db_bytes)
    global gdb
    gdb = dbm_bytes.decode('ascii')
    intialise()


def intialise():
    try:
        global r
        r = redis.StrictRedis(
            host=ghost,
            port=gport,
            password=gdb,
            db=0,
            decode_responses=True)
        global name
        print("{:*^20}".format('ＷＡＩＯ Ｂａｎｋ ｖ１.０'))
        while True:
            name = input('* Enter Username to Log In: ')
            if name and name.isalpha():
                name = name.lower()
                global login_Start
                login_Start = time.time()
                clear()
                welcome()
            elif name and name.isdigit():
                print('* Please use Alphabet characters only')
            else:
                print('* Only Alphabet Usernames are allowed.')           
    except Exception as e:
        print(e)    


if __name__ == '__main__':
    main()
else:
    print('Module running')
    #Run as module
