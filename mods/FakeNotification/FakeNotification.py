# coding=utf-8

import util
import blue
import localization
import eve.common.script.util.notificationconst as notificationConst
from notifications.common.notification import Notification

def DoFakeNotification():
	message = u"联盟指挥部，傻逼指挥们，都给老子滚到会议大厅来！"
	notification = Notification(notificationID=1, typeID=notificationConst.notificationTypeServerShutdown, senderID=None, receiverID=session.charid, processed=0, created=blue.os.GetWallclockTime(), data={'text': message})
	notification.subject = u"全屏广播"
	notification.subtext = u"来自：军用馒头"
	sm.ScatterEvent('OnNewNotificationReceived', notification)
	return

