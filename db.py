import sqlite3

databaseName = "quiz.db"

courses = {
    "DS_3850": "DS 3850",
    "DS_3860": "DS 3860",
    "FIN_3210": "FIN 3210",
    "ART_1250": "ART 1250",
    "DS_3620": "DS 3620"
}

def connect_db():
    return sqlite3.connect(databaseName)

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()
    for table in courses:
        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT,
            option1 TEXT,
            option2 TEXT,
            option3 TEXT,
            option4 TEXT,
            correct TEXT
        )
        """)
    conn.commit()
    conn.close()

def insert_question(table, question, options, correct):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(f"""
        INSERT INTO {table} (question, option1, option2, option3, option4, correct)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (question, *options, correct))
    conn.commit()
    conn.close()

def get_all_questions(table):
    """Return all questions for a specific course table."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table}")
    rows = cursor.fetchall()
    conn.close()
    return rows

def preload_sample_questions():
    """Only run this once to populate your DB with sample questions."""
    all_questions = {
        "DS_3850": [
            ("What does the `len()` function do in Python?", ["Adds two numbers", "Returns the length of an object", "Creates a new list", "Converts a string to an integer"], "Returns the length of an object"),
            ("Which symbol is used for comments in Python?", ["//", "/* */", "#", "%%"], "#"),
            ("What is the output of `print(2 ** 3)`?", ["6", "9", "8", "5"], "8"),
            ("Which of these is a valid variable name?", ["2name", "my-name", "_score", "class"], "_score"),
            ("What data type is the result of `input()`?", ["int", "float", "string", "bool"], "string"),
            ("What is the purpose of a loop?", ["To exit a program", "To repeat code", "To define a function", "To print output"], "To repeat code"),
            ("How do you define a function in Python?", ["define my_function():", "function my_function():", "def my_function():", "func my_function():"], "def my_function():"),
            ("What does `list.append(5)` do?", ["Removes 5 from the list", "Inserts 5 at the beginning", "Adds 5 to the end of the list", "Replaces all items with 5"], "Adds 5 to the end of the list"),
            ("What does `if` do in Python?", ["Declares a class", "Creates a list", "Starts a conditional block", "Imports a module"], "Starts a conditional block"),
            ("What does `range(5)` return?", ["0 to 4", "1 to 5", "1 to 4", "0 to 5"], "0 to 4")
        ],
        "DS_3860": [
            ("What does SQL stand for?", ["Structured Query Language", "Standard Question Language", "Simple Quick Language", "Stored Query List"], "Structured Query Language"),
            ("Which SQL command is used to retrieve data?", ["INSERT", "GET", "SELECT", "RETRIEVE"], "SELECT"),
            ("Which keyword adds a new row to a table?", ["ADD", "CREATE", "UPDATE", "INSERT INTO"], "INSERT INTO"),
            ("What does `WHERE` do in SQL?", ["Sorts results", "Filters rows", "Joins tables", "Adds columns"], "Filters rows"),
            ("Which clause is used to sort results?", ["ORDER BY", "GROUP BY", "SORT", "ARRANGE"], "ORDER BY"),
            ("What does `NULL` mean in SQL?", ["Zero", "Empty string", "Unknown or missing value", "False"], "Unknown or missing value"),
            ("What is a primary key?", ["A column that contains foreign data", "A unique identifier for rows", "A password", "A comment line"], "A unique identifier for rows"),
            ("Which of the following joins returns only matching rows from both tables?", ["LEFT JOIN", "FULL JOIN", "INNER JOIN", "OUTER JOIN"], "INNER JOIN"),
            ("What does `UPDATE` do in SQL?", ["Changes existing data", "Deletes a row", "Adds a new row", "Drops a table"], "Changes existing data"),
            ("Which SQL statement removes a table?", ["DELETE", "REMOVE", "DROP TABLE", "CLEAR"], "DROP TABLE")
        ],
        "FIN_3210": [
            ("What does ROI stand for?", ["Rate of Income", "Return on Investment", "Risk of Investment", "Rate of Inflation"], "Return on Investment"),
            ("What is a bond?", ["A type of stock", "A loan made to a government or company", "A savings account", "A tax deduction"], "A loan made to a government or company"),
            ("What is the time value of money?", ["A principle that money grows on trees", "Money is worth more in the future", "Money now is worth more than the same amount later", "Money has no value over time"], "Money now is worth more than the same amount later"),
            ("What does diversification help reduce?", ["Profits", "Taxes", "Risk", "Income"], "Risk"),
            ("What is the formula for net income?", ["Revenue – Expenses", "Assets – Liabilities", "Expenses – Revenue", "Revenue + Expenses"], "Revenue – Expenses"),
            ("What is the market for short-term debt called?", ["Capital market", "Stock market", "Money market", "Futures market"], "Money market"),
            ("What is a stock dividend?", ["A tax refund", "A share of profits paid to shareholders", "A type of bond", "A price increase"], "A share of profits paid to shareholders"),
            ("Which of these is a financial statement?", ["Income Report", "Balance Sheet", "Tax Return", "Expense Forecast"], "Balance Sheet"),
            ("What does liquidity mean?", ["The ability to make a profit", "How quickly assets turn to cash", "The cost of an asset", "A market's stability"], "How quickly assets turn to cash"),
            ("What is compound interest?", ["Interest on the original amount", "Interest earned on interest", "A tax benefit", "A market trend"], "Interest earned on interest")
        ],
        "ART_1250": [
            ("What does the Crop Tool do?", ["Resize the canvas", "Cut out a part of an image", "Add a border", "Merge layers"], "Cut out a part of an image"),
            ("What is a layer in Photoshop?", ["A brush tool", "A type of filter", "A separate image level", "A color effect"], "A separate image level"),
            ("What does the Magic Wand Tool select?", ["All text", "Areas of similar color", "Entire image", "Gradient fills"], "Areas of similar color"),
            ("What format keeps layers intact?", [".jpg", ".png", ".psd", ".gif"], ".psd"),
            ("What is the shortcut for undo?", ["Ctrl + S", "Ctrl + U", "Ctrl + Z", "Ctrl + X"], "Ctrl + Z"),
            ("Which panel shows the list of layers?", ["Tools", "Layers", "History", "Options"], "Layers"),
            ("What does Opacity control?", ["Color", "Brightness", "Transparency", "Size"], "Transparency"),
            ("Which tool removes blemishes?", ["Lasso Tool", "Patch Tool", "Spot Healing Brush", "Pen Tool"], "Spot Healing Brush"),
            ("What does the Clone Stamp Tool do?", ["Duplicates parts of an image", "Adds text", "Crops a photo", "Adds filters"], "Duplicates parts of an image"),
            ("Which file format is best for web?", [".bmp", ".png", ".psd", ".jpg"], ".jpg")
        ],
        "DS_3620": [
            ("What symbol starts a formula in Excel?", ["!", "#", "=", "$"], "="),
            ("What does `SUM(A1:A5)` do?", ["Adds the values from A1 to A5", "Finds the max value", "Sorts data", "Subtracts A5 from A1"], "Adds the values from A1 to A5"),
            ("What is a cell reference?", ["A formula name", "A column header", "The location of a cell (like B2)", "A type of filter"], "The location of a cell (like B2)"),
            ("What does the fill handle do?", ["Zooms the sheet", "Fills colors", "Copies a pattern or formula", "Deletes cells"], "Copies a pattern or formula"),
            ("What does `IF` do in Excel?", ["Repeats a row", "Makes a chart", "Adds a condition", "Inserts a table"], "Adds a condition"),
            ("Which chart is best for parts of a whole?", ["Line chart", "Pie chart", "Scatter plot", "Histogram"], "Pie chart"),
            ("What does Ctrl + C do?", ["Cut", "Copy", "Clear", "Paste"], "Copy"),
            ("What does `VLOOKUP` do?", ["Looks for vertical cells", "Searches for values in a column", "Validates a list", "Links spreadsheets"], "Searches for values in a column"),
            ("What does conditional formatting do?", ["Sorts data", "Adds comments", "Formats cells based on rules", "Deletes duplicates"], "Formats cells based on rules"),
            ("What is a pivot table used for?", ["To create charts", "To summarize data", "To color rows", "To merge cells"], "To summarize data")
        ]
    }

    for table, questions in all_questions.items():
        for q in questions:
            insert_question(table, q[0], q[1], q[2])

# Always create tables when module is used
create_tables()

# Run this ONCE manually to preload sample data:
preload_sample_questions()