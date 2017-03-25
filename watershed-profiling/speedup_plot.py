import pandas as pd
import matplotlib.pyplot as plt
data = pd.read_csv('speedup.csv')

#print data

ax = data.plot(y=['8GB','16GB','32GB'],
				x='CUs', 
                title='Speed-up on Comet', 
                #legend=None,
                #xlim=(0,16),
                #xticks = [0,1,2,3,4,5,6,7,8,16],
                #ylim=(0,12),
                marker=',',
                )

ax.set_xlabel("Number of Cores")
ax.set_ylabel("Execution Time (s)")

ax.grid()
#plt.show()
plt.savefig('speed-up.jpg')