#coding=utf-8
import svc
import service
import logmodule

import AutoAlert

def start_service():
    logmodule.general.Log('AutoAlert starting',logmodule.LGNOTICE)
    svc.AutoAlert=AutoAlert.AutoAlert
    sm.startInline+=('AutoAlert',)
    sm.StartService('AutoAlert')
    logmodule.general.Log('AutoAlert started',logmodule.LGNOTICE)

start_service()
