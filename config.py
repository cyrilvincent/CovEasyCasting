phoneId = "Phone"
tempId = "data/temperature.csv"
tempPort = 0
preasureId = "C8:14:51:08:8F:3A"
preasurePort = "BTSPPServer"
weightId = "COM1"
weightPort = 0
mixId = "COM3"
mixPort = 0
timeOutData = 60
loggingLevel = 10 # Debug
serviceName = "EasyCastingBox"
serviceUUID = "94f72d29-2006-2010-1972-fba39e49d4ff"
btServerPort = 3

defaultConfig = """(
        BTClient(0, Device(config.phoneId)),
        FileClient(1, Device(config.tempId, config.tempPort)),
        MockClient(2, Device(1000)),
        MockClient(3, Device(2500)),
        SerialClient(4, Device(config.mixId), timeout=3600),
    )"""

hardwareConfig = """(
        BTClient(0, Device(config.phoneId)),
        FileClient(1, Device(config.tempId, config.tempPort)),
        BTClient(2, Device(config.preasureId, config.preasurePort)),
        MockClient(3, Device(2500)),
        SerialClient(4, Device(config.mixId), timeout=3600),
    )"""

mockConfig = """(
        MockClient(0, Device(0)),
        FileClient(1, Device("data/temperature.csv")),
        MockClient(2, Device(1000)),
        MockClient(3, Device(2500)),
        FileMixClient(4, Device("data/mix.csv"), timeout=3600)
    )"""

mockExceptPhoneConfig = """(
        BTClient(0, Device(config.phoneId, config.phonePort)),
        FileClient(1, Device("data/temperature.csv")),
        MockClient(2, Device(1000)),
        MockClient(3, Device(2500)),
        FileMixClient(4, Device("data/mix.csv"), timeout=3600)
    )"""

