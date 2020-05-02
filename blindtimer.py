from datetime import datetime

class BlindTimer:

    __BLINDS = [100, 200, 300, 400, 500, 600, 800, 1000, 1500, 2000, 3000, 4000, 5000, 10000, 20000, 40000, 50000]

    def __init__(self, blindinterval):
        self.__blindinterval = blindinterval
        self.__blinds = (self.__BLINDS[0], self.__BLINDS[0] * 2)
        self.__blindlimit = len(self.__BLINDS) - 1
        self.__blindcount = 0
        self.__starttime = datetime.utcnow().timestamp()

    def getblinds(self):
        ts = datetime.utcnow().timestamp()
        blindsup = (ts - self.__starttime) >= self.__blindinterval
        if blindsup:
            if self.__blindcount < self.__blindlimit:
                self.__blindcount = self.__blindcount + 1
            self.__blinds = (self.__BLINDS[self.__blindcount], self.__BLINDS[self.__blindcount] * 2)
            self.__starttime = ts
        self.__pot = 0
        self.__actcount = 0
        self.__round = ''
        self.__betindex = 0
        self.__playercount = 0
        return self.__blinds

if __name__ == "__main__":
    import time
    b = BlindTimer(1)
    for i in range(0, 20):
        blinds = b.getblinds()
        print(blinds[0], blinds[1])
        time.sleep(1)

