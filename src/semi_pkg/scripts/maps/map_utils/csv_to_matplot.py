import matplotlib.pyplot as plt
import pandas as pd

def csvTomatplot(name):

    df = pd.read_csv(f'maps/Siheung/maps/straight/{name}.csv', names=None, header=None)
    data_list = df.values.tolist()
    x=[]
    y=[]

    for i in range(1, len(data_list)):
        x.append(df[0][i])
        y.append(df[1][i])
    
    plt.scatter(x,y)
    plt.show()

csvTomatplot("straight_line")
