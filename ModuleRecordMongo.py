import time
import recordMongo as rec


def main():
    while True:
        rec.RecordMongo.record_mongo()
        print("Kayıt başarılı")
        time.sleep(60)


if __name__ == '__main__':
    main()
