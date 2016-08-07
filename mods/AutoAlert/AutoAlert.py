# coding:utf-8
import types
import logmodule
import blue
import util
import sys
import svc
import service
from carbon.common.script.util.linkUtil import GetShowInfoLink


class AutoAlert(service.Service):
    __guid__ = 'svc.AutoAlert'
    __displayname__ = 'Auto Alert Service'
    __notifyevents__ = ['OnLSC']
    __alertchannel = 0

    def OnLSC(self, channelID, estimatedMemberCount, method, identityInfo, args):
        # logmodule.general.Log("AutoAlert Processing....method:%s chID:%s  id:%s"%(method,channelID,identityInfo),logmodule.LGNOTICE)
        AllianceID, CorpID, CfgLine, Role, CorpRole, WarFac = identityInfo
        Charname = None
        SolarsystemID = None
        if type(CfgLine) == types.IntType:
            CharID = CfgLine
        else:
            CharID = CfgLine[0]
            Charname = CfgLine[1]
        if method == "JoinChannel" and self.__alertchannel != 0:
            logmodule.general.Log("Detected ID:%s(%s) entering" % (Charname, CharID), logmodule.LGNOTICE)
            # 判断是否为本地
            if type(channelID) == types.IntType:
                logmodule.general.Log("Not Local CH", logmodule.LGNOTICE)
                return
            if channelID[0][0] != "solarsystemid2":
                logmodule.general.Log("Not Local CH", logmodule.LGNOTICE)
                return
            SolarsystemID = channelID[0][1]
            if self.Ishostile(CharID):  # 判断声望
                logmodule.general.Log("Sending Alert Message", logmodule.LGNOTICE)
                charInfo = cfg.eveowners.Get(CharID)
                charText = GetShowInfoLink(charInfo.typeID, charInfo.name, itemID=CharID)
                systemText = GetShowInfoLink(const.typeSolarSystem, cfg.evelocations.Get(SolarsystemID).name,
                                             SolarsystemID)
                msg = "%s %s" % (charText, systemText)
                #TODO:消息需要定时检查发送，不能直接发送
                sm.GetService('LSC').SendMessage(self.__alertchannel, msg)  # 往服务器发送
                sm.GetService('LSC').GetChannelWindow(self.__alertchannel).Speak(msg, eve.session.charid,
                                                                                 localEcho=True)  # 本地聊天框刷新
                #self.__AddMessage(msg)
                logmodule.general.Log("Sent Alert Message", logmodule.LGNOTICE)
            else:
                logmodule.general.Log("Safe", logmodule.LGNOTICE)
        elif method == "SendMessage":
            if CharID == session.charid:  # 发言的是自己才有效
                if args[0] == ".startalert" and self.__alertchannel == 0:
                    self.__alertchannel = channelID
                    logmodule.general.Log("Alert Channel Set. CH is %s" % str(self.__alertchannel), logmodule.LGNOTICE)
                elif args[0] == ".stopalert":
                    self.__alertchannel = 0
                    logmodule.general.Log("Alert Channel Cancelled", logmodule.LGNOTICE)
    def __AddMessage(self,msg): #添加消息
    def __SendMessage(self): #发送消息
        pass
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
