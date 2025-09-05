from datetime import datetime
import sqlite3

def daily():

    con = sqlite3.connect('daily.db')
    cur = con.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS income_track(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            income_scourse text,
            income_value real,
            entry_date TEXT
            )
            ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS expense_track(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                income_id INTEGER,
                expense_name text,
                expense_value real,
                entry_date TEXT,
                FOREIGN KEY (income_id) REFERENCES income_track (id)
                )
                ''')
    

    print("Daily tracker")
    while True:
        try:
            today = datetime.today().strftime("%Y-%m-%d")
            
            income_scourse = input("Please provide income scourse or leave it blank with space: ")    
            income_value = int(input("Please enter daily balance: $"))

            cur.execute("INSERT OR IGNORE INTO income_track (income_scourse, income_value, entry_date) VALUES (?, ?, ?)",
                        (income_scourse, income_value, today))          
            con.commit()
            income_id = cur.lastrowid

            expense_all = 0

            while True:
                expense_name = input("Enter name of expense: ")
                expense_value = int(input("Enter cost: -$"))
                expense_all += expense_value

                cur.execute("INSERT OR IGNORE INTO expense_track (income_id, expense_name, expense_value, entry_date) VALUES (?, ?, ?, ?)",
                            (income_id, expense_name, expense_value, today))
                con.commit()

                choice = input("Click 'Enter' to continue or 'done' to return: ").lower()                
                if choice == "done":
                    break

            income_left = income_value - expense_all
            print(f"\nYou left with ${income_left}")

            m_choice = input("\nClick 'Enter' to do again or 'back' to return: ").lower()
            if m_choice == "back":
                break    

        except ValueError:
            print("⚠️ Invalid value!")

def monthly():
    print("Monthly tracker")

    while True:
        try:    
            income = int(input("Please enter monthly balance: $"))
            outcome = 0
            while True:
                expense_name = input("Enter name of expense: ")
                expense_value = int(input("Enter cost: -$"))
                outcome += expense_value
                choice = input("Click 'Enter' to continue or 'done' to return: ").lower()

                if choice == "done":
                    break

            income -= outcome
            print(f"\nYou left with ${income}")
            m_choise = input("\nClick 'Enter' to do again or 'back' to return").lower()

            if m_choise == "back":
                break    

        except ValueError:
            print("⚠️ Invalid value!")

def yearly():
    print("Yearly tracker")

    while True:
        try:    
            income = int(input("Please enter Yearly balance: $"))
            outcome = 0
            while True:
                expense_name = input("Enter name of expense: ")
                expense_value = int(input("Enter cost: -$"))
                outcome += expense_value
                choice = input("Click 'Enter' to continue or 'done' to return: ").lower()

                if choice == "done":
                    break

            income -= outcome
            print(f"\nYou left with ${income}")
            m_choise = input("\nClick 'Enter' to do again or 'back' to return").lower()

            if m_choise == "back":
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