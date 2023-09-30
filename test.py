import numpy as np
from numpy.random import RandomState
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

state = RandomState(0)

df = pd.DataFrame({"month":state.randint(1,12,20),
              "hour":state.randint(1,24,20)
              })

# print(df)

sns.heatmap(pd.crosstab(df["month"], df["hour"]), cmap ="Reds",linewidths=1)

plt.show()


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

rng = np.random.default_rng(2022)
df = pd.DataFrame({'Engagement': rng.integers(1000, 100000, 1000),
                   'Weekday': rng.integers(0, 7, 1000),
                   'Hour': rng.integers(0, 24, 1000)})
print(df)

out = df.groupby(['Hour', 'Weekday'])['Engagement'].mean().unstack()
print(out)
sns.heatmap(out)
plt.show()