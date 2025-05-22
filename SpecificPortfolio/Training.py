import numpy as np
import copy
from datetime import date
from TrainingSet import Calculations as Calc
from keras import models
import pandas as pd
import tensorflow as tf

np.set_printoptions(suppress=True)

class Model:
    def __init__(self,Securities:list,MaxSteps:int,Alpha:float):
        #Calculate all features forgiven portfolio
        Calc_OBJ =Calc.Calculate(Securities)
        #Specific Obj Instance
        Calc_Full = copy.deepcopy(Calc_OBJ)
        Calc_Short = copy.deepcopy(Calc_OBJ)

        Today = pd.to_datetime(date.today())
        
        Calc_Full.Specify(Today,Securities,"Full")
        Calc_Short.Specify(Today,Securities,"Short")

        #Features Full - Numerical
        with Calc_Full as calc:
            Er_Full = calc.ExpectedReturns()
            STD_Full = calc.STD()
            Beta_Full = calc.Beta()
            Corr_Full = calc.Correlation()
            TradingVol_Full = calc.TradingVol()

        #Features Short - Numerical
        with Calc_Short as calc:
            Er_Short = calc.ExpectedReturns()
            STD_Short = calc.STD()
            Beta_Short = calc.Beta()
            Corr_Short = calc.Correlation()
            TradingVol_Short = calc.TradingVol()

        self.Features = {
            "Er_F":Er_Full.astype(np.float32),
            "Er_S":Er_Short.astype(np.float32),
            "STD_F":STD_Full.astype(np.float32),
            "STD_S":STD_Short.astype(np.float32),
            "Beta_F":Beta_Full.astype(np.float32),
            "Beta_S":Beta_Short.astype(np.float32),
            "Corr_F":Corr_Full.astype(np.float32),
            "Corr_S":Corr_Short.astype(np.float32),
            "Vol_F":TradingVol_Full.astype(np.float32),
            "Vol_S":TradingVol_Short.astype(np.float32)
            }


        #Starting W Vector
        self.W = np.full(len(Securities),1/len(Securities))

        self.MaxSteps = MaxSteps
        self.Alpha = Alpha
        self.Parts = {}
        self.ScoreHist = []
        self.W_Hist = []

        #Load in saved neural net model
        self.Model = models.load_model(r"Neural Network\TrainedModel.keras")

    def Optimal(self,Weights):

        Weights = tf.cast(Weights,tf.float32)

        #Create adjusted weight vector based on correlation paris (average weight within each pair)
        n=1
        CorrWeights = []
        for s in Weights[:-1]:
            for a in Weights[n:]:
                CorrW = tf.where(tf.minimum(s, a) < 0.01, 0.0, (s + a) / 2.0)
                CorrWeights.append(CorrW)
            n+=1

        CorrWeights = tf.stack(CorrWeights)

        # in the case where portfolio optimizes to 1 security, correlation weights will all be 0. If that is the case just want correlation to be 0 vector so divide by 1
        sum_corr = tf.reduce_sum(CorrWeights)
        corr_divisor = tf.where(tf.equal(sum_corr, 0), tf.constant(1.0), sum_corr) 

        # number of security pairs in corr vector will be (n^2 -n)/2. Which means that total average weight will be greater than 1/ not=1. Need to divide correlation by sum of corrweights vector
        # after calculation

        Feature_V = tf.stack([
            tf.tensordot(self.Features['Er_F'],Weights, axes=1),
            tf.tensordot(self.Features['Er_S'],Weights, axes=1),
            tf.tensordot(self.Features['STD_F'],Weights, axes=1),
            tf.tensordot(self.Features['STD_S'],Weights, axes=1),
            tf.tensordot(self.Features['Beta_F'],Weights, axes=1),
            tf.tensordot(self.Features['Beta_S'],Weights, axes=1),
            tf.tensordot(self.Features['Corr_F'],CorrWeights, axes=1)/corr_divisor,
            tf.tensordot(self.Features['Corr_S'],CorrWeights, axes=1)/corr_divisor,
            tf.tensordot(self.Features['Vol_F'],Weights, axes=1),
            tf.tensordot(self.Features['Vol_S'],Weights, axes=1)
            ])
        
        prediction = self.Model(tf.reshape(Feature_V, (1, -1)), training=False)
        return tf.squeeze(prediction)
    
    def Train(self):
        
        Vector = tf.Variable(self.W, dtype=tf.float32)

        for i in range(self.MaxSteps):

            #Compute gradient function of Optimal()
            with tf.GradientTape() as tape:
                tape.watch(Vector)
                score = self.Optimal(Vector)

            Gr_Vector = tape.gradient(score,Vector)


            if Gr_Vector is None: 
                raise RuntimeError("Gradient eval returned none")

            AdjNeeded = True
            while AdjNeeded:
                #Take average of gradient and subtract it from each value within vector
                G_AVG = tf.reduce_mean(Gr_Vector)
                Gr_Vector-=G_AVG
                Next = Vector+Gr_Vector

                limits = tf.logical_or(Next < 0,Next > 1)

                #only return numbers which are outside of limit (greater than 1 or less than 0)
                diff = tf.where(limits,Next,tf.zeros_like(Next))

                #adjust any differnces over 1 to only give amount in excess to 1 to be redistributed
                diff = tf.where(diff > 1.0,diff-1.0,diff)

                count_realloc = tf.reduce_sum(tf.cast(diff == 0.0,tf.float32))
                realloc_val = tf.reduce_sum(diff)/count_realloc
                adj = tf.where(diff == 0.0, -realloc_val, diff)
                Gr_Vector -= adj

                Final = Vector+Gr_Vector

                cond1 = tf.reduce_any(Final < 0)
                cond2 = tf.reduce_any(Final > 1)
                cond3 = tf.abs(tf.reduce_sum(Final) - 1.0) < 0.1

                if tf.logical_not(tf.logical_or(cond1, cond2)) and cond3: #TODO: Make sure it will not get perpetually stuck in this fixing loop
                    AdjNeeded = False

            #if not on first step, keep momentum from previous step (built to help get of local maxima)
            if i> 0: Gr_Vector = (Gr_Vector * self.Alpha) + (LastGr * (1 - self.Alpha))

            LastGr = tf.identity(Gr_Vector)

            Vector.assign_add(Gr_Vector * ((self.MaxSteps - i) / self.MaxSteps))

            self.W_Hist.append(Vector)
            self.ScoreHist.append(self.Optimal(Vector).numpy())


        return (tf.round(Vector*1e6)/1e6).numpy()
    
