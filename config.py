phoneId = "C8:14:51:08:8F:3A"
phonePort = "BTSPPServer"
tempId = "data/temperature.csv"
tempPort = 0
preasureId = "C8:14:51:08:8F:3A"
preasurePort = "SMS/MMS"
weightId = "COM1"
weightPort = 0
mixId = "COM3"
mixPort = 0
timeOutData = 60

defaultConfig = """(
        BTClient(0, Device(config.phoneId, config.phonePort)),
        FileClient(1, Device(config.tempId, config.tempPort)),
        BTClient(2, Device(config.preasureId, config.preasurePort)),
        SerialClient(3, Device(config.weightId)),
        SerialClient(4, Device(config.mixId), timeout=3600),
    )"""

fileConfig = """(
        BTClient(0, Device(config.phoneId, config.phonePort)),
        FileClient(1, Device(config.tempId, config.tempPort)),
        BTClient(2, Device(config.preasureId, config.preasurePort)),
        SerialClient(3, Device(config.weightId)),
        FileClient(4, Device("data/mix.csv"))
    )"""


