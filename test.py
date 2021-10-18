#!/usr/bin/env python
# encoding: utf-8
"""
@author: HanYunsong
@contact: yshan@aibee.com
@time: 2021/10/18 10:05 上午
@desc: test
"""
from pyhive import hive
import subprocess
import pymysql
import pandas as pd
from os import path
from os import system


def getHiveConn(host, port, auth, KSN):
    subprocess.call('kinit -kt /etc/bigdata.keytab bigdata', shell=True)
    conn = hive.Connection(host=host,
                           port=port,
                           auth=auth,
                           kerberos_service_name=KSN,
                           )
    cursor = conn.cursor()
    return cursor


def getMySQLTables(host, user, passwd, database):
    conn = pymysql.connect(host=host, user=user, passwd=passwd, database=database)
    cursor = conn.cursor()
    sql = "select subject,layer,db_name,tb_name from dw_manual_conf_test"
    try:
        cursor.execute(sql)
        conn.commit()
    except:
        conn.rollback()
    result = cursor.fetchall()
    list = []
    for res in result:
        list.append(res[0] + '.' + res[1] + '.' + res[2] + '.' + res[3])
    return list


def createRST(lpath, spath, subject, layernm, tablename):
    if not path.exists(f'{spath}.rst'):
        subprocess.call(f'touch {spath}.rst', shell=True)
        subjectfile = open(f'{spath}.rst', 'w', encoding='utf-8')
        sword = f'''{subject}主题
==========================

.. toctree::

* 数据仓库是数据平台的存储部分，采用维度建模思想构建。
    + ODS层（操作数据层），主要用于存储直接从业务系统采集过来的最原始的数据。尽量避免直接采用本层数据。
    + DWD层（明细数据层），在ODS层基础上，根据业务过程建模出来的事实明细层。对ODS层数据进行清洗（去除空值，脏数据，超过极限范围的数据等）。
    + DIM层（维度数据层），存放实体的属性信息，数据一般从业务库离线维表加工而来。
    + ADS层（应用数据层），用于业务应用所使用的指标，一般会同步到应用数据库进行业务系统展示。
    + BI层（MySQL BI 后端层），用于BI 业务指标的后端 Service，存储于 MySQL 中。

.. toctree::
   :maxdepth: 3

'''
        subjectfile.write(sword)
    # subjectfile.write(f"\n   {subject}/{layernm}")
    if not path.exists(f'{lpath}.rst'):
        sfile = open(f'{spath}.rst', 'a', encoding='utf-8')
        sfile.write(f"\n   {subject}/{layernm}")

        subprocess.call(f'touch {lpath}.rst', shell=True)
        layerfile = open(f'{lpath}.rst', 'a', encoding='utf-8')
        lword = f'''============
{layernm.upper()} 层
============

数据表描述
==========

.. csv-table::
   :widths: auto
   :header-rows: 1
   :file: {layernm}.csv


数据表一览
===========

.. toctree::
   :maxdepth: 1

'''
        layerfile.write(lword)


    if not path.exists(f'{lpath}/{tablename}.rst'):
        tablefile = open(f'{lpath}/{tablename}.rst', 'a', encoding='utf-8')
        tword = f'''============================================
{tablename}
============================================


.. csv-table:: {tablename} 字段一览
   :widths: auto
   :header-rows: 1
   :file: {tablename}.csv
'''
        tablefile.write(tword)
        lfile = open(f'{lpath}.rst', 'a', encoding='utf-8')
        lfile.write(f"\n   {layernm}/{tablename}")



def createTableCSV(lpath,tablename, table_info={}):
    dataframe = pd.DataFrame(table_info)
    if not path.exists(f'{lpath}.csv'):
        dataframe.to_csv(f'{lpath}.csv', index=False, sep=',')
    else:
        if not path.exists(f'{lpath}/{tablename}.csv'):
            dataframe.to_csv(f'{lpath}.csv', index=False, header=False, mode='a')


def createTableSQLFile(tablename, sql_info):
    name = tablename.split('.')[0]

    # if not path.exists(f'{savePath}{name}.sql'):
    #     system(f'touch {savePath}{name}.sql')
    file = open(f'{savePath}{name}.sql', 'a', encoding='utf-8')
    file.write(f"{sql_info}\n")


