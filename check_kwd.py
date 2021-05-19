from src.trendsetter import Trendsetter
import subprocess

kwd = '/m/04n7dpf' # Topic "Interest Rate"

ts = Trendsetter()

interest = ts.get_interest(kwd, 'today 3-m')
if interest.iat[-1,0] > 90:
    subprocess.run(["/usr/bin/zenity", "--notification",
                    "--text", "Hot topic: Interest rate"])
