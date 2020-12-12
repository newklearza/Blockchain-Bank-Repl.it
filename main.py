import redis
import time
from random import randint
import base64
import re
from datetime import datetime, date
from clear_screen import clear

# WIP
def get_interest():
    time.sleep(2)
    input("* Press Enter to continue...")
    menu()


def check_duplicate_account():
    if r.exists(str(uname)):
        r.mset({gather_email: time.time(), gather_mobile: time.time()})
        print("* Duplicate Accounts are not Permitted, Goodbye!")
        time.sleep(1)
        intialise()
    else:
        pass
    if r.exists(gather_email) or r.exists(gather_mobile):
        r.set(str(uname), time.time())
        print("* Duplicate Accounts are not Permitted, Goodbye!")
        time.sleep(1)
        intialise()
    else:
        r.mset({gather_email: time.time(), gather_mobile: time.time()})


def log_out():
    clear()
    now = datetime.now()
    r.mset(
        {
            str(uname) + "_last_login_date": str(date.today()),
            str(uname) + "_last_login_time": now.strftime("%H:%M:%S"),
            str(uname) + "_lastLogin": time.time(),
        }
    )
    time.sleep(1)
    print("* Your session lasted:", round(time.time() - login_start), "Seconds.")
    time.sleep(1)
    print(
        "* Closing Balance:",
        "${:,.2f}".format(float(r.get(str(uname) + "_balance"))) + ",",
        "* Savings Balance is:",
        "${:,.2f}".format(float(r.get(str(uname) + "_savings"))),
    )
    time.sleep(1)
    print("* Thank You for banking with WAIO Bank *,", str(uname).title() + ".")
    time.sleep(1)
    print("{:*^20}".format("WAIO Bank V1.0"))
    intialise()


# WIP
def run_loan():
    print("A WIP")


def run_delete():
    print("* Alert * Reset in progress, please wait... ")
    mobile = r.get(str(uname) + "_mobile")
    email = r.get(str(uname) + "_email")
    if r.exists(email):
        r.delete(str(email))
    if r.exists(mobile):
        r.delete(str(mobile))
    for key in r.scan_iter(match=f"*{str(uname)}*"):
        time.sleep(0.2)
        r.delete(key)
    print('* Account, reset, please click "Run" and sign up!')
    print("* Your session lasted:", round(time.time() - login_start), "Seconds.")
    time.sleep(1)
    intialise()


def menu():
    clear()
    menu = True
    while menu == True:
        if (
            float(r.get(str(uname) + "_balance")) <= 0
            and float(r.get(str(uname) + "_savings")) <= 0
            ):
            print("* ALERT *: Oh No, You have no money left,", str(uname) + "!")
            time.sleep(1)
            print("* Emergency Option *")
            time.sleep(0.5)
            print("* Enter[1]-Reset or [2]-Request a loan based on your Transactions.")
            time.sleep(0.5)
            relief_option = int(input("* or [3] to Exit : "))
            if relief_option == 1:
                print("* You have Opted for a Reset.")
                time.sleep(1)
                reset_Confirm = int(input("* Enter[1] to Confirm Reset account...: "))
                if reset_Confirm == 1:
                    run_delete()
                else:
                    pass
            elif relief_option == 2:
                print("* You have Opted for a Loan")
                time.sleep(2)
                input("* Press Enter to apply for Loan.")
                loan_confirm = input("* Enter[1] to Confirm Request for a Loan...")
                if loan_confirm == 1:
                    run_loan()
                else:
                    pass
            elif relief_option == 3:
                log_out()
            else:
                print("* That is an invalid option, try again please.")
        print(
            "* Your Account Balance is:",
            "${:,.2f}".format(float(r.get(str(uname) + "_balance"))),
            "and Savings Balance is:",
            "${:,.2f}".format(float(r.get(str(uname) + "_savings"))),
        )
        time.sleep(1)
        print(
            "* MAIN MENU * [1]-Help, [2]-Savings, [3]-Statement, [4]-Gamble, [5]-Log Out *: "
        )
        if r.get(str(uname) + "_status") == "admin":
            print("* For Administrator Menu, use Admin or admin * :")
        choice = input("* Please select an option: ").strip()
        if choice == "1" or choice == "Help" or choice == "help":
            menu = False
            help()
        elif choice == "2" or choice == "Savings" or choice == "savings":
            menu = False
            savings()
        elif choice == "3" or choice == "Statement" or choice == "statement":
            menu = False
            statement()
        elif choice == "4" or choice == "Gamble" or choice == "gamble":
            menu = False
            gamble()
        elif (
            choice == "5"
            or choice == "Quit"
            or choice == "quit"
            or choice == "Logout"
            or choice == "logout"
            or choice == "Log Out"
            or choice == "log out"
            or choice == "Exit"
            or choice == "exit"
            ):
            menu = False
            log_out()
        elif (
            choice == "Admin"
            or choice == "admin"
            and r.get(str(uname) + "_status") == "admin"
            ):
            # Admin Menu
            print("* Secret Admin Menu")
            time.sleep(2)
            admin()
        else:
            print("* Invalid input. Please try again.")


