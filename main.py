from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

def track_finance(period_name, income_table, expense_table, date_filter_format):
    print(f"{period_name.capitalize()} tracker")
    con = sqlite3.connect('finance.db')
    cur = con.cursor()

    cur.execute(f'''
        CREATE TABLE IF NOT EXISTS {income_table}(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        income_source TEXT,
        income_value REAL,
        income_date TEXT
        )''')
    
    cur.execute(f'''
        CREATE TABLE IF NOT EXISTS {expense_table}(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        income_id INTEGER,
        expense_name TEXT,
        expense_value REAL,
        expense_date TEXT,
        FOREIGN KEY (income_id) REFERENCES {income_table} (id)
        )''')
    
    while True:
        try:
            income_all = 0

            # *** Income Loop ***
            while True:
                try:
                    print("*** Income ***")    
                    income_source = input("Please provide income source or leave it blank: ")    
                    income_value = int(input(f"Please enter {period_name} balance: $"))
                    income_date = input("Please enter date (YYYY-MM-DD): ")
                    income_date = datetime.strptime(income_date, "%Y-%m-%d").strftime("%Y-%m-%d")
                    
                    income_all += income_value

                    cur.execute(f"INSERT INTO {income_table} (income_source, income_value, income_date) VALUES (?, ?, ?)",
                                (income_source, income_value, income_date))          
                    con.commit()
                    income_id = cur.lastrowid

                    choice = input("click enter to add income or type 'expense' for expenses: ").lower()
                    if choice == "expense":
                        break
                except ValueError:
                    print("⚠️ Invalid value!")
                
            # *** Expense Loop ***
            expense_all = 0
            while True:
                try:
                    expense_name = input("Enter name of expense: ")
                    expense_value = int(input("Enter cost: -$"))
                    expense_date = input("Please enter date of expense (YYYY-MM-DD): ")
                    expense_all += expense_value

                    cur.execute(f"INSERT INTO {expense_table} (income_id, expense_name, expense_value, expense_date) VALUES (?, ?, ?, ?)",
                                (income_id, expense_name, expense_value, expense_date))
                    con.commit()

                    choice = input("Click 'Enter' to continue or 'done' to return: ").lower()                
                    if choice == "done":
                        break
                except ValueError:
                    print("⚠️ Invalid value!")

            income_left = income_all - expense_all
            print(f"\nYou left with ${income_left}")

            # *** Menu for charts or back ***
            m_choice = input("\nClick 'Enter' to do again or 'back' to return, 'chart' for chart: ").lower()

            if m_choice == "chart":
                try:
                    if date_filter_format == "%Y-%m-%d":
                        selected = input("Please specify date (YYYY-MM-DD):")
                    elif date_filter_format == "%Y-%m":
                        selected = input("Please specify month (YYYY-MM): ")
                    else:
                        selected = input("Please specify year (YYYY): ")

                    df_income = pd.read_sql(f"SELECT * FROM {income_table} WHERE strftime('{date_filter_format}', income_date) = ?",
                                            con, params = [selected]
                                            )
                    df_expense = pd.read_sql(f"SELECT * FROM {expense_table} WHERE strftime('{date_filter_format}', expense_date) = ?",
                                            con,params = [selected]
                                            )
                    
                    if df_income.empty and df_expense.empty:
                        print("No data for Plot.")
                        continue

                    # Bar chart

                    totals = [df_income["income_value"].sum(), df_expense["expense_value"].sum()]
                    labels = ["Income", "Expense"]
                    plt.bar(labels, totals)
                    plt.title("Income vs Expense")
                    plt.show()

                    # Pie chart
                    if not df_expense.empty:
                        expense_by_category = df_expense.groupby("expense_name")["expense_value"].sum()
                        plt.pie(expense_by_category, labels=expense_by_category.index, autopct="%1.1f%%")
                        plt.title(f"Expense Breakdown for {selected}")
                        plt.show()

                    if not df_expense.empty:
                        starting_income = df_income["income_value"].sum()
                        df_expense["running_balance"] = starting_income - df_expense["expense_value"].cumsum()
                        plt.plot(df_expense["expense_name"], df_expense["running_balance"], marker="o")
                        plt.title(f"Balance trend for {selected}")
                        plt.xlabel("Expense #")
                        plt.ylabel("Remaining Balance ($)")
                        plt.show()

                    return_back = input("Type 'back' to return: ").lower()
                    if return_back == "back":
                        return
                    else:
                        print("Please enter valid option!")

                except ValueError:
                    print("⚠️ Invalid value!")

            elif m_choice == "back":
                con.close()
                break 
               
        except Exception as e:
            print(f"⚠️ Something went wrong: {e}")

def main():
    print("-" * 30)
    print("😊Welcome to Financee!")
    print("-" * 30)    

    while True:
        print("\n1. Daily Finance Tracking")
        print("2. Monthly Finance Tracking")
        print("3. Yearly Finance Tracking")
        print("4. Exit")

        try:
            choice = input("Please choose the option: ")

            if choice == "1":
                track_finance("daily", "income_track", "expense_track", "%Y-%m-%d")    
            elif choice == "2":
                track_finance("monthly", "income_monthly", "expense_monthly", "%Y-%m")
            elif choice == "3":
                track_finance("yearly", "income_yearly", "expense_yearly", "%Y")
            elif choice == "4":
                print("😊 You are Welcome!")
                break
        except Exception as e:
            print("⚠️ Something went wrong!")

if __name__ == "__main__":
    main()