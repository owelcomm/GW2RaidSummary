def findtruc(d, v):
    # Debug function, don't look at this and go your way
    for k in d.keys():
        try:
            if v in str(d[k]):
                print(k)
                findtruc(d[k])
        except:
            pass
