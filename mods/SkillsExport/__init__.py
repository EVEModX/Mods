import logmodule
import blue

import ExportPyfa
import ExportEFT

if session.charid:
    ExportPyfa.ExportFile()
    ExportEFT.ExportFile()

logmodule.general.Log("EVEModX: SkillsExport", logmodule.LGNOTICE)


