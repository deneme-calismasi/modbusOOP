import configparser


class cnfOperation():

    @staticmethod
    def readModBusHost():
        config = configparser.ConfigParser()
        config.read('Config.ini')
        return config['Modbus_host']['host']

    @staticmethod
    def readModBusPort():
        config = configparser.ConfigParser()
        config.read('Config.ini')
        return config['Modbus_port']['port']

    @staticmethod
    def readModBusCount():
        config = configparser.ConfigParser()
        config.read('Config.ini')
        return config['Modbus_regs']['count']

    @staticmethod
    def readMongoDb():
        config = configparser.ConfigParser()
        config.read('Config.ini')
        return config['Mongo_DB']['client']

    @staticmethod
    def readMy_Db():
        config = configparser.ConfigParser()
        config.read('Config.ini')
        return config['My_DB']['my_client']

    @staticmethod
    def readMy_Col():
        config = configparser.ConfigParser()
        config.read('Config.ini')
        return config['My_Col']['My_db']
