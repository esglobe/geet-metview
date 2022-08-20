import subprocess
import pandas as pd
from datetime import datetime

dates = pd.date_range('2012-01-01','2022-09-01',freq='M')
meses = list(map(lambda x: x.strftime('%Y-%m') , dates))


for mes in meses:

  response = subprocess.run(["python3", "./terepaima/code/4_1_mod13q1_terepaima_proceso.py", mes])