# admin system - WIP
def admin():
    print("* A WIP")
    time.sleep(2)
    menu()


# Gamble System
def gamble():
    balance = r.get(str(uname) + "_balance")
    print("* You have a 40% chance in winning,")
    time.sleep(0.5)
    print("* If you lose, you lose the amount gambled,")
    time.sleep(0.5)
    print("* If you win, you can win between 1-3 times the amount bet.")
    time.sleep(0.5)
    gamble_amount = int(
        input("* How much would you like to Gamble ? or (9) - Back to Main Menu: ")
    )
    if gamble_amount == 9:
        menu()
    while gamble_amount > int(balance):
        print(
            "* You cannot gamble more than you have",
            "You entered,",
            "${:,.2f}".format(float(gamble_amount)),
            "but only have,",
            "${:,.2f}".format(float(balance)),
        )
        time.sleep(2)
        gamble_amount = int(input("* How much would you like to Gamble ?: "))
    else:
        rand_check = randint(1, 10)
        r.incr(str(uname) + "_transactions")
        if rand_check >= 6:
            rand_win = randint(1, 3)
            winnings = gamble_amount * rand_win
            print("* Congratulations, You won", "${:,.2f}".format(float(winnings)))
            r.incr(str(uname) + "_balance", winnings)
            time.sleep(2)
            input("* Press Enter to continue...")
        else:
            print("* Bad luck, You lost", "${:,.2f}".format(float(gamble_amount)))
            r.decr(str(uname) + "_balance", gamble_amount)
            time.sleep(2)
            input("* Press Enter to continue...")
    menu()


# Savings System
def savings():
    savings = r.get(str(uname) + "_savings")
    balance = r.get(str(uname) + "_balance")
    print(
        "* You have",
        "${:,.2f}".format(float(savings)),
        "in your savings account earning",
        r.get(str(uname) + "_interest_rate"),
        "% daily Compound interest.",
    )
    # get_interest()
    print(
        "* You have", "${:,.2f}".format(float(balance)), "in your current bank account."
    )
    time.sleep(2)
    print("* SAVINGS MENU * ")
    savings_menu = int(
        input("* Press [1]-Add to Savings, [2] Withdraw from Savings, [3]-Main Menu: ")
    )
    if savings_menu == 1:
        print("* Current Available Balance:", "${:,.2f}".format(float(balance)))
        savings_amount = int(input("* Enter Amount to add to Savings ?: "))
        if savings_amount > int(balance):
            print("* You have insufficient funds, please try a lesser amount")
            time.sleep(2)
        else:
            r.incr(str(uname) + "_transactions")
            r.incr(str(uname) + "_savings", savings_amount)
            r.decr(str(uname) + "_balance", savings_amount)
            print(
                "* Savings Balance is now",
                "${:,.2f}".format(float(r.get(str(uname) + "_savings"))),
            )
            time.sleep(2)
    if savings_menu == 2:
        print("* Current Savings Balance:", "${:,.2f}".format(float(savings)))
        savings_Withdraw = int(input("*** Enter Amount to Withdraw from Savings ?: "))
        if savings_Withdraw > int(savings):
            print(
                "* You have insufficient funds in Savings, please try a lesser amount"
            )
            time.sleep(2)
            input("* Press Enter to continue...")
        else:
            r.incr(str(uname) + "_transactions")
            r.decr(str(uname) + "_savings", savings_Withdraw)
            r.incr(str(uname) + "_balance", savings_Withdraw)
            print(
                "* Savings Balance is now",
                "${:,.2f}".format(float(r.get(str(uname) + "_savings"))),
            )
            time.sleep(2)
    menu()