def createColumnCSV(tpath, columns, partitions):
    column_info = []
    partdic = {'brand': '甲方ID', 'city': '甲方所在城市', 'site': '甲方所在站点', 'dt': '统计日期'}
    for item in columns:
        comment = item[2].replace('?', '')
        if item[0] in partitions:
            if item[0] in partdic.keys():
                comment = partdic[item[0]]
            column_info.append({u'列名': item[0], u'字段类型': item[1], u'描述': comment, u'是否分区列': u'分区列'})
        else:
            column_info.append({u'列名': item[0], u'字段类型': item[1], u'描述': comment, u'是否分区列': ''})
    dataframe = pd.DataFrame(column_info)
    if path.exists(f'{tpath}.csv'):
        subprocess.call(f'rm {tpath}.csv', shell=True)
    dataframe.to_csv(f'{tpath}.csv', index=False, sep=',')


def getTables(tablename):
    hcursor.execute(f"show create table {tablename}")
    data = hcursor.fetchall()
    table_info = []
    str = ''
    if 'VIEW' in data[0][0]:
        for i in range(len(data)):
            str += data[i][0]
        str += ';'
        table_info.append({u'表名': tablename, u'表类型': '视图', u'用途描述': ''})
        # table_info.append({u'表名': tablename, u'用途描述': ''})
    else:
        table_info.append({u'表名': tablename, u'表类型': '物理表', u'用途描述': ''})
        # table_info.append({u'表名': tablename, u'用途描述': ''})
        for i in range(len(data)):
            if 'ROW FORMAT' in data[i][0]:
                if 'Parquet' in data[i + 1][0]:
                    str += ' STORED AS PARQUET;'
                else:
                    str += ';'
                break
            else:
                if data[i][0].startswith('COMMENT'):
                    comment = data[i][0].split('\'')[1]
                    table_info.clear()
                    table_info.append({u'表名': tablename, u'表类型': '物理表', u'用途描述': f'{comment}'.replace(u'?', '')})
                    # table_info.append({u'表名': tablename,  u'用途描述': f'{comment}'.replace(u'?', '')})
                str += data[i][0].replace('?', '')
    return str, table_info


def getColums(tablename):
    sql = f'desc {tablename}'
    columns_info = []
    hcursor.execute(sql)
    res = hcursor.fetchall()
    for item in res:
        if item[0] == '':
            break
        columns_info.append(item)
    return columns_info


def getPartitionColumns(tablename):
    sql = f'desc {tablename}'
    hcursor.execute(sql)
    res = hcursor.fetchall()
    part_column = []
    for i in range(len(res)):
        if '# Partition Information' in res[i][0]:
            for j in range(i + 3, len(res)):
                part_column.append(res[j][0])
            break
        else:
            continue
    return part_column


def buildCSVAndRTS(tables):
    for table in tables:
        name = table.split('.')
        subject = name[0]
        layernm = name[1]
        tablenm = name[2] + '.' + name[3]
        lpath = savePath + subject + '/' + layernm
        spath = savePath + subject
        tpath = lpath + '/' + tablenm
        # print(subject,layernm,tablenm)
        if path.exists(f'{savePath}{subject}/{layernm}/{tablenm}.csv'):
            print(tablenm + 'is exists')
            continue
        else:
            print('create ' + tablenm)
            subprocess.call(f'mkdir -p {savePath}{subject}/{layernm}', shell=True)
            tables = getTables(tablenm)
            table_info = tables[1]
            createRST(lpath, spath, subject, layernm, tablenm)
            createTableCSV(lpath, tablenm, table_info)
            partitions = getPartitionColumns(tablenm)
            columns = getColums(tablenm)
            createColumnCSV(tpath, columns, partitions)


if __name__ == '__main__':
    hcursor = getHiveConn('bj-yarn-cm02.aibee.cn', 10000, 'KERBEROS', 'hive')
    tables = getMySQLTables("bj-ops016.aibee.cn", "dw_etl_admin_w", "uy6Q5fLAmz0o", "dw_etl_prod")
    savePath = './source/table/'
    buildCSVAndRTS(tables)
