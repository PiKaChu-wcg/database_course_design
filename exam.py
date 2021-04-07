import sys
import numpy as np
import pandas as pd
import pymysql
from sqlalchemy import create_engine
import copy
import random
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from qdarkstyle import load_stylesheet_pyqt5
from random import randint

class QtTable(QAbstractTableModel):
    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data
    def rowCount(self, parent=None):
        return self._data.shape[0]
    def columnCount(self, parent=None):
        return self._data.shape[1]
    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None
    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]

class mywin(QMainWindow):
    def __init__(self,shape):
        super().__init__()
        self.connect()
        self.initUI(shape)
    def connect(self):
        self.db=pymysql.connect(host='182.254.226.32',user='root',passwd=r'123456',port=3306,db='exam',charset='utf8')
        self.cursor=self.db.cursor()
        self.engine = create_engine("mysql+pymysql://{}:{}@{}:{}/{}".format('root', '123456', '182.254.226.32', '3306', 'exam'))
    def initUI(self,shape):
        self.view=QTableView(self)
        self.view.setGeometry(shape[0]*0.2,0,shape[0]*0.8,shape[1])
        self.showtable('question')

        selector=QComboBox(self)
        selector.setGeometry(20,80,100,30)
        selector.addItems(['question','exam','content','subject','chapter','teacher','student','test'])        
        selector.currentIndexChanged[str].connect(self.showtable)

        self.setGeometry(300,300,*shape)
        bt1=QPushButton(self)
        bt1.setText('插入题目')
        bt1.clicked.connect(self.import_question)
        bt1.move(20,20)
        
        bt2=QPushButton(self)
        bt2.setText("生成试卷")
        bt2.clicked.connect(self.exportpaper)
        bt2.move(20,160)
    

    def exportpaper(self):
        fname=QFileDialog.getSaveFileName(self,'生成试卷','/home','.txt(*.txt)')
        if  not fname[0]:

            return
        papername=fname[0].split('/')[-1][:-4]
        df=pd.DataFrame([papername],columns=['e_name'])
        df.to_sql('exam',self.engine,index=False,if_exists="append")
        df_e=pd.read_sql_query('select * from {};'.format("exam"), self.engine)
        df_q= pd.read_sql_query('select * from {};'.format("question"), self.engine)
        num=0
        score=0
        df_c=pd.DataFrame(columns=['q_num'])
        s=set()
        while num<df_q.shape[0] and score<100:
            i=randint(0,df_q.shape[0]-1)
            if not i in s:
                s.add(i)
                num+=1
                score+=df_q.iloc[i]['q_score']
            
        df_c=df_q.iloc[list(s)]
        df_c['e_num']=df_e.shape[0]
        df_c[['e_num','q_num']].to_sql('content',self.engine,if_exists='append',index=False)
        df_c.to_csv(fname[0])


    def import_question(self):
        fname=QFileDialog.getOpenFileName(self,'插入试题', '/home','csv(*.csv)')
        if fname[0]:
            self.import_pd(fname[0])
    def import_pd(self,fname):
        df=pd.read_csv(fname)
        df.to_sql('quesion',self.engine,index=False,if_exists='append')
    def showtable(self,str):
        sql_query = 'select * from {};'.format(str)
        df_read = pd.read_sql_query(sql_query, self.engine)
        #print(df_read)
        self.view.setModel(QtTable(df_read))




def main():
    app=QApplication(sys.argv)
    app.setStyleSheet(load_stylesheet_pyqt5())
    w=mywin((640,720))
    w.show()
    sys.exit(app.exec_())   
    
if __name__=="__main__":
    main()