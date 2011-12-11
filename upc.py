def upc2isbn(upc):
    if (upc[0:3] != '978' and upc[0:3] != '979') or not(len(upc)==13 or len(upc) == 18):
        return ""

    if upc[0:3]=='979':
        return upc
    else:
        isbn=upc[3:12]
        multiplier=1
        sum=0
        for digit in isbn:
            sum= sum+(int(digit) * multiplier)
            multiplier=multiplier+1
        checksum=sum % 11

        if checksum == 10:
            checksum = "X"

        return isbn+str(checksum)
