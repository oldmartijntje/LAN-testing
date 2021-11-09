#DEBUG
# PAUSE SCRIPT, MAKE SOUND AND WAIT TILL KEY IS PRESSED, PUT A BREAKPOINT AT "print("debug")"
import threading, winsound, time
def input_thread(wait):
    input()
    wait.append(True)
wait = []
threading.Thread(target=input_thread, args=(wait,)).start()
while not wait:
    winsound.Beep(700, 100)
    time.sleep(.3)
    print("yeet")
print("debug")
# PAUSE SCRIPT, MAKE SOUND AND WAIT TILL KEY IS PRESSED, PUT A BREAKPOINT AT "print("debug")"
#DEBUG
