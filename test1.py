from datetime import datetime
import time

print(datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d"))