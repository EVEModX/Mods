from eve.client.script.ui.shared import colorThemes
import ThemeConfig

def AddNewTheme():
    for theme in ThemeConfig.THEMES:
        if theme[0] not in [x[0] for x in colorThemes.THEMES]:
            colorThemes.THEMES = (theme,) + colorThemes.THEMES

def ApplyTheme():
    sm.GetService('uiColor').SetThemeID(ThemeConfig.ThemeID)
