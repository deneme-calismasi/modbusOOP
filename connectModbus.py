import numpy as np
from pyModbusTCP.client import ModbusClient
import cnfOperations as cnf


class ConnectModbus():
    @staticmethod
    def connect_modbus():
        host = cnf.cnfOperation.readModBusHost()
        port = cnf.cnfOperation.readModBusPort()
        count = int(cnf.cnfOperation.readModBusCount())

        sensor_no = ModbusClient(host=host, port=port, unit_id=1, auto_open=True)
        sensor_no.open()
        regs = sensor_no.read_holding_registers(0, count)
        if regs:
            print(regs)
        else:
            print("read error")

        for n in range(count // 2):
            data_count = n * 2
            regs[data_count], regs[data_count + 1] = regs[data_count + 1], regs[data_count]

        dec_array = regs

        data_bytes = np.array(dec_array, dtype=np.uint16)
        data_as_float = data_bytes.view(dtype=np.float32)
        return data_as_float
