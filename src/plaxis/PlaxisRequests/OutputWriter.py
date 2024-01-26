#########################################################################
#
#      Title:       Result Output Classes
#
#########################################################################
#
#      Description: Output classes to export results to various outup formats
#
#
#########################################################################
#
#########################################################################
#
#       Author      Thomson, Simon simon.thomson@aecom.com
#
##########################################################################
#
#       Version:    Beta 0.0.3
#
##########################################################################
#
#       Date:       January 2023 
#
###########################################################################

import os.path
from plaxis.pypyodbc import pypyodbc
from io import StringIO

def GetWriter(fileOut=None, tableOut=None, columns=None, formats=None, logger = None):
    
    if fileOut == None:
        return strWriter(columns, formats, logger)
    
    if IsDbFile(fileOut):
        return dbWriter (fileOut, tableOut,columns,formats, logger)
    else:
        return csvWriter(fileOut, tableOut,columns,formats, logger)

def IsDbFile (self, db_file=None):   
        retvar = False
        
        if (db_file != None):
            if (db_file[-4:] == '.mdb'):
                retvar = True
            if (db_file[-6:] == '.accdb'):
                retvar = True
        
        return retvar
        
class writer:
    def __init__(self, fileOut=None, tableOut=None, columns=None, formats=None, logger=None):
        self.fileOut = fileOut
        self.tableOut = tableOut
        self.columns = columns
        self.formats = formats
        self.logger = logger
        self.rowsOut = []
    def log (self,msg):
        if (self.logger is not None):
            self.logger.info(msg)


class strWriter(writer):
    def __init__(self, columns=None, formats=None, logger=None):
        super(strWriter, self).__init__(fileOut=None, tableOut=None, columns=columns, formats=formats, logger=logger)
    def writeOutput(self):
            self.log('Outputting to string....')
            self.str_out += '"\n"'.join(self.rowsOut)

class dbWriter(writer):
    def __init__(self, fileOut=None, tableOut=None, columns=None, formats=None,logger=None
                    ):
        super(dbWriter, self).__init__(fileOut, tableOut, columns, formats, logger)
        self.getConnected (self.fileOut)
        self.createTable(self.tableOut, self.columns, self.formats)

    def getConnected(self, db_file):
            
            self.conn_string = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + db_file + ';'
            
            file = ''
            
            if (os.path.isfile(db_file)):
                self.conn = pypyodbc.connect(self.conn_string)
                self.log ('connecting to existing db:' + db_file)
            else:
                if db_file[-6:]=='.accdb':
                    file = db_file[:-6]
                if db_file[-4:]=='.mdb':
                    file = db_file[:-4]
                if not file:
                    file = db_file
                self.conn = pypyodbc.win_create_mdb(file) 
                self.log ('connecting to new db:' + db_file)
                db_file = file + '.mdb'
            
            self.db_file = db_file
        
   

    
    def setFields(self, fields, formats):
        self.columns = fields.split(',')
        self.formats = formats.split(',') 
        self.types = formats.split(',')
        for i in range(len(self.types)):
            if (self.formats[i]=='{:2f}'):
                self.types[i] = 'float'
            if (self.formats[i]=='{:f}'):
                self.types[i] = 'float'    
            if (self.formats[i]=='{}'):
                self.types[i] = 'varchar(255)'
            if (self.formats[i]=='{:0}'):
                self.types[i] = 'int'  
            if (self.formats[i]=='{0}'):
                self.types[i] = 'int'              
                    
    def createTable(self, tname, fields, formats):
        self.tname = tname
        self.setFields(fields, formats)
        self.sql_insert = 'insert into ' + tname + ' ('
        self.sql_drop = 'drop table ' + tname
        self.sql_create = 'create table '+ tname + ' (id autoincrement primary key, '
        self.sql_select = 'select '
        separator = ''
        for i in range (len(self.columns)):
            if (i > 0):
                separator=', '
            self.sql_create += separator + '[' + self.columns[i] + '] ' + self.types[i]
            self.sql_insert += separator + '[' + self.columns[i] + ']'
            self.sql_select += separator + '[' + self.columns[i] + ']'
        self.sql_create += ')'
        self.sql_insert += ')'
        self.sql_select += ' from ' + tname
        print (self.sql_create)
        cursor = self.conn.cursor()
        if (self.tableExists(tname)):
            cursor.execute(self.sql_drop)
        cursor.execute(self.sql_create) 
        self.conn.commit()
    def tableExists(self, tname):
        try:
            cursor = self.conn.cursor()
            sql = 'select top 1 * from '  + tname 
            cursor.execute(sql)
            return True
        except:
            return False
        
    def insertValues(self, data):
        self.sql_data = self.sql_insert + ' values ('  
        separator = ''
        for i in range(len(data)):
            if (i > 0):
                separator=', '
            if (self.types[i].find('varchar') >= 0):
                self.sql_data += separator + '\'' + str(data[i]) + '\'' 
            else:
                self.sql_data += separator +  str(data[i])
        self.sql_data += ')'
        cursor = self.conn.cursor()
        cursor.execute(self.sql_data)
        self.conn.commit()
    
    def writeOutput (self, mode='a', clear=True):
        self.sql_data = self.sql_insert + ' values ('
        separator = ''
        for i in range(len(self.rowsOut)):
            if (i > 0):
                separator=', '
            self.sql_data += separator + '(' + self.rowsOut[i] + ')'
            cursor = self.conn.cursor()
            cursor.execute(self.sql_data)
            self.conn.commit()
        if (clear==True):
            self.rowsOut = []


class csvWriter (writer):
    def __init__(self, fileOut=None, tableOut=None, columns=None, formats=None, logger=None
                    ):
        super(csvWriter, self).__init__(fileOut, tableOut, columns, formats, logger)
        self.rowsOut.append (columns)
        self.writeOutput(mode='w',clear=True)

    def writeOutput (self, mode='a', clear=True):

        self.log ('Outputting {0} rows to file {1}'.format(len(self.rowsOut), os.path.basename(self.fileOut)))
        with open(self.fileOut, mode) as fp:
            fp.write("\n".join(str(row) for row in self.rowsOut)) 
            fp.write('\n')   
        if (clear==True):
            self.rowsOut = []
    