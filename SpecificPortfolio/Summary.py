import matplotlib.pyplot as plt
import pandas as pd
import autograd.numpy as np

def Report(a,W):
    #Score
    Score = {"Metric": "Market Return", "Value":a.Optimal(W).numpy()}

    # Weights
    weights = {"Metric": "Weights", "Value": list(W)} 

    # Combine all into a DataFrame
    df = pd.DataFrame([Score,weights])

    # Display the table
    print(df.to_string(index=False))

def Graph(a):
    Data = a.ScoreHist
    # Plot the data
    plt.plot(Data, marker='o', linestyle='-', color='b',markersize=3)

    # Labels and title
    plt.xlabel("Step")
    plt.ylabel("Overall Score")
    plt.title("Score progression per step")

    # Show the graph
    plt.show()
