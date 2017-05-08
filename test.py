#coding=utf-8
# import threading
# from time import ctime,sleep
#
# def music(func):
#     for i in range(2):
#         print ("I was listening to %s. %s" %(func,ctime()))
#         sleep(1)
#
# def move(func):
#     for i in range(2):
#         print ("I was at the %s! %s" %(func,ctime()))
#         sleep(5)
#
# threads = []
# t1 = threading.Thread(target=music,args=(u'爱情买卖',))
# threads.append(t1)
# t2 = threading.Thread(target=move,args=(u'阿凡达',))
# threads.append(t2)
#
# if __name__ == '__main__':
#     for t in threads:
#         t.setDaemon(True)
#         t.start()
#     print ("all over %s" %ctime())



# import urllib.request
# content = urllib.request.urlopen("http://hiaero.net/python-relative-imports/").read().decode("utf-8")
# print(content)

from bs4 import BeautifulSoup
html_doc = """
<p>A bytecode program may be executed by parsing and <i>directly</i> executing the instructions, one at a time. This kind of <i>bytecode interpreter</i> is very portable. Some systems, called dynamic translators, or <i><a href="/wiki/Just-in-time_compilation" title="Just-in-time compilation">just-in-time</a></i> (JIT) compilers, translate bytecode into <a href="/wiki/Machine_code" title="Machine code">machine code</a> as necessary at <a href="/wiki/Run_time_(program_lifecycle_phase)" title="Run time (program lifecycle phase)">runtime</a>. This makes the virtual machine hardware-specific, but doesn't lose the portability of the bytecode. For example, <a href="/wiki/Java_(programming_language)" title="Java (programming language)">Java</a> and <a href="/wiki/Smalltalk" title="Smalltalk">Smalltalk</a> code is typically stored in bytecoded format, which is typically then JIT compiled to translate the bytecode to machine code before execution. This introduces a delay before a program is run, when bytecode is compiled to native machine code, but improves execution speed considerably compared to interpreting source code directly, normally by several orders of magnitude.<sup class="noprint Inline-Template Template-Fact" style="white-space:nowrap;">[<i><a href="/wiki/Wikipedia:Citation_needed" title="Wikipedia:Citation needed"><span title="This claim needs references to reliable sources. (August 2011)">citation needed</span></a></i>]</sup></p>
"""
soup = BeautifulSoup(html_doc,"html.parser")
print(soup.find("p").get_text())









