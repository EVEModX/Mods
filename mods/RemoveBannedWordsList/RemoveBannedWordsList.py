import localization
from localization.localizationBase import Localization as l10n

def RunPatch():
    if hasattr(l10n, "_EVEMODX_RemoveBannedWord_GetByLabel"):
        return False
    l10n._EVEMODX_RemoveBannedWord_GetByLabel = l10n.GetByLabel
    def NewGetByLabel(self, labelNameAndPath, languageID = None, **kwargs):
        if labelNameAndPath == "UI/Chat/ChannelWindow/ChinaServerBannedWords":
            return ""
        return l10n._EVEMODX_RemoveBannedWord_GetByLabel(self, labelNameAndPath, languageID, **kwargs)

    l10n.GetByLabel = NewGetByLabel
    localization.GetByLabel = localization.__GetLocalization().GetByLabel
    return True
