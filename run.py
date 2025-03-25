from collections import defaultdict
import os

import jinja2
import csv

from xhtml2pdf import pisa
from datetime import date


def render_html(data):
    """
    Render html page using jinja based on layout.html
    """
    template_loader = jinja2.FileSystemLoader(searchpath="./")
    template_env = jinja2.Environment(loader=template_loader)
    template_file = "layout.html"
    template = template_env.get_template(template_file)
    output_text = template.render(data=data, now=date.today())
    # HTML(string=outputText).write_pdf("weasyout.pdf")

    html_path = "./res/program.html"
    html_file = open(html_path, "w")
    html_file.write(output_text)
    html_file.close()
    print("Now converting program ... ")
    pdf_path = "./res/program.pdf"
    html2pdf(html_path, pdf_path)


def html2pdf(html_path, pdf_path):
    """
    Convert html to pdf using pdfkit which is a wrapper of wkhtmltopdf
    """
    # options = {
    #     "page-size": "Letter",
    #     "margin-top": "0.35in",
    #     "margin-right": "0.75in",
    #     "margin-bottom": "0.75in",
    #     "margin-left": "0.75in",
    #     "encoding": "UTF-8",
    #     "no-outline": None,
    #     "enable-local-file-access": None,
    # }
    pisa.showLogging()
    with open(pdf_path, "w+b") as f:
        pisa_status = pisa.CreatePDF(open(html_path, "r"), dest=f)
        # Check for errors
        if pisa_status.err:
            print("An error occurred!")


def get_data_dict():
    sponsors = defaultdict(list)
    # https://stackoverflow.com/a/49150749/1449799
    with open("sponsors/sponsors.csv", "r", newline="", encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            record = row
            record["width"] = 150-25*int(record["lvldx"])
            sponsors[row["Level"]].append(record)
    
    submissions = defaultdict(list)
    with open("data.csv", "r", newline="", encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # publish_info = {
            #     "ID": row["ID"],
            #     "Title": row["Title"],
            #     "Authors": {
            #         "label": "Author{}:".format("s" if "," in row["Authors"] or ";" in row["Authors"] else ""),
            #         "authors": row["Authors"],
            #     },
            #     "Abstract": row["Abstract"],
            #     "CategoryLabel": row["CategoryLabel"],
            # }
            submissions[row["CategoryLabel"]].append(row)
    return {"sponsors":sponsors, "submissions":submissions}


if __name__ == "__main__":
    data = get_data_dict()
    render_html(data)
    print("All done!")
