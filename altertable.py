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
    sql = "select db_name,tb_name from dw_manual_conf_test"
    try:
        cursor.execute(sql)
        conn.commit()
    except:
        conn.rollback()
    result = cursor.fetchall()
    list = []
    for res in result:
        list.append(res[0] + '.' + res[1])
    return list

tabless = ['ads_mall_common_bi.ads_mall_arrive_times_statistic_v02', 'ads_mall_common_bi.ads_mall_arrive_times_statistic_v02_temp', 'ads_mall_common_bi.ads_mall_customer_archives_v02', 'ads_mall_common_bi.ads_mall_customer_last_event_v02', 'ads_mall_common_bi.ads_mall_customer_preference_v02', 'ads_mall_common_bi.ads_mall_customer_record_v02', 'ads_mall_common_bi.ads_mall_daily_event_statistic_v02', 'ads_mall_common_bi.ads_mall_daily_flow_statistic_v02', 'ads_mall_common_bi.ads_mall_heat_map_statistic_v02', 'ads_mall_common_bi.ads_mall_person_relation_statistic_v02', 'ads_mall_common_bi.ads_mall_pid_detail_v11', 'ads_mall_common_bi.ads_mall_stay_time_statistic_v02', 'ads_mall_common_bi.ads_mall_stay_time_sum_full_v11', 'ads_mall_common_bi.ads_mall_time_event_statistic_v02', 'ads_mall_common_bi.ads_mall_user_events_full_v11', 'ads_mall_common_bi.ads_mall_user_events_v02', 'dw.dim_car_info', 'dw.dim_person_info', 'dw.dim_person_info_global_mallbi', 'dw.dim_person_info_local', 'dw.dim_store_info_current', 'dw_staging.dim_activity_area_his_v1', 'dw_staging.dim_brand_info_v1', 'dw_staging.dim_category_info_v1', 'dw_staging.dim_floor_mapping_v1', 'dw_staging.dim_gate_info_v1', 'dw_staging.dim_gpid_merge_info_current_v1', 'dw_staging.dim_gpid_merge_info_his_v1', 'dw_staging.dim_mall_info_v2', 'dw_staging.dim_pid_mapping_current_v1', 'dw_staging.dim_pid_mapping_v1', 'dw_staging.dim_project_info_v1', 'dw_staging.dim_region_info_v1', 'dw_staging.dim_store_brand_info_v1', 'dw_staging.dim_store_info_current_v2', 'dw.dwd_parkinglot_event', 'dw.dwd_parkinglot_lane_pv', 'dw.dwd_parkinglot_spot_occupy', 'dw.dwd_parkinglot_violations', 'dw_staging.dwd_person_event_detail_rawlog_v1', 'dw_staging.dwd_person_event_v1', 'dw_staging.dwd_trajectory_v1', 'dw_staging.ods_faceid_globalpid_mapping_v1', 'dw_staging.ods_face_info_v2', 'dw_staging.ods_gpid_merge_info_v1', 'dw_staging.ods_mall_traffic_v1', 'dw_staging.ods_store_traffic_v1', 'dw_staging.ods_track_v1']
tt=[]
hcursor = getHiveConn('bj-yarn-cm02.aibee.cn', 10000, 'KERBEROS', 'hive')
for tables in tabless :
    hcursor.execute(f"show create table {tables}")
    data = hcursor.fetchall()
    table_info = []
    str = ''
    if 'VIEW' not in data[0][0]:
        for i in range(len(data)):
            if data[i][0].startswith('COMMENT'):
                comment = data[i][0].split('\'')[1]
                # print(f"{tables}  {comment}")
            else: tt.append(tables)
print(tt)





