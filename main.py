from cls import CLSCenter

c = CLSCenter("http://cls-test02.hessware.local", "test", "test")

sw = c.getSwitchingPoint("Koffer")

sw.switch(100)
