import logmodule
import util
import eve.client.script.util.contractutils as cutils
import contractutils 
import eve.client.script.ui.shared.neocom.contracts.contractentry as contractentry
import eve.client.script.ui.shared.neocom.contracts.contracts as contracts
import eve.client.script.ui.shared.market.buyMultiFromBase as buyMultiFromBase

# Improve the legibility of numbers
def FormatDigit(amount):
    amount = long(amount)
    if amount % 100 == 0:
        return "%.0f" % (amount / 100.0)
    elif amount % 10 == 0:
        return "%.1f" % (amount / 100.0)
    else :
        return "%.2f" % (amount / 100.0)

def zhFmtISKWithDescription(isk, justDesc = False):
    iskFmt = util.FmtISK(isk, showFractionsAlways=0)
    
    if abs(isk) >= 1000000000000:
        cnISKfmt = u"%s \u4e07\u4ebf ISK" % FormatDigit(isk / 10000000000)
        iskFmt = u"%s (%s)" % (iskFmt, cnISKfmt)
    elif abs(isk) >= 100000000:
        cnISKfmt = u"%s \u4ebf ISK" % FormatDigit(isk / 1000000)
        iskFmt = u"%s (%s)" % (iskFmt, cnISKfmt)
    elif abs(isk) >= 10000:
        cnISKfmt = u"%s \u4e07 ISK" % FormatDigit(isk / 100)
        iskFmt = u"%s (%s)" % (iskFmt, cnISKfmt)
    else:
        cnISKfmt = iskFmt
    
    if justDesc:
        return cnISKfmt
    else:
        return iskFmt

def RunPatch():
    cutils.FmtISKWithDescription = zhFmtISKWithDescription
    contractutils.FmtISKWithDescription = zhFmtISKWithDescription
    contractentry.FmtISKWithDescription = zhFmtISKWithDescription
    contracts.FmtISKWithDescription = zhFmtISKWithDescription
    buyMultiFromBase.FmtISKWithDescription = zhFmtISKWithDescription
    logmodule.general.Log("Code Injected: zhFmt", logmodule.LGNOTICE)

    

