# coding:utf-8
import types
import logmodule
import blue
import stackless
import util
import sys
import svc
import service
from carbon.common.script.util.linkUtil import GetShowInfoLink
from carbon.common.script.util.timerstuff import AutoTimer

class AutoAlert(service.Service):
    __guid__ = 'svc.AutoAlert'
    __displayname__ = 'Auto Alert Service'
    __notifyevents__ = ['OnLSC']
    __alertchannel = 0
    __cachemsgs={}
    __timer= None
    __MAX_NAME_PER_SYSTEM=10 #每个星系最多同时报几个名字 THIS IS A CONFIG LINE. DO NOT CHANGE THIS IN CODE.
    def OnLSC(self, channelID, estimatedMemberCount, method, identityInfo, args):
        # logmodule.general.Log("AutoAlert Processing....method:%s chID:%s  id:%s"%(method,channelID,identityInfo),logmodule.LGNOTICE)
        AllianceID, CorpID, CfgLine, Role, CorpRole, WarFac = identityInfo
        Charname = None
        SolarsystemID = None
        #self.__timer=AutoTimer(5000,self.__SendMessage)
        if type(CfgLine) == types.IntType:
            CharID = CfgLine
        else:
            CharID = CfgLine[0]
            Charname = CfgLine[1]
        if method == "JoinChannel" and self.__alertchannel != 0:
            #logmodule.general.Log("Detected ID:%s(%s) entering" % (Charname, CharID), logmodule.LGNOTICE)
            # 判断是否为本地
            if type(channelID) == types.IntType:
                #logmodule.general.Log("Not Local CH", logmodule.LGNOTICE)
                return
            if channelID[0][0] != "solarsystemid2":
                #logmodule.general.Log("Not Local CH", logmodule.LGNOTICE)
                return
            SolarsystemID = channelID[0][1]
            if self.Ishostile(CharID):  # 判断声望
                #logmodule.general.Log("Sending Alert Message", logmodule.LGNOTICE)
                charInfo = cfg.eveowners.Get(CharID)
                charText = GetShowInfoLink(charInfo.typeID, charInfo.name, itemID=CharID)
                systemText = GetShowInfoLink(const.typeSolarSystem, cfg.evelocations.Get(SolarsystemID).name,
                                             SolarsystemID)
                msg = "%s %s" % (charText, systemText)
                #TODO:消息需要定时检查发送，不能直接发送
                sm.GetService('LSC').SendMessage(self.__alertchannel, msg)  # 往服务器发送
                sm.GetService('LSC').GetChannelWindow(self.__alertchannel).Speak(msg, eve.session.charid,localEcho=True)  # 本地聊天框刷新
                #self.__AddMessage(charText,systemText)
                #logmodule.general.Log("Cached Alert Message", logmodule.LGNOTICE)
            else:
                pass
                #logmodule.general.Log("Safe", logmodule.LGNOTICE)
        elif method == "SendMessage":
            if CharID == session.charid:  # 发言的是自己才有效
                if args[0] == ".startalert":
                    if type(channelID) != types.IntType:
                        return
                    if self.__alertchannel !=0 :
                        sm.GetService('LSC').GetChannelWindow(self.__alertchannel).Speak(u"AutoAlert:Alert havs already started",
                                                                                         eve.session.charid,
                                                                                         localEcho=True)
                    self.__alertchannel = channelID
                    #logmodule.general.Log(u"Alert Channel Set. CH is %s" % str(self.__alertchannel), logmodule.LGNOTICE)
                    sm.GetService('LSC').GetChannelWindow(self.__alertchannel).Speak(u"AutoAlert:Alert started", eve.session.charid,localEcho=True)  # 本地聊天框刷新
                elif args[0] == ".stopalert":
                    if self.__alertchannel == 0:
                        sm.GetService('LSC').GetChannelWindow(self.__alertchannel).Speak(u"AutoAlert:Alert has already stopped",
                                                                                         eve.session.charid,
                                                                                         localEcho=True)
                        return
                    sm.GetService('LSC').GetChannelWindow(self.__alertchannel).Speak(u"AutoAlert:Alert stopped",eve.session.charid, localEcho=True)
                    self.__alertchannel = 0
                    #logmodule.general.Log(u"Alert Channel Cancelled", logmodule.LGNOTICE)
    def __AddMessage(self,char,system): #添加消息
        old=stackless.getcurrent().set_atomic(True)
        try:
            if system not in self.__cachemsgs:
                self.__cachemsgs[system]=[]
            self.__cachemsgs[system].append(char)
        finally:
            stackless.getcurrent().set_atomic(old)
    def __SendMessage(self): #发送消息
        old=stackless.getcurrent().set_atomic(True)
        try:
            for key in self.__cachemsgs:
                msg=""
                if len(self.__cachemsgs[key]) > self.__MAX_NAME_PER_SYSTEM:
                    msg=key+" "+str(len(self.__cachemsgs[key]))+" hostile(s)"
                else:
                    msg=key
                    for name in self.__cachemsgs[key]:
                        msg+=" "+name
                sm.GetService('LSC').SendMessage(self.__alertchannel, msg)  # 往服务器发送
                sm.GetService('LSC').GetChannelWindow(self.__alertchannel).Speak(msg, eve.session.charid,localEcho=True)
        finally:
            stackless.getcurrent().set_atomic(old)
    def Ishostile(self, charid):  # 判断声望 True:报警 False:不报警
        pubinfo = sm.RemoteSvc('charMgr').GetPublicInfo(charid)
        corpID = pubinfo.corporationID
        allianceID = None
        if not util.IsNPC(pubinfo.corporationID):
            allianceID = sm.GetService('corp').GetCorporation(pubinfo.corporationID).allianceID
        ret = sm.GetService('addressbook').GetRelationship(charid, corpID, allianceID)
        relationships = [ret.persToCorp,
                         ret.persToPers,
                         ret.persToAlliance,
                         ret.corpToPers,
                         ret.corpToCorp,
                         ret.corpToAlliance,
                         ret.allianceToPers,
                         ret.allianceToCorp,
                         ret.allianceToAlliance]
        relationship = 0.0
        for r in relationships:
            if r != 0.0 and r > relationship or relationship == 0.0:
                relationship = r
        return relationship <= 0
    def Run(self, *args):
        service.Service.Run(self, *args)
