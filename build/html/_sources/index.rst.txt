.. documentation master file, created by
   sphinx-quickstart on Sun Jul  4 10:51:36 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Aibee数据平台 - 数仓手册
============================================

.. toctree::

* 数据仓库是数据平台的存储部分，采用维度建模思想构建。
    + 用户主题，主要用于存储直接从业务系统采集过来的最原始的数据。尽量避免直接采用本层数据。
    + 订单主题，在ODS层基础上，根据业务过程建模出来的事实明细层。对ODS层数据进行清洗（去除空值，脏数据，超过极限范围的数据等）。
    + 工单主题，存放实体的属性信息，数据一般从业务库离线维表加工而来。
    + 资产主题，（应用数据层），用于业务应用所使用的指标，一般会同步到应用数据库进行业务系统展示。

.. toctree::
   :maxdepth: 4

   table/Mall-客流
   table/Mall-停车场
   table/工单




