import numpy as np
import datetime as dt
import cnfOperations as cnf
import connectModbus as cm


class ListDict():
    @staticmethod
    def list_to_dict():
        con = cm.ConnectModbus()
        regs_count = int(cnf.cnfOperation.readModBusRegsCount())

        value = [[num for num in range(1, 1 + (regs_count) // 2)],
                 [num for num in range(1, 1 + (regs_count) // 2)],
                 con.connect_modbus()]

        data = np.array(value).T.tolist()

        products = data
        arr = []
        for product in products:
            vals = {}
            vals["Sensor No"] = str(int(product[1]))
            vals["Temp"] = str(round(product[2], 4))
            vals["Time"] = str(dt.datetime.now().strftime('%Y-%m-%d %X'))
            arr.append(vals)
        return arr
