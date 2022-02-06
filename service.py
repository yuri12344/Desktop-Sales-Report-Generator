import datetime
from services.sales_reports.all_sales_report import generate_all_sales_report
import os
import webbrowser


def open_report_dir():
    rep_dir = f'{os.getcwd()}/services/sales_reports/reports/'
    try:
        os.stat(rep_dir)
    except:
        os.makedirs(f'{rep_dir}tmp')
    webbrowser.open(rep_dir)


def all_sales_report(self_):
    # Take data information
    customer_name = self_.all_sales_report_client_name.text().upper()
    customer_name = customer_name.replace('/', '-') if len(customer_name) > 0 else "WITHOUT_NAME"

    date_from = f'{self_.all_sales_report_date_from.text()} {self_.sales_report_hours_from.text()}:00'
    date_to = f'{self_.all_sales_report_date_to.text()} {self_.sales_report_hours_to.text()}:00'
    customer_id = self_.all_sales_report_client_id.text()

    date_from = datetime.datetime.strptime(date_from, '%d/%m/%Y %H:%M:%S')
    date_to = datetime.datetime.strptime(date_to, '%d/%m/%Y %H:%M:%S')

    dto = {
        'customer_name': customer_name,
        'customer_id': int(customer_id),
        'date_from': date_from,
        'date_to': date_to,
    }   
    generate_all_sales_report(self_, dto)