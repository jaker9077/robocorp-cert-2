# Robocorp Imports
from robocorp import browser
from RPA.HTTP import HTTP
from RPA.Tables import Tables
from RPA.Archive import Archive

# Other Imports
import os
import shutil

# Use dependencies to set up tmp directories
def p_100(tmp_pdf_dir, tmp_screenshot_dir, pdf_dir):
    os.makedirs(tmp_pdf_dir, exist_ok=True)
    os.makedirs(tmp_screenshot_dir, exist_ok=True)
    os.makedirs(pdf_dir, exist_ok=True)


# Open the robot order website
def p_101():
    page = browser.page()
    page.goto("https://robotsparebinindustries.com/#/robot-order")
    

# Download the orders
def p_102():
    http = HTTP()
    http.download("https://robotsparebinindustries.com/orders.csv", target_file="output/orders.csv" , overwrite=True)
    

# Read the orders from the CSV file into a table variable
def p_103():
    # Instantiate the Tables library
    tables = Tables()
    robot_orders = tables.read_table_from_csv("output/orders.csv", header=True, delimiters=",")
    return robot_orders


# Archive the receipts
def p_300(pdf_dir):
    lib = Archive()
    lib.archive_folder_with_zip(pdf_dir, "output/robot_receipts.zip")


# Delete the tmp directories and the pdfs
def p_400(tmp_dir, pdf_dir):
    shutil.rmtree(tmp_dir, ignore_errors=True)
    shutil.rmtree(pdf_dir, ignore_errors=True)