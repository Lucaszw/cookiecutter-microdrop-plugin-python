import threading
import time

import paho_mqtt_helpers as pmh


class SimplePlugin(pmh.BaseMqttReactor):
        def __init__(self, *args, **kwargs):
            pmh.BaseMqttReactor.__init__(self)
            self.start()

        def listen(self):
            # Subscribe to all state channels of all senders
            self.onStateMsg("{sender}", "{val}", self.onStateMsgReceived)
            # Subscribe to the status of this plugin
            self.onStatusMsg(self.url_safe_plugin_name, self.onStatusReceived)
            self.bindStatusMsg("update-time")
            self.subscribe()
            self.getTime()

        def getTime(self):
            """ Publish Status Every 5 seconds """
            threading.Timer(5.0, self.getTime).start()
            self.trigger("update-time", time.ctime())

        def onStateMsgReceived(self, payload, args):
            """ Print arguments of state message """
            print("Args::")
            print(args)

        def onStatusReceived(self, payload, args):
            """ Print payload of status message """
            print("Payload::")
            print(payload)


if __name__ == '__main__':
    SimplePlugin()
