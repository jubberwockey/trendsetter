from src.trendsetter import Trendsetter
import subprocess

kwds = {'/m/04n7dpf': 'Interest Rate',
        '/m/0gz_4': 'Stock market crash'
       }

ts = Trendsetter()

for kwd, val in kwds.items():
    interest = ts.get_interest(kwd, 'today 3-m')
    if interest.iat[-1,0] > 90:
        subprocess.run(["/usr/bin/zenity", "--notification",
                        "--text", "Hot topic: {}".format(val)])
