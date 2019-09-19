phoneId = "Phone"
tempId = "00:0E:EA:CF:58:B8"
tempPort = 1
preasureId = "0"
preasurePort = 0
weightId = "/dev/ttyUSB0" #"COM5"
weightPort = 0
mixId = "C8:14:51:08:8F:3A"
mixPort = "BTSPPServer"
timeOutData = 60
btServerPort = 0
loggingLevel = 10 # Debug
serviceName = "pibox"
serviceUUID = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

defaultConfig = """(
        BTClient(0, Device(config.phoneId)),
        BTClient(1, Device(config.tempId, config.tempPort)),
        MockClient(2, Device(1000)),
        SerialClient(3, Device(config.weightId)),
        SerialClient(4, Device(config.mixId), timeout=3600),
    )"""

hardwareConfig = """(
        BTClient("pho", Device(config.phoneId)),
        BTClient("tem", Device(config.tempId, config.tempPort)),
        BTClient("pre", Device(config.preasureId, config.preasurePort)),
        SerialClient("wei", Device(config.weightId)),
        BTClient("mix", Device(config.mixId, config.mixPort)),
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

