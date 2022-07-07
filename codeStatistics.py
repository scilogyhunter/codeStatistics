# -*- coding:utf-8 -*-
# 开发者：科技猎人 scilogyhunter  2019.02.27
# 仓库地址：https://github.com/scilogyhunter/codeStatistics

import os
import re
import sys
import time


#统计一个文件的总行数，代码行数，注释行数，空行数
#某一行可能既有代码又有注释，此时相应行数都会增加
def CalcLines(f):
    lineNo       = 0
    totalLines   = 0
    codeLines    = 0
    commentLines = 0
    emptyLines   = 0
    
    lineList    = f.readlines()
    totalLines  = len(lineList)

    while lineNo < totalLines:
        if lineList[lineNo].isspace():  #空行
            emptyLines += 1; 
            lineNo += 1; 
            continue

        regMatch = re.match('^([^/]*)/(/|\*)+(.*)$', lineList[lineNo].strip())
        if regMatch != None:  #注释行
            commentLines += 1

            #代码&注释混合行
            if regMatch.group(1) != '':
                codeLines += 1
            elif regMatch.group(2) == '*' \
                and re.match('^.*\*/.+$', regMatch.group(3)) != None:
                codeLines += 1

            #行注释或单行块注释
            if '/*' not in lineList[lineNo] or '*/' in lineList[lineNo]:
                lineNo += 1; continue

            #跨行块注释
            lineNo += 1
            while 1:
                try:
                    line = lineList[lineNo]
                except:
                    #print ("except\r")
                    return [totalLines, codeLines, commentLines, emptyLines]
                else:
                    if '*/' in line:
                        commentLines += 1  #'*/'所在行
                        break
                    else:
                        if line.isspace():
                            emptyLines += 1
                        else:
                            commentLines += 1
                        lineNo = lineNo + 1
                        continue
                    
        else:  #代码行
            codeLines += 1

        lineNo += 1
        continue

    return [totalLines, codeLines, commentLines, emptyLines]


