import os
import re

if __name__ == "__main__":
    dir = r'Z:\raw_data\2018_03_14_expt018_SK_FUCCI_dose_response\WellB02_Seq0000\0000_transforms'
    fileNames = sorted(os.listdir(dir))
    a = []
    b = []
    for counter, fn in enumerate(fileNames[1:]):
        with open(os.path.join(dir,fn),'r') as f:
            text = f.read()
        pattern = re.compile(r'data="([\d\.E\-\+]+)\s+([\d\.E\-\+]+)"')
        matches = pattern.findall(text)
        # print(text)
        # print(matches)
        atemp = 0
        btemp = 0
        for match in matches:
            # print(match)
            # print(int(float(match[0])))
            # print(int(float(match[1])))
            atemp += round(float(match[0]))
            btemp += round(float(match[1]))
        a.append(atemp)
        b.append(btemp)
    # print(a)
    # print(b)
    # print(str(min(a)) + ' ' + str(min(b)))
    # print(str(max(a)) + ' ' + str(max(b)))
    xshift = max(a)-min(a)
    yshift = max(b)-min(b)
    print('x shift: ' + str(xshift))
    print('y shift: ' + str(yshift))


        # print(matches[0][0])
        # print(matches[1][0])
        # a = int(matches[0][0])+int(matches[1][0])
        # b = int(matches[0][1]) + int(matches[1][1])
        # print(a)
        # print(b)


        # well = list(set([pattern.match(f).group(1) for f in allFiles if pattern.match(f)]))
        # sequence = list(set([pattern.match(f).group(2) for f in allFiles if pattern.match(f)]))
        # times = sorted(set([pattern.match(f).group(3) for f in allFiles if pattern.match(f)]))
        # sites = sorted(set([pattern.match(f).group(4) for f in allFiles if pattern.match(f)]))
        # channels = sorted(set([pattern.match(f).group(5) for f in allFiles if pattern.match(f)]))