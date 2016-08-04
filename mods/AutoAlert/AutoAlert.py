#coding:utf-8
import types
import logmodule
import blue
import util
import sys
import svc
import service
class AutoAlert(service.Service):
    __guid__ = 'svc.AutoAlert'
    __displayname__ = 'Auto Alert Service'
    __notifyevents__ = ['OnLSC']
    __alertchannel = 0

    def OnLSC(self, channelID, estimatedMemberCount, method, identityInfo, args):
        logmodule.general.Log("AutoAlert Processing....",logmodule.LGNOTICE)
        AllianceID, CorpID, CfgLine, Role, CorpRole, WarFac = identityInfo
        if type(CfgLine) == types.IntType:
            CharID = CfgLine
        else:
            CharID = CfgLine[0]
        if method == "JoinChannel" and self.__alertchannel != 0:
            #判断是否为本地
            if type(channelID)==types.IntType:
                return
            if channelID[0]!="solarsystemid2":
                return
            if self.Ishostile(CharID):  # 判断声望
                sm.GetService('LSC').SendMessage(self.__alertchannel,"warning for"+CharID+"entering")
        elif method == "SendMessage":
            if CharID == session.charid:  # 发言的是自己才有效
                if args[0] == ".startalert" and self.__alertchannel == 0:
                    self.__alertchannel = channelID[1]
                    logmodule.general.Log("Alert Channel Set",logmodule.LGNOTICE)
                elif args[0] == ".stopalert":
                    self.__alertchannel = 0

    def Ishostile(self, charid):  # 判断声望 True:报警 False:不报警
        # TODO:实现正确判断声望
        return True
    def Run(self,*args):
        service.Service.Run(self,*args)
