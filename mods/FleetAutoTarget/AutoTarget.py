import logmodule
from eve.client.script.ui.shared.fleet.fleetbroadcast import FleetBroadcastView

def PatchFn(fn):
    def wrapper(self):
        ret = fn(self)
        try:
            br = sm.GetService('fleet').GetBroadcastHistory()[0]
            logmodule.general.Log("GetBroadcastListEntry invoked: %s %d %d" % (br.name, br.charID, br.itemID), logmodule.LGNOTICE)
            if br.name in ("Target", "HealArmor", "HealShield"):
                sm.GetService('target').TryLockTarget(br.itemID)
        except:
            pass
        return ret
    return wrapper

def RunPatch():
    FleetBroadcastView.LoadBroadcastHistory = PatchFn(FleetBroadcastView.LoadBroadcastHistory)
    logmodule.general.Log("Code Injected", logmodule.LGNOTICE)
