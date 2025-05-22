**Project Description**:                                                                                                                                                    Created By: Liam Hayes

The main objective of this project is to optimize portfolio allocation for highest potential performance. The end return will be a allocation vector (W) indicating the projected optimal allocation amoungst securities in the portfolio.

***Structure Overview***:
This project is divided into three sub steps:
1) Data gen and prep
2) Neural Network training
3) Optimizing outcomes for input random portfolio

Each of which can be found in seperate folders in the repository.

***Model Concept***
1) The first part of this model is based on a regression trained neural net aiming to predict portfolio yield from a large dataset of historical portfolios. The data for training the neural net is generated in step 1.
2) Once the neural net is trained, the network is passed through a progressive gradient learning function to optimize predicted yield of a given portfolio. 
![alt text](<TrProg.png>)


