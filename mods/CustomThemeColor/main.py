from eve.client.script.ui.shared import colorThemes
from CustomThemeColor import config

colorThemes.THEMES = config.THEMES + colorThemes.THEMES
sm.GetService('uiColor').SetThemeID(config.ThemeID)
