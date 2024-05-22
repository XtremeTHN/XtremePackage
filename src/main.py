from modules.progress import Progress
import time

prog = Progress()

for x in range(0,100):
    prog.update(x)
    prog.print(x)
    
    time.sleep(0.2)