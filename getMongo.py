import cnfOperations as cnf
import pymongo
import pandas as pd


class GetMongo():
    @staticmethod
    def get_value_mongo():
        myclient = pymongo.MongoClient(cnf.cnfOperation.readMongoDb())
        mydb = myclient[cnf.cnfOperation.readMy_Db()]
        mycol = mydb[cnf.cnfOperation.readMy_Col()]
        mydoc_all = mycol.find()
        df = pd.DataFrame(list(mydoc_all))
        return df.to_csv("abc.csv", sep=",")
