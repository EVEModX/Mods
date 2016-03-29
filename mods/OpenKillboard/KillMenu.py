import logmodule
import blue
import util
from eve.client.script.ui.services.menusvc import MenuSvc

import config

def OpenKillInfo(charid):
    kburl = 'http://kb.ceve-market.org/pilot/%d/' % charid
    if config.USE_IGB:
        uicore.cmd.OpenBrowser(kburl)
    else:
        blue.os.ShellExecute(kburl)

def PatchFn(fn):
    def wrapper(self, charid, corpid, unparsed = 0, filterFunc = None, multi = 0, **kwargs):
        ret = fn(self, charid, corpid, unparsed, filterFunc, multi, **kwargs)
        if not util.IsNPC(charid):
            ret += [["Open Killboard", OpenKillInfo, (charid,)]]
        return ret
    return wrapper

def RunPatch():
    MenuSvc._CharacterMenu = PatchFn(MenuSvc._CharacterMenu)
    logmodule.general.Log("Code Injected", logmodule.LGNOTICE)
