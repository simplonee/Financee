from datetime import datetime
import sqlite3

def daily():
    print("Daily tracker")
    con = sqlite3.connect('finance.db')
    cur = con.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS income_track(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            income_source TEXT,
            income_value REAL,
            entry_date TEXT
            )
            ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS expense_track(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                income_id INTEGER,
                expense_name TEXT,
                expense_value REAL,
                entry_date TEXT,
                FOREIGN KEY (income_id) REFERENCES income_track (id)
                )
                ''')

    while True:
        try:
            today = datetime.today().strftime("%Y-%m-%d")
            income_all = 0

            while True:
                try:
                    print("*** Income ***")    
                    income_source = input("Please provide income scourse or leave it blank with space: ")    
                    income_value = int(input("Please enter daily balance: $"))
                    income_all += income_value

                    cur.execute("INSERT INTO income_track (income_source, income_value, entry_date) VALUES (?, ?, ?)",
                                (income_source, income_value, today))          
                    con.commit()
                    income_id = cur.lastrowid

                    choise = input("click enter to add income or type 'expense' for expenses: ").lower()
                    if choise == "expense":
                        break

                except ValueError:
                    print("⚠️ Invalid value!")
                

            expense_all = 0

            while True:
                expense_name = input("Enter name of expense: ")
                expense_value = int(input("Enter cost: -$"))
                expense_all += expense_value

                cur.execute("INSERT INTO expense_track (income_id, expense_name, expense_value, entry_date) VALUES (?, ?, ?, ?)",
                            (income_id, expense_name, expense_value, today))
                con.commit()

                choice = input("Click 'Enter' to continue or 'done' to return: ").lower()                
                if choice == "done":
                    break

            income_left = income_all - expense_all
            print(f"\nYou left with ${income_left}")

            m_choice = input("\nClick 'Enter' to do again or 'back' to return: ").lower()
            if m_choice == "back":
                con.close()
                break    
        except ValueError:
            print("⚠️ Invalid value!")

def monthly():
    print("Monthly tracker")
    con = sqlite3.connect('finance.db')
    cur = con.cursor()
    cur.execute('''
                CREATE TABLE IF NOT EXISTS income_monthly(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    income_source TEXT,
                    income_value REAL,
                    income_date TEXT
                )''')

    cur.execute('''
                CREATE TABLE IF NOT EXISTS expense_monthly(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    income_id INTEGER,
                    expense_name TEXT,
                    expense_value REAL,
                    expense_date TEXT,
                    FOREIGN KEY (income_id) REFERENCES income_monthly (id)
                )''')

    while True:
        try:   
            income_all = 0
            while True:
                try:
                    print("*** Income ***")    
                    income_source = input("Please provide income scourse or leave it blank with space: ")
                    income_value = int(input("Please enter monthly balance: $"))
                    income_date = input("Please enter date of income (YYYY-MM-DD): ")
                    income_date = datetime.strptime(income_date, "%Y-%m-%d").strftime("%Y-%m-%d")

                    income_all += income_value

                    cur.execute("INSERT INTO income_monthly (income_source, income_value, income_date) VALUES (?, ?, ?)",
                                (income_source, income_value, income_date))
                    con.commit()
                    income_id = cur.lastrowid

                    choise = input("Click enter to add income or type 'expense' for expenses: ").lower()
                    if choise == "expense":
                        break
                
                except ValueError:
                    print("⚠️ Invalid value!")

            expense_all = 0

            while True:
                try:
                    print("*** Expense ***")    
                    expense_name = input("\nEnter name of expense: ")
                    expense_value = int(input("Enter cost: -$"))
                    expense_date = input("Please enter date of expense (YYYY-MM-DD): ")
                    expense_all += expense_value

                    cur.execute("INSERT INTO expense_monthly (income_id, expense_name, expense_value, expense_date) VALUES (?, ?, ?, ?)",
                                (income_id, expense_name, expense_value, expense_date))
                    con.commit()
                    
                    choice = input("Click 'Enter' to continue or 'done' to return: ").lower()
                    if choice == "done":
                        break
                
                except ValueError:
                    print("⚠️ Invalid value!")

            income_left = income_all - expense_all
            print(f"\nYou left with ${income_left}")

            m_choise = input("\nClick 'Enter' to do again or 'back' to return: ").lower()
            if m_choise == "back":
                con.close()
                break    

        except ValueError:
            print("⚠️ Invalid value!")

def yearly():
    print("Yearly tracker")
    con = sqlite3.connect('finance.db')
    cur = con.cursor()
    cur.execute('''
                CREATE TABLE IF NOT EXISTS income_yearly(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    income_source TEXT,
                    income_value REAL,
                    income_date TEXT
                )''')

    cur.execute('''
                CREATE TABLE IF NOT EXISTS expense_yearly(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    income_id INTEGER,
                    expense_name TEXT,
                    expense_value REAL,
                    expense_date TEXT,
                    FOREIGN KEY (income_id) REFERENCES income_yearly (id)
                )''')

    while True:
        try:
            income_all = 0
            while True:
                try:
                    print("*** Income ***")    
                    income_source = input("\nPlease provide income scourse or leave it blank with space: ")
                    income_value = int(input("Please enter yearly balance: $"))
                    income_date = input("Please enter date of income (YYYY-MM-DD): ")
                    income_date = datetime.strptime(income_date, "%Y-%m-%d").strftime("%Y-%m-%d")

                    income_all += income_value

                    cur.execute("INSERT INTO income_yearly (income_source, income_value, income_date) VALUES (?, ?, ?)",
                                (income_source, income_value, income_date))
                    con.commit()
                    income_id = cur.lastrowid

                    choise = input("click enter to add income or type 'expense' for expenses: ").lower()
                    if choise == "expense":
                        break
                except ValueError:
                    print("⚠️ Invalid value!")

            expense_all = 0

            while True:
                try:
                    print("*** Expense ***")    
                    expense_name = input("Enter name of expense: ")
                    expense_value = int(input("Enter cost: -$"))
                    expense_date = input("Please enter date of expense (YYYY-MM-DD): ")
                    expense_all += expense_value

                    cur.execute("INSERT INTO expense_yearly (income_id, expense_name, expense_value, expense_date) VALUES (?, ?, ?, ?)",
                                (income_id, expense_name, expense_value, expense_date))
                    con.commit()
                    
                    choice = input("Click 'Enter' to continue or 'done' to return: ").lower()
                    if choice == "done":
                        break
                except ValueError:
                    print("⚠️ Invalid value!")

            income_left = income_all - expense_all
            print(f"\nYou left with ${income_left}")

            m_choise = input("\nClick 'Enter' to do again or 'back' to return: ").lower()
            if m_choise == "back":
                con.close()
                break    

        except ValueError:
            print("⚠️ Invalid value!")

def main():
    print("-" * 30)
    print("😊Welcome to Financee!")
    print("-" * 30)    

    while True:
        print("\n1. Daily Fiance Tracking")
        print("2. Monthly Finance Tracking")
        print("3. Yearly Finance Tracking")
        print("4. Exit")

        try:
            choice = input("Please choose the option: ")

            if choice == "1":
                daily()
            
            elif choice == "2":
                monthly()
            
            elif choice == "3":
                yearly()
            
            elif choice == "4":
                print("😊 You are Welcome!")
                break

        except ValueError:
            print("⚠️ Invalid option!")

        except Exception as e:
            print("⚠️ Something went wrong!")

if __name__ == "__main__":
    main()