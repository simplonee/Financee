from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
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

            m_choice = input("\nClick 'Enter' to do again or 'back' to return, 'chart' for chart: ").lower()

            if m_choice == "chart":
                try:
                    df_income = pd.read_sql("SELECT * FROM income_track WHERE entry_date = ?",
                                            con,
                                            params = [today]
                                            )
                    df_expense = pd.read_sql("SELECT * FROM expense_track WHERE entry_date = ?",
                                            con,
                                            params = [today]
                                            )
                    
                    if df_income.empty and df_expense.empty:
                        print("No data for Plot.")
                        continue
                    totals = [df_income["income_value"].sum(), df_expense["expense_value"].sum()]
                    labels = ["Income", "Expense"]

                    plt.bar(labels, totals)
                    plt.title("Income vs Expense")
                    plt.show()

                    expense_by_category = df_expense.groupby("expense_name")["expense_value"].sum()
                    plt.pie(expense_by_category, labels=expense_by_category.index, autopct="%1.1f%%")
                    plt.title(f"Expense Breakdown for {today}")
                    plt.show()

                    starting_income = df_income["income_value"].sum()
                    df_expense["running_balance"] = starting_income - df_expense["expense_value"].cumsum()

                    plt.plot(df_expense["expense_name"], df_expense["running_balance"], marker="o")
                    plt.title(f"Balance trand for {today}")
                    plt.xlabel("Expense #")
                    plt.ylabel("Remaining Balance ($)")
                    plt.show()
                except ValueError:
                    print("⚠️ Invalid value!")

            elif m_choice == "back":
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

            m_choice = input("\nClick 'Enter' to do again or type 'back' to return, 'chart' for charts: ").lower()

            if m_choice == "chart":
                try:
                    selected_month = input("Plese specify month (YYYY-MM): ")
                    df_income = pd.read_sql("SELECT * FROM income_monthly WHERE  strftime('%Y-%m', income_date) = ?",
                                            con,
                                            params = [selected_month]
                                            )
                    df_expense = pd.read_sql("SELECT * FROM expense_monthly WHERE  strftime('%Y-%m', expense_date) = ?",
                                            con,
                                            params = [selected_month]
                                            )
                    
                    if df_income.empty and df_expense.empty:
                        print("No data for Plot.")
                        continue
                    totals = [df_income["income_value"].sum(), df_expense["expense_value"].sum()]
                    labels = ["Income", "Expense"]

                    plt.bar(labels, totals)
                    plt.title("Income vs Expense")
                    plt.show()

                    expense_by_category = df_expense.groupby("expense_name")["expense_value"].sum()
                    plt.pie(expense_by_category, labels=expense_by_category.index, autopct="%1.1f%%")
                    plt.title(f"Expense Breakdown for {selected_month}")
                    plt.show()

                    starting_income = df_income["income_value"].sum()
                    df_expense["running_balance"] = starting_income - df_expense["expense_value"].cumsum()

                    plt.plot(df_expense.index, df_expense["running_balance"], marker="o")
                    plt.title(f"Balance trend for {selected_month}")
                    plt.xlabel("Expense #")
                    plt.ylabel("Remaining Balance ($)")
                    plt.show()
                except ValueError:
                    print("⚠️ Invalid value!")

            elif m_choice == "back":
                con.close()
                break    

        except Exception as e:
            print(f"⚠️ Something went wrong: {e}")
            con.close()


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
                    income_source = input("\nPlease provide income source or leave it blank with space: ")
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

            m_choice = input("\nClick 'Enter' to do again or type 'back' to return, 'chart' for charts: ").lower()

            if m_choice == "chart":
                try:
                    selected_year = input("Plese specify Year (YYYY): ")
                    df_income = pd.read_sql("SELECT * FROM income_yearly WHERE  strftime('%Y', income_date) = ?",
                                            con,
                                            params = [selected_year]
                                            )
                    df_expense = pd.read_sql("SELECT * FROM expense_yearly WHERE  strftime('%Y', expense_date) = ?",
                                            con,
                                            params = [selected_year]
                                            )
                    
                    if df_income.empty and df_expense.empty:
                        print("No data for Plot.")
                        continue
                    totals = [df_income["income_value"].sum(), df_expense["expense_value"].sum()]
                    labels = ["Income", "Expense"]

                    plt.bar(labels, totals)
                    plt.title("Income vs Expense")
                    plt.show()

                    expense_by_category = df_expense.groupby("expense_name")["expense_value"].sum()
                    plt.pie(expense_by_category, labels=expense_by_category.index, autopct="%1.1f%%")
                    plt.title(f"Expense Breakdown for {selected_year}")
                    plt.show()

                    starting_income = df_income["income_value"].sum()
                    df_expense["running_balance"] = starting_income - df_expense["expense_value"].cumsum()

                    plt.plot(df_expense.index, df_expense["running_balance"], marker="o")
                    plt.title(f"Balance trend for {selected_year}")
                    plt.xlabel("Expense #")
                    plt.ylabel("Remaining Balance ($)")
                    plt.show()
                except ValueError:
                    print("⚠️ Invalid value!")

            elif m_choice == "back":
                con.close()
                break        

        except Exception as e:
            print(f"⚠️ Something went wrong: {e}")
            con.close()

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