import preload.realdata
import preload.testdata
import preload.testcases


class Preloader():
    adetid = None
    metreid = None
    kiloid = None
    debug = True

    def __init__(self):
        self.kiloid = -1
        self.metreid = -1
        self.adetid = -1

    def preLoad(self):
        if self.debug:
            realdata = preload.realdata.RealData()
            realdata.preloadBaseData()
            self.adetid = realdata.adetid
            self.metreid = realdata.metreid
            self.kiloid = realdata.kiloid
            testdata = preload.testdata.TestData(self.kiloid, self.metreid, self.adetid)
            testdata.preLoadTestData()
        else:
            realdata = preload.realdata.RealData()
            realdata.preloadRealData()
            self.adetid = realdata.adetid
            self.metreid = realdata.metreid
            self.kiloid = realdata.kiloid
