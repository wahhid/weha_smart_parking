from wehabcaflazzlibrary.flazz_library import FlazzLibrary


flazz = FlazzLibrary('/dev/tty.UC-232AC',  38400, timeout=8)

errorHandling = flazz.connect()
if not errorHandling.err:
    errHandling = flazz.signon()
    if not errorHandling.err:
        print("Sign On Successfully")
    else:
        print("Sign On Failed")
else:
    print(errorHandling.message)
