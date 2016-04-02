import logmodule
import blue
import os

def ExportXML():
    xml = '<eveapi version="2"><result>'
    xml += '<characterID>%d</characterID>' % session.charid
    xml += '<name>%s</name>' % cfg.eveowners.Get(session.charid).name.encode("utf8")
    xml += '<rowset columns="typeID,skillpoints,level,published" key="typeID" name="skills">'

    skills = sm.GetService('skills').GetSkills()
    for skillID in skills:
        #logmodule.general.Log(str(skill), logmodule.LGNOTICE)
        xml += '<row typeID="%d" published="1" level="%d" skillpoints="%d"/>' % (skillID, skills[skillID].skillLevel, skills[skillID].skillPoints)
    xml += '</rowset></result></eveapi>'
    return xml
    
def ExportFile():
    xml = ExportXML()
    directory = blue.sysinfo.GetUserDocumentsDirectory() + '/EVE/SkillsExport/'
    if not os.path.exists(directory):
        os.makedirs(directory)
    filename = directory + '%s.xml' % cfg.eveowners.Get(session.charid).name
    with open(filename, 'w') as f:
        f.write(xml)