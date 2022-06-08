import pandas as pd
import numpy as np
import plotly.express as px


if __name__ == '__main__':
    df = pd.read_table("annotated_words.csv", delimiter=",")
    words =set(df["word"].tolist())
    df =  pd.DataFrame(df["shift_index"].tolist(), 
                    index =df["word"].tolist(),
                    columns=["shift_index"])

    df["cos_sim"] = np.ones(97)
    cos_dist = {}
    with open("results/changesCorrectAlpha.txt", 'r', errors='ignore') as f:
        for line in f.readlines():
            tokens = line.strip().split()
            if(tokens[0] in words):
               df.at[tokens[0], "cos_sim"] = tokens[1]
    print(df)
    fig = px.scatter(df, x="cos_sim", y="shift_index", color=df.index,  trendline="ols")
    fig.show()
    f.close()
    
    #print(cos_dist)