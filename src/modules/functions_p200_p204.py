# Robocorp Imports
from robocorp import browser
from RPA.PDF import PDF

# Other Imports
import time


# Fill out the order form
def p_200(tmp_pdf_dir, tmp_screenshot_dir, orders):

    # Loop through the orders
    for row in orders:

        # Close the modal
        p_201()

        # Fill out the form
        page = browser.page()
        page.select_option("#head", str(row["Head"]))
        page.check(f"#id-body-{row['Body']}")
        page.fill("input[placeholder='Enter the part number for the legs']", str(row["Legs"]))
        page.fill("input[placeholder='Shipping address']", str(row["Address"]))
        
        # True loop to handle error div
        while True:
            page.click("#order")
            
            # Wait for 1 second to allow the page to update
            time.sleep(1)
            
            # If the error happens, click order again
            if page.is_visible(".alert alert-danger"):
                print("Error div visible, trying again...")
                continue
            
            # If no error happens, order the next robot
            if not page.is_visible("#order"):
                break

        # Get order number
        order_number = page.locator(".badge").inner_text()

        # Store receipt as PDF
        tmp_pdf_receipt_path = p_202(order_number, tmp_pdf_dir)

        # Get screenshot of robot
        tmp_robot_picture_path = p_203(order_number, tmp_screenshot_dir)

        # Embed screenshot to pdf receipt
        p_204(order_number, tmp_pdf_receipt_path, tmp_robot_picture_path)

        # Order next robot
        page.locator("#order-another").click()


# Close the annoying modal pop up on the page
def p_201():
    page = browser.page()
    page.click(".btn-dark")


# Store receipt as PDF
def p_202(order_number, tmp_pdf_dir):
    # Instantiate the PDF library
    pdf = PDF()
    page = browser.page()
    html_receipt = page.locator("#receipt").inner_html()
    tmp_pdf_receipt_path = f"{tmp_pdf_dir}{order_number}.pdf"
    pdf.html_to_pdf(html_receipt, tmp_pdf_receipt_path)
    return tmp_pdf_receipt_path


# Screenshot robot
def p_203(order_number, tmp_screenshot_dir):
    page = browser.page()
    tmp_robot_picture_path = f"{tmp_screenshot_dir}{order_number}.png"
    page.locator("#robot-preview-image").screenshot(path=tmp_robot_picture_path)
    return tmp_robot_picture_path


# Embed screenshot to receipt pdf
def p_204(order_number, tmp_pdf_receipt_path, tmp_robot_pic_path):
    pdf = PDF()
    pdf_receipt_path = f"output/pdfs/{order_number}.pdf"
    pdf.add_watermark_image_to_pdf(image_path=tmp_robot_pic_path, source_path=tmp_pdf_receipt_path, output_path=pdf_receipt_path)