# Custom Function Imports
from src.modules.functions import p_100, p_101, p_102, p_103, p_300, p_400
from src.modules.functions_p200_p204 import p_200
# Robocorp Imports
from robocorp.tasks import task


### Initialize Dependencies ###

tmp_pdf_dir = "output/tmp/pdfs/"
tmp_screenshot_dir = "output/tmp/screenshots/"
tmp_dir = "output/tmp/"
pdf_dir = "output/pdfs/"

###############################

@task
def main():
    # Create tmp directories
    p_100(tmp_pdf_dir, tmp_screenshot_dir, pdf_dir)

    # Open website
    p_101()

    # Download orders
    p_102()

    # Read orders
    orders = p_103()
    
    # Fill out the form
    p_200(tmp_pdf_dir, tmp_screenshot_dir, orders)
    
    # Archive the receipts
    p_300(pdf_dir)
    
    # Delete the tmp directories and the pdfs
    p_400(tmp_dir, pdf_dir)



   









    

