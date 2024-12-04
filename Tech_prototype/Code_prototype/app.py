import os
from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Path to the directory where your CSV files are stored
CSV_DIRECTORY = 'data/'


# Function to get the company codes from the CSV filenames
def get_company_codes_from_csv():
    csv_files = [f for f in os.listdir(CSV_DIRECTORY) if f.endswith(".csv")]
    company_codes = [os.path.splitext(f)[0] for f in csv_files]  # Extract company codes from file names
    return company_codes


# Initialize company list before starting the app
def initialize_app():
    global company_list
    company_list = get_company_codes_from_csv()


initialize_app()


# Home route to render the dropdown
@app.route("/")
def index():
    return render_template("index.html", companies=company_list)


# Route to handle form submission and display CSV data
@app.route("/search", methods=["POST"])
def search():
    company_code = request.form["company_code"]
    csv_file_path = os.path.join(CSV_DIRECTORY, f"{company_code}.csv")

    # Check if the CSV file exists
    if os.path.exists(csv_file_path):
        data = pd.read_csv(csv_file_path)
        return render_template("result.html", data=data.to_html(), company_code=company_code)
    else:
        return f"Data for {company_code} not found."


if __name__ == "__main__":
    # Run the app and initialize the company list
    initialize_app()
    app.run(debug=True)