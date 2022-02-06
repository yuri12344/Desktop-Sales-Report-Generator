import os
from dotenv import load_dotenv
import pymysql
import threading
load_dotenv()


def show_messages_database(self_, *args):
    while True:
        mysql = self_.connections['mysql']['msg']
        self_.status_db.setText(f"{mysql} \n Connections: Check your internet or VPN, or credentials in .env")
                

def connect_db(self_):
    threading.Thread(target=show_messages_database, args=(self_,)).start()
    threading.Thread(target=mysql_conn, args=(self_,)).start()
    
    
def mysql_conn(self_):
    urlMysql = os.getenv('DB_MYSQL_URL')
    userMysql = os.getenv('DB_MYSQL_USER')
    passMysql = os.getenv('DB_MYSQL_PASS')
    envMysql = os.getenv('DB_MYSQL_NAME')
    try:   
        self_.connections['mysql']['conn'] = pymysql.connect(host=urlMysql, user=userMysql, passwd=passMysql, database=envMysql)
        self_.connections['mysql']['msg'] = "Mysql -> OK"
        return
    except Exception as e:
        self_.connections['mysql']['msg'] = "Mysql -> Not Possible to Connect MySql"
        return
    
