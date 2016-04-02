import evetypes
import blue
import os

def ExportTXT():
    txt = ''
    skills = sm.GetService('skills').GetSkills()
    for skillID in skills:
        txt += '%s=%d\n' % (evetypes.GetName(skillID), skills[skillID].skillLevel)
    return txt
    
def ExportFile():
    txt = ExportTXT()
    directory = blue.sysinfo.GetUserDocumentsDirectory() + '/EVE/SkillsExport/'
    if not os.path.exists(directory):
        os.makedirs(directory)
    filename = directory + '%s.txt' % cfg.eveowners.Get(session.charid).name
    with open(filename, 'w') as f:
        f.write(txt.encode("gbk"))