#!/usr/bin/env python
# encoding: utf-8
"""
@author: HanYunsong
@contact: yshan@aibee.com
@time: 2021/10/8 11:25 下午
@desc: autobuild2
"""
from pyhive import hive
import subprocess
import pymysql
import pandas as pd
from os import path


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
    sql = "select layer,db_name,tb_name from dw_manual_conf"
    try:
        cursor.execute(sql)
        conn.commit()
    except:
        conn.rollback()
    result = cursor.fetchall()
    list = []
    for res in result:
        list.append(res[0] + '.' + res[1] + '.' + res[2])
    return list


def createRST(layernm, tablename):
    lpath = savePath + layernm
    if not path.exists(f'{lpath}.rst'):
        subprocess.call(f'touch {lpath}.rst', shell=True)
        layerfile = open(f'{lpath}.rst', 'w', encoding='utf-8')
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
        file = open(f'{lpath}.rst', 'a', encoding='utf-8')
        file.write(f"\n   {layernm}/{tablename}")


def createTableCSV(layer, tablename, table_info={}):
    dataframe = pd.DataFrame(table_info)
    lpath = savePath + layer
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


def createColumnCSV(layer, tablename, columns, partitions):
    column_info = []
    lpath = savePath + layer
    tpath = lpath + '/' + tablename
    partdic = {'brand': '甲方ID', 'city': '甲方所在城市', 'site': '甲方所在站点', 'dt': '统计日期'}
    for item in columns:
        comment= item[2].replace('?', '')
        if item[0] in partitions:
            if item[0] in partdic.keys():
                comment=partdic[item[0]]
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
        #table_info.append({u'表名': tablename, u'表类型': '视图', u'用途描述': ''})
        table_info.append({u'表名': tablename, u'用途描述': ''})
    else:
        #table_info.append({u'表名': tablename, u'表类型': '物理表', u'用途描述': ''})
        table_info.append({u'表名': tablename, u'用途描述': ''})
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
                    #table_info.append({u'表名': tablename, u'表类型': '物理表', u'用途描述': f'{comment}'.replace(u'?', '')})
                    table_info.append({u'表名': tablename,  u'用途描述': f'{comment}'.replace(u'?', '')})
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
    print(tables)
    for table in tables:
        name = table.split('.')
        layernm = name[0]
        tablenm = name[1] + '.' + name[2]
        if path.exists(f'{savePath}{layernm}/{tablenm}.csv'):
            print(tablenm)
            continue
        else:
            print(tablenm)
            subprocess.call(f'mkdir -p {savePath}{layernm}', shell=True)
            tables = getTables(tablenm)
            table_info = tables[1]
            createTableCSV(layernm, tablenm, table_info)
            createRST(layernm, tablenm)
            partitions = getPartitionColumns(tablenm)
            columns = getColums(tablenm)
            createColumnCSV(layernm, tablenm, columns, partitions)


# def buildHTML():
#     cmd = 'source ~/venv/bin/activate ' \
#           + ' && ' + 'make clean' \
#           + ' && ' + 'make html' \
          # + ' && ' + 'docker build -t nginx_dw_manual:0.0.1 .' \
          # + ' && ' + 'docker run -di --name=nginx -p 90:80  nginx_dw_manual:0.0.1'
    # subprocess.call(cmd, shell=True)


if __name__ == '__main__':
    hcursor = getHiveConn('bj-yarn-cm02.aibee.cn', 10000, 'KERBEROS', 'hive')
    tables = getMySQLTables("bj-ops016.aibee.cn", "dw_etl_admin_w", "uy6Q5fLAmz0o", "dw_etl_prod")
    savePath = './source/table/'
    buildCSVAndRTS(tables)
