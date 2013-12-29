#! /usr/bin/env python
# coding=utf-8
from bottle import Bottle, run, template,request
from bottle import get,post
from wxapi import *
from bottle import static_file

app = Bottle()

@app.route('/hello')
def hello():
    return "Hello World!"
@app.route('/say_hi/<name>')
def say_hi(name):
    print name
    print request
    return name

@app.get('/weixinloging')
def weixinloging():
    print request 
    print "----------"
    print request.query_string
    return request.query_string
 
@app.get('/')
def zuche():
    print "****"
    s=request.query.get("echostr")
    print s
    print "####"
    return s
    
@app.post("/")
def get_post_msg():
    msg=parse_msg()
    print 'post msg:'
    print msg["Content"].encode("gbk")
    return test_main(msg["Content"],msg)
 
@app.route('/static/:filename')
def server_static(filename):
    print filename
    return static_file(filename, root='/home/weixin/static')
    
def pic(process,msg):
    #msg,title="",description="",picurl="",url=""
    return process.process_pic_txt(msg,u"这个东东很好吃",u"海洋公园的蜘蛛蟹","http://61.166.152.25/static/zhizhu.jpg","http://www.baidu.com")
    
def joke(process,msg):
    text= '''刚入学的时候，全班自我介绍。一男同学走上讲台：\
    “我叫王鹏，来自北京，我爱下棋！”说完就下去了，\
    下一位是个女生，该女娇羞地走上讲台，忐忑不安地自我介绍：\
    “我……我叫夏琪……”。。
    '''
    return    process.process_text(msg,text)

def songs(process,msg):
    return process.process_text(msg,'lai lai songs')
    
def  test_main(arg,msg):
    funs={'1':lambda:pic,
     '2':lambda:joke,
     '3':lambda:songs}
    process=process_msg()
    print funs['1']()(process,msg)
    if arg in funs:
        return    funs[arg]()(process,msg)
    text=u'''回复命令列表
                1.来看个图片
                2.看个笑话
                3.听首歌'''
    return process.process_text(msg,text)
      



run(app, host='61.166.152.25', port=80,reloader=True)
