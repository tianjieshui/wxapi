#! /usr/bin/env python
# coding=utf-8
__author__ = 'jszhou'
from bottle import *
import hashlib
import xml.etree.ElementTree as ET
import urllib2
# import requests
import json

def get_parm(token):
    signature = request.GET.get('signature', None)  # ƴд���Ժ������ǣ���signatureд��singnature��ֱ�ӵ�����ôҲ��֤���ɹ�
    timestamp = request.GET.get('timestamp', None)
    nonce = request.GET.get('nonce', None)
    echostr = request.GET.get('echostr', None)
    return [token, timestamp, nonce,signature]
            
def checkSig(token,parm):
    '''token ��ע�������ģ�parm Ϊ[token, timestamp, nonce,signature]'''
    tmpList = parm[:-1]
    tmpList.sort()
    tmpstr = "%s%s%s" % tuple(tmpList)
    hashstr = hashlib.sha1(tmpstr).hexdigest()
    signature=parm[-1]
    if hashstr == signature:
        return True
    else:
        return False
        
def parse_msg():
    """
    ��������������΢��Server Post������XML���ݵģ�ȡ�����ֶζ�Ӧ��ֵ���Ա�����Ĵ�����ã�Ҳ����lxml��ģ�顣
    """
    recvmsg = request.body.read()  # ���ؿ��ǵĵط����������Stack OverFlow���ҵ��˴�
    root = ET.fromstring(recvmsg)
    msg = {}
    for child in root:
        msg[child.tag] = child.text
    return msg
    
def get_app_token(appid,secret):
    #9b01fd9d71c0705577a3d43a9b8bb78d
    #wx36b64bfb413892a8
    url="https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s"
    url2=url%(appid,secret)
    f=urllib2.urlopen(url2)
    buf=f.read()
    f.close()
    print buf
    
    

class process_msg():
    def  process_text(self,rev_msg,text):
        #rev_msg=parse_msg()
        textTpl = """<xml>
             <ToUserName><![CDATA[%s]]></ToUserName>
             <FromUserName><![CDATA[%s]]></FromUserName>
             <CreateTime>%s</CreateTime>
             <MsgType><![CDATA[text]]></MsgType>
             <Content><![CDATA[%s]]></Content>
             <FuncFlag>0</FuncFlag>
             </xml>"""
        echostr = textTpl % (rev_msg['FromUserName'], rev_msg['ToUserName'], str(int(time.time())),text)
        return echostr
        
    def process_pic_txt(self,msg,title="",description="",picurl="",url=""):
        '''����汾����һ��ͼƬ��������������ʽʹ����Ҫ�޸�'''
        pictextTpl = """<xml>
                <ToUserName><![CDATA[%s]]></ToUserName>
                <FromUserName><![CDATA[%s]]></FromUserName>
                <CreateTime>%s</CreateTime>
                <MsgType><![CDATA[news]]></MsgType>
                <ArticleCount>1</ArticleCount>
                <Articles>
                <item>
                <Title><![CDATA[%s]]></Title>
                <Description><![CDATA[%s]]></Description>
                <PicUrl><![CDATA[%s]]></PicUrl>
                <Url><![CDATA[%s]]></Url>
                </item>
                </Articles>
                <FuncFlag>1</FuncFlag>
                </xml> """
        echostr=pictextTpl% (msg['FromUserName'], msg['ToUserName'], str(int(time.time())),title, description,picurl, url)
        return echostr
    
        
