from wehabcaflazzlibrary.flazz_library import FlazzLibrary

flazz = FlazzLibrary('/dev/tty.UC-232AC',  38400, timeout=8)

errorHandling = flazz.connect()
if not errorHandling.err:
    errHandling = flazz.payment("fewafaew","fewafaew")
    if not errorHandling.err:
        print("Payment Successfully")
    else:
        print("Payment Failed")
else:
    print(errorHandling.message)