# Statement System - WIP
def statement():
    savings = r.get(str(uname) + "_savings")
    balance = r.get(str(uname) + "_balance")
    interest_rate = r.get(str(uname) + "_interest_rate")
    transactions = r.get(str(uname) + "_transactions")
    sign_up_date = r.get(str(uname) + "_sign_up_date")
    sign_up_time = r.get(str(uname) + "_sign_up_time")
    last_login_date = r.get(str(uname) + "_last_login_date")
    last_login_time = r.get(str(uname) + "_last_login_time")
    logins = r.get(str(uname) + "_logins")
    print(
        "* Available Balance:",
        "${:,.2f}".format(float(balance)) + ",",
        "Savings Balance:",
        "${:,.2f}".format(float(savings)),
        "earning",
        interest_rate,
        "% daily Compound interest.",
    )
    time.sleep(1)
    # Calculate Interest
    print("---")
    # get_interest()
    time.sleep(1)
    print("---")
    print(
        "* Number of Transactions:",
        str(transactions) + ",",
        "Number of Logged Logins:",
        logins,
    )
    time.sleep(1)
    print("---")
    print(
        "* Last Login Date and Time:",
        last_login_date,
        str(last_login_time) + ",",
        "Registration Date and Time:",
        sign_up_date,
        sign_up_time,
    )
    time.sleep(2)
    input("* Press Enter to continue...")
    menu()


# Help System - WIP
def help():
    print("* Welcome to the Help System")
    time.sleep(2)
    input("* Press Enter to continue...")
    menu()
    
def existing_user():
    print("*", str(uname).title(), "is registered, if this is you...")
    while pin != r.get(str(uname) + "_pin"):
        pin = input("* Please Enter Your Pin to continue: ")
        pin_error += 1
        if pin == r.get(str(uname) + "_pin"):
            r.incr(str(uname) + "_logins")
            print("* Pin Accepted, Welcome back", str(uname).title())
            time.sleep(2)
            menu()
        else:
            if pin_error == 3:
                print("* Incorrect Pin Code, Goodbye!")
                print(
                    "* Your session lasted:",
                    round(time.time() - login_start),
                    "Seconds.",
                )
                intialise()
            print("* Incorrect Pin Code, You have", 3 - pin_error, "attempts left.")
        
def isValid(s): 
    Pattern = re.compile("(0/27/+27)?[6-8][0-10]{10}") 
    return Pattern.match(s)


def new_user():
    decide = 0
    while decide == 0:
        print("* Notice: * No Bank Account Detected.")
        time.sleep(0.5)
        print("* Would you like one ?")
        decision = input("* Y/y/Yes/yes or N/n/No/no: ")
        if (
            decision == "N"
            or decision == "n"
            or decision == "no"
            or decision == "No"
            ):
            print("* No problem, Goodbye, you'll be back ;)")
            time.sleep(3)
            clear()
            intialise()
        elif (
            decision == "Y"
            or decision == "y"
            or decision == "yes"
            or decision == "Yes"
            ):
            clear()
            print(
                "* Good choice and welcome to WAIO Bank,", str(uname).title() + "!"
            )
            decide = 1
        else:
            print("* Invalid input. Select one of the options correctly please.")
            time.sleep(3)
            clear()
    user_input = 0
    while True:
        try:                  
            pin = int(input("* Setup a Pin to Register: "))
        except ValueError:
            print("* Please use Numerical characters only.")
            continue
        else:
            break
    pin_check = 0
    while pin_check != pin:
        try:
            pin_check = int(input("* Please Confirm Pin: "))
        except ValueError:
            print("* Please use Numerical characters only.")
    time.sleep(2)     
    clear()
    print("* Pin saved successfully.")
    email_form = 0
    while email_form == 0:
        global gather_email
        gather_email = input("* Please Enter your Email Address: ")
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,4}$'
        if(re.search(regex,gather_email)):
            email_form = 1
        else:
            print("* Email address does not exist, enter your email address.")    
    email_check = 0
    while email_check != gather_email:
        email_check = input("* Please Confirm Email: ")
    print("* Email address saved successfully.")
    clear()
    mobile_form = 0
    while mobile_form == 0:
        global gather_mobile
        gather_mobile = input("* Please Enter your Mobile Number: ")
        s = gather_mobile
        if (isValid(s)):  
            print ("* Valid Number")      
        else : 
            print ("* Invalid Number")        
             
    mobile_check = 0
    while mobile_check != gather_mobile:
        mobile_check = input("* Please Confirm Mobile: ")
    print("* Mobile number saved successfully.")
    check_duplicate_account()
    gift = randint(1, 100)
    print(
        "* You have been gifted:",
        "${:,.2f}".format(float(gift)),
        "to start your Account Balance.",
    )
    now = datetime.now()
    r.mset(
        {
            str(uname) + "_pin": pin,
            str(uname) + "_balance": gift,
            str(uname) + "_transactions": 0,
            str(uname) + "_savings": 0,
            str(uname) + "_interest_rate": randint(1, 5),
            str(uname) + "_sign_up_date": str(date.today()),
            str(uname) + "_last_login_date": str(date.today()),
            str(uname) + "_sign_up_time": now.strftime("%H:%M:%S"),
            str(uname) + "_last_login_time": now.strftime("%H:%M:%S"),
            str(uname) + "_lastLogin": time.time(),
            str(uname) + "_lastBatchRun": time.time(),
            str(uname) + "_logins": 1,
            str(uname) + "_email": gather_email,
            str(uname) + "_mobile": gather_mobile,
            str(uname) + "_status": "member",
        }
    )
    time.sleep(1)
    input("* Press Enter to continue...")
    menu()    
    

