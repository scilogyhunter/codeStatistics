# codeStatistics
codeStatistics.py 用于统计C语言工程中的文件数和代码行数.

需要先安装Python运行环境。
执行方法：.\codeStatistics.py .\libsylixos\
可以指定要统计的文件夹路经，不指定则默认统计当前路劲下的代码。

执行codeStatistics后会在运行窗口显示统计信息，然后按任意键退出。
同时还会生成record.csv和record.txt记录文件，其中record.csv可以用Excel表格打开。
codeStatistics每次执行只对一个文件夹及其子文件夹进行代码统计，并向记录文件添加一行统计信息。