#coding=utf-8
import svc
import service
import logmodule

import AutoAlert

def start_service():
    logmodule.general.Log('AutoAlert 0.0.1 starting',logmodule.LGNOTICE)
    svc.AutoAlert=AutoAlert.AutoAlert
    sm.startInline+=('AutoAlert',)
    sm.StartService('AutoAlert')
    logmodule.general.Log('AutoAlert 0.0.1 started',logmodule.LGNOTICE)

start_service()