def onboarding():
    print("------------------------------------------")
    print("********** Welcome to WAIO Bank **********")
    print("------------------------------------------")
    code = randint(1, 10)
    code1 = randint(1, 10)
    code_ans = code + code1
    code_error = 0
    code_check = 0
    while code_ans != code_check:
        print()
        print("* Security Code is:", code, "+", code1, "= ?") 
        try:
            code_check = int(input("* Calculate Security Code Correctly to continue: "))
        except ValueError:
            print("Please use Numerical characters only.")
        code_error += 1
        if code_check == code_ans:
            print("* Security Code Correctly Calculated.")
        else:
            if code_error == 3:
                print("* Incorrect Security Code, Goodbye!")
                print(
                    "* Your session lasted:",
                    round(time.time() - login_start),
                    "Seconds.",
                )
                time.sleep(3)
                clear()
                intialise()
            print(
                "* Incorrect Security Code, You have", 3 - code_error, "attempts left."
            )
        time.sleep(2)
        clear()          
    pin = 0
    pin_error = 0
    if r.exists(str(uname) + "_pin"):
        existing_user()
    else:
        new_user()


def main():
    host_message = (
        "cmVkaXMtMTQ3MjYuYzg0LnVzLWVhc3QtMS0yLmVjMi5jbG91ZC5yZWRpc2xhYnMuY29t"
    )
    host_bytes = host_message.encode("ascii")
    hostm_bytes = base64.b64decode(host_bytes)
    global ghost
    ghost = hostm_bytes.decode("ascii")
    port_message = "MTQ3MjY="
    port_bytes = port_message.encode("ascii")
    portm_bytes = base64.b64decode(port_bytes)
    global gport
    gport = portm_bytes.decode("ascii")
    db_message = "WjByRnZ0OEwzdVBUMTV3eFBGQndDY1NCaW9KT25BcVU="
    db_bytes = db_message.encode("ascii")
    dbm_bytes = base64.b64decode(db_bytes)
    global gdb
    gdb = dbm_bytes.decode("ascii")
    intialise()


def intialise():
    try:
        global r
        r = redis.StrictRedis(
            host=ghost, port=gport, password=gdb, db=0, decode_responses=True
        )
        global uname
        print("{:*^20}".format("WAIO Bank V1.0"))
        while True:
            uname = input("* Enter Username to Log In: ").strip()
            if uname and uname.isalpha():
                uname = uname.lower()
                global login_start
                login_start = time.time()
                clear()
                onboarding()
            elif uname and uname.isdigit():
                print("* Please use Alphabet characters only.")
            else:
                print("* Only Alphabet usernames are allowed.")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
else:
    print("Module running")
    # Run as module