class codeStatistic:
    '代码统计基类'
    
    def __init__(self, path):
        self.path                   = path  #统计路径
        self.filetype               = {'.c': 0, '.h': 0, '.cpp': 0, '.hpp': 0, '.s': 0, '.S': 0, '.asm': 0} #统计文件类型
        self.num_dirs               = 0     #路径下文件夹数量
        self.num_files              = 0     #路径下文件数量,包括子文件夹里的文件数量
        self.num_effectivefiles     = 0     #总有效文件数
        self.num_totalLines         = 0     #总行数
        self.num_codeLines          = 0     #总代码行数
        self.num_commentLines       = 0     #总注释行数
        self.num_emptyLines         = 0     #总空行数
        self.num_targetfilesize     = 0     #所有目标文件总大小统计
        self.num_totalfilesize      = 0     #所有文件总大小统计
    def __del__(self):
        pass
    
    def statistic(self):#统计数据
        starttime = time.time()
        
        for root,dirs,files in os.walk(self.path):    #遍历统计
            for name in dirs:
                self.num_dirs += 1
            for name in files:
                filepath = os.path.join(root, name)
                self.num_files += 1                   #总文件数统计
                self.num_totalfilesize += os.path.getsize(filepath)  #总文件大小统计

                type = os.path.splitext(name)[1]                                    #获取文件后缀名
                if type in self.filetype:                                            #判定是否为要统计的文件类型
                    self.num_effectivefiles += 1
                    self.filetype[type]     += 1                                         #目标类型文件数统计
                    self.num_targetfilesize += os.path.getsize(filepath)  #所有目标文件总大小统计
                    with open(filepath, 'r', encoding='gb18030',errors='ignore') as f:
                        totalLines, codeLines, commentLines, emptyLines = CalcLines(f)
                        self.num_totalLines     += totalLines
                        self.num_codeLines      += codeLines
                        self.num_commentLines   += commentLines
                        self.num_emptyLines     += emptyLines
        self.timecast = time.time() - starttime
        self.execdate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    
    def display(self):#显示统计结果
        #文件层面的统计
        print ("path = %s \r" % (self.path))
        print ("-"*20 + "  files  " + "-"*20)
        print ("total dirs      = %10d \r" % (self.num_dirs))
        print ("total files     = %10d \r" % (self.num_files))
        print ("effective       = %10d \r" % (self.num_effectivefiles))
        for type in self.filetype:
            print ("%5s files     = %10d \r" % (type, self.filetype[type]))
        print ("file per dir    = %13.2f\r" % (self.num_files / self.num_dirs))
        #代码行层面的统计
        print ("-"*20 + "  lines " + "-"*20)
        
        print ("totalLines      = %10d \r" % (self.num_totalLines))
        print ("codeLines       = %10d      %6.2f%%\r" % (self.num_codeLines, (self.num_codeLines * 100 / self.num_totalLines)))
        print ("commentLines    = %10d      %6.2f%%\r" % (self.num_commentLines, (self.num_commentLines * 100 / self.num_totalLines)))
        print ("emptyLines      = %10d      %6.2f%%\r" % (self.num_emptyLines, (self.num_emptyLines * 100 / self.num_totalLines)))
        
        print ("line per file   = %13.2f\r" % (self.num_totalLines / self.num_effectivefiles))
        
        #字符层面的统计
        print ("-"*20 + "  chars  " + "-"*20)
        print ("totalfilesize   = %10d\r"  % (self.num_totalfilesize))
        print ("targetfilesize  = %10d\r"  % (self.num_targetfilesize))
        print ("char per line   = %13.2f\r" % (self.num_targetfilesize/(self.num_totalLines - self.num_commentLines)))
        print ("char per file   = %13.2f\r" % (self.num_targetfilesize/self.num_effectivefiles))
        #时间信息
        print ("-"*20 + "  time   " + "-"*20)
        print ("time cast : %fs\r" % (self.timecast))
        print ("execdate  : %s\r" % (self.execdate))
        
        #结束
        print ("-"*20 + "   end   " + "-"*20)

    def record(self):#记录统计结果
        fout = os.getcwd() + "\\record.txt"

        #字段说明
        if not os.path.exists(fout):
            with open(fout, 'w') as f:
                f.write("%-20s\t" % ("date"))
                f.write("%-32s\t" % ("path"))
                f.write("%10s\t" % ("totalD"))
                f.write("%10s\t" % ("totalF"))
                f.write("%10s\t" % ("effectiveF"))
                f.write("%10s\t" % (".c"))
                f.write("%10s\t" % (".h"))
                f.write("%10s\t" % (".cpp"))
                f.write("%10s\t" % (".hpp"))
                f.write("%10s\t" % (".s"))
                f.write("%10s\t" % (".S"))
                f.write("%10s\t" % (".asm"))
                f.write("%10s\t" % ("fpd"))
                f.write("%10s\t" % ("total"))
                f.write("%10s\t" % ("codeL"))
                f.write("%10s\t" % ("commentL"))
                f.write("%10s\t" % ("empty"))
                f.write("%10s\t" % ("codeL%"))
                f.write("%10s\t" % ("commentL%"))
                f.write("%10s\t" % ("emptyL%"))
                f.write("%10s\t" % ("lpf"))
                f.write("%10s\t" % ("totalFS"))
                f.write("%10s\t" % ("targetFS"))
                f.write("%10s\t" % ("cpl"))
                f.write("%10s\t" % ("cpf"))
                f.write("%10s\t" % ("time cast"))

                f.write("\r")
        #字段信息
        with open(fout, 'a+') as f:
            f.write("%-20s\t" % (self.execdate))
            f.write("%-32s\t" % (self.path))

            f.write("%10d\t" % (self.num_dirs))
            f.write("%10d\t" % (self.num_files))
            f.write("%10d\t" % (self.num_effectivefiles))
            for type in self.filetype:
                f.write("%10d\t" % (self.filetype[type]))
            f.write("%10.2f\t" % (self.num_files / self.num_dirs))
            f.write("%10d\t" % (self.num_totalLines))
            f.write("%10d\t" % (self.num_codeLines))
            f.write("%10d\t" % (self.num_commentLines))
            f.write("%10d\t" % (self.num_emptyLines))
            
            f.write("%9.2f%%\t" % (self.num_codeLines * 100 / self.num_totalLines))
            f.write("%9.2f%%\t" % (self.num_commentLines * 100 / self.num_totalLines))
            f.write("%9.2f%%\t" % (self.num_emptyLines * 100 / self.num_totalLines))
            
            f.write("%10.2f\t" % (self.num_totalLines / self.num_effectivefiles))
            
            f.write("%10d\t"  % (self.num_totalfilesize))
            f.write("%10d\t"  % (self.num_targetfilesize))
            f.write("%10.2f\t" % (self.num_targetfilesize/(self.num_totalLines - self.num_commentLines)))
            f.write("%10.2f\t" % (self.num_targetfilesize/self.num_effectivefiles))
            f.write("%9.2fs\t" % (self.timecast))
            f.write("\r")


    def recordcsv(self):#记录统计结果
        fout = os.getcwd() + "\\record.csv"

        #字段说明
        if not os.path.exists(fout):
            with open(fout, 'w') as f:
                f.write("%s," % ("date"))
                f.write("%s," % ("path"))
                f.write("%s," % ("total dir"))
                f.write("%s," % ("total files"))
                f.write("%s," % ("effective files"))
                f.write("%s," % (".c"))
                f.write("%s," % (".h"))
                f.write("%s," % (".cpp"))
                f.write("%s," % (".hpp"))
                f.write("%s," % (".s"))
                f.write("%s," % (".S"))
                f.write("%s," % (".asm"))
                f.write("%s," % ("fpd"))
                f.write("%s," % ("totaline"))
                f.write("%s," % ("codeline"))
                f.write("%s," % ("commentline"))
                f.write("%s," % ("emptyline"))
                f.write("%s," % ("codeline%"))
                f.write("%s," % ("commentline%"))
                f.write("%s," % ("emptyline%"))
                f.write("%s," % ("lpf"))
                f.write("%s," % ("total size"))
                f.write("%s," % ("effective size"))
                f.write("%s," % ("cpl"))
                f.write("%s," % ("cpf"))
                f.write("%s," % ("time cast"))

                f.write("\r")
        #字段信息
        with open(fout, 'a+') as f:
            f.write("%s," % (self.execdate))
            f.write("%s," % (self.path))

            f.write("%d," % (self.num_dirs))
            f.write("%d," % (self.num_files))
            f.write("%d," % (self.num_effectivefiles))
            for type in self.filetype:
                f.write("%d," % (self.filetype[type]))
            f.write("%.2f," % (self.num_files / self.num_dirs))
            f.write("%d," % (self.num_totalLines))
            f.write("%d," % (self.num_codeLines))
            f.write("%d," % (self.num_commentLines))
            f.write("%d," % (self.num_emptyLines))
            
            f.write("%.2f%%," % (self.num_codeLines * 100 / self.num_totalLines))
            f.write("%.2f%%," % (self.num_commentLines * 100 / self.num_totalLines))
            f.write("%.2f%%," % (self.num_emptyLines * 100 / self.num_totalLines))
            
            f.write("%.2f," % (self.num_totalLines / self.num_effectivefiles))
            
            f.write("%d,"  % (self.num_totalfilesize))
            f.write("%d,"  % (self.num_targetfilesize))
            f.write("%.2f," % (self.num_targetfilesize/(self.num_totalLines - self.num_commentLines)))
            f.write("%.2f," % (self.num_targetfilesize/self.num_effectivefiles))
            f.write("%.2fs," % (self.timecast))
            f.write("\r")



if __name__ == "__main__":

    if len(sys.argv) == 1:
        path = os.getcwd()    #获取当前路径
    else:
        path = sys.argv[1]
        
    cs = codeStatistic(path)
    cs.statistic()
    cs.display()
    cs.record()
    cs.recordcsv()

    os.system('pause')

