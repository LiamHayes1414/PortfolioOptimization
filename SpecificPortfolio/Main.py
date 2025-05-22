#Portfolio Optimization
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'  # or '3' to suppress even more


from Training import Model
import Summary


#See README file for project description

#_____________________MODEL INPUTS________________________
#>List of Securities
Securities = ['ZWC.TO','BNS.TO','ENCC.TO','FLT.V']

#Max Steps
MaxSteps = 30         #<- Number of vector steps the model will go through until end of optimization

#Alpha
Alpha = 0.7         #<- Weight given to new gradient when doing momentum weighted avg on each new step    (New Gradient*Alpha + Previous Gradient*(1-Alpha))

#_________________________________________________________


a = Model(Securities,MaxSteps,Alpha)

W = a.Train()

#Results
Summary.Report(a,W)
Summary.Graph(a)





