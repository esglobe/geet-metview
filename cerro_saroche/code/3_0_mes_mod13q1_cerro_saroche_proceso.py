import subprocess
import pandas as pd
from datetime import datetime

dates = pd.date_range('2022-01-01','2022-08-01',freq='M')
meses = list(map(lambda x: x.strftime('%Y-%m') , dates))


for mes in meses:

  response = subprocess.run(["python3", "./3_1_mod13q1_cerro_saroche_proceso.py", mes])
