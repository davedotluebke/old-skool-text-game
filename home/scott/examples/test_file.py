while True:
    try:
        coords = float(input(':'))
    except Exception:
        continue
    lat = float(coords.split(',')[0])
    long = float(coords.split(',')[1])
    o_lat = -lat
    o_long = ((long+360) % 360) - 180
    print(str(o_lat)+','+str(o_long))
