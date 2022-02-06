#!/usr/bin/env python
# -*- coding: utf-8 -*-
from threading import Thread
import pandas as pd
import datetime
import requests
import re
import os
import datetime
from PyQt5.QtWidgets import QApplication

mydir = os.getcwd()


# Show messages in UI
def show_messages(self_, *args):
    text = args[0]
    try:
        if text['status'] == 'success':
            print(text['message'])
            now = datetime.datetime.now().strftime("%H:%M")
            self_.status.setStyleSheet("color: green; background-color: rgb(192, 190, 191);")
            self_.status.setText(f"{now} - {text['message']}")
            QApplication.processEvents()
            
        if text['status'] == "fail":
            print(text['message'])
            now = datetime.datetime.now().strftime("%H:%M")
            self_.status.setStyleSheet("color: red; background-color: rgb(192, 190, 191);")
            self_.status.setText(f"{now} - {text['message']}")
            QApplication.processEvents()

    except Exception as e:
        print(f"Error in show messages {e}")

        # Read the temporary files
def get_filename_from_cd(cd):
    if not cd:
        return None
    fname = re.findall('filename=(.+)', cd)
    if len(fname) == 0:
        return None
    return fname[0]


def get_filename(customer_name, data):
    date = data.strftime("%d/%m/%Y %H:%M:%S").replace('/', '-').replace(' ', '-')
    filename = f'{mydir}/services/sales_reports/reports/relatorio-percursos-{customer_name}-{date}.xlsx'
    return filename


# Get the list of active vehicles
def get_all_sales_by_rule(mydb, customer_id):
    try:
        sql = """""".format(customer_id)
        return pd.read_sql(sql, con=mydb)
    except Exception as e:
        print("Error:", e)


# Call sales report can be called by a thread
def call_sales_report_thread_one(self_, result, date_from, date_to, headers):
    ...
    return


# Call sales report return a binary from the request and transform it into a dataframe
def call_sales_report_thread_two(self_, result, date_from, date_to, headers):
    ...
    return


def manage_multi_thread(self_, result, date_from, date_to, headers):
    # Create two threads with half of the sales for each one
    size = int(len(result) / 2)
    size_two = int((size - len(result)) * -1)

    df_1 = result[0:size]
    df_2 = result[size_two:]
    df_thread1 = Thread(target=call_sales_report_thread_one, args=(self_, df_1, date_from, date_to, headers))
    df_thread2 = Thread(target=call_sales_report_thread_two, args=(self_, df_2, date_from, date_to, headers))

    df_thread1.start()
    df_thread2.start()

    df_thread1.join()
    df_thread2.join()
    return


def generate_all_sales_report(self_, dto):
    start = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    self_.list_result = []
    msg = f'Starting in {start}'
    print(msg)
    customer_id = dto['customer_id']
    customer_name = dto['customer_name']
    date_from = dto['date_from']
    date_to = dto['date_to']
    mydb = self_.connections['mysql']['conn']

    if mydb == None:
        show_messages(self_, {'status': 'fail', 'message': "Not connected in MySql Database Yet"})
        return

    if date_from > date_to:
        show_messages(self_, {'status': 'fail', 'message': 'Date from need be minor then Date to'} )
        return

    try:
        result = get_all_sales_by_rule(mydb, customer_id)
        print('Found ' + str(len(result.index)) + ' sales... ')

        filename = get_filename(customer_name, date_from)
        show_messages(self_, {'status': 'success', 'message': 'Find sales - Processing...'})

        if len(result) >= 11:
            manage_multi_thread(self_, result, date_from=date_to, date_to=date_to, headers=headers)
        if len(result) < 11:
            call_sales_report_thread_one(self_, result, date_from=date_to, date_to=date_to, headers=headers)
       
        try:
            if len(self_.list_result) > 0:
                sales = pd.concat(self_.list_result, ignore_index=True)
                sales.to_excel(filename, index=False)
                self_.open_dir()
                show_messages(self_, {'status': 'success', 'message': f'Sucess generated report! Total of sales {len(self_.list_result)}'})
            if len(self_.list_result) == 0:
                show_messages(self_, {'status': 'fail', 'message': "No one sale for this client in this period"})
        
        except Exception as e:
            show_messages(self_, {'status': 'fail', 'message': f'Error in file generation: {e}'})
        
        end = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print(f'Finished process in {end}')
    except Exception as e:
        show_messages(self_, {'status': 'fail', 'message': f'Failed in code execution {e}'})
        return 
