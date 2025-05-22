import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow import keras

Data = pd.read_csv(r"TrainingSet\TrainingSet.csv")

#Features (X) output (Y)
X = Data.drop("Perf",axis=1).values
Y = Data["Perf"].values

#Train/Test Split
X_Train,X_Test,Y_Train,Y_Test = train_test_split(X,Y,test_size=0.2,random_state=42)

#Scaling features
scale = keras.layers.Normalization()
scale.adapt(X_Train)

network = keras.Sequential([
    scale,
    keras.layers.Dense(64,activation = 'relu'),
    keras.layers.Dense(64,activation='relu'),
    keras.layers.Dense(1)
])

network.compile(optimizer = 'adam',
                loss = 'mse',
                metrics = ['mae'])

#train
network.fit(X_Train,Y_Train, epochs = 40,batch_size = 32,validation_split = 0.1)

loss,mae=network.evaluate(X_Test,Y_Test)

print(f"Test MAE: {mae:.2f}")

#Save Training objs for later use
network.save(r"Neural Network\TrainedModel.keras")
