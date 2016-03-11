from eve.client.script.ui.eveCommands import EveCommandService
import bluepy

def RunPatch():
    def NewDoQuitGame(self):
        try:
            sm.GetService('tutorial').OnCloseApp()
            self.settings.SaveSettings()
            sm.GetService('clientStatsSvc').OnProcessExit()
        except:
            self.LogException()
        finally:
            bluepy.Terminate('User requesting close')
    EveCommandService.DoQuitGame = NewDoQuitGame
    