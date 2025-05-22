Project Description:

      ***TO BE UPDATED***

    Created By: Liam Hayes

*Objective*: Given a set of securities, optimize a portfolio based on a set of volatility and expected return features.

__Definitions__

**Importance Weight (In)**:
    _Def: Weight given to different features of optimization model based on how the portfolio is desired to be built.

    Optimal Portfolio Weights:

        I1: % Importance of expected returns [0,1]
        I2: % Importance of standard deviation   [0,1]
        I3: % Importance of Beta                 [0,1]
        I4: % Importance of Security Correlation [0,1]

        Constraint => sum(In)= 1

**Security Weights (Wn)**
    _Def: Proportional weight of security n in portfolio. Algorithm will optimize by vector W = [W1,W2,...,Wn] where the optimal W vector achieves the highest 'optimal portfolio' outcome. The resulting W vector will be used as the optimal portfolio composition based on given inputs. 

**Optimal Portfolio**: 
    _Def: The optimal portfolio will exist generally where it has a minimum volatility and maximum expected returns. This represents the high level direction for optimization.

    Model=>  Max[(Expected Returns * I1) - (Volatility * I2)]
    
**Expected Returns**: 
    _Def: Weighted avg of expected returns of securities in portfolio (by BV)

    Model=>  [R1,R2,...,Rn] * [W1,W2,...,Wn]^T

    Rn:
        _Def: Expected return of security n

                                (Annualized)
        Model=>  [(1 + Daily Avg % Chng in security price)^252] -1 +(average annual dividend yield)

**Volatility**:
    _Def: Measure of overall risk of portfolio. Data analyzed should be prorated the same was that expected returns are (Ex. if expected return ^252 then data should be over last 252 days). This is broken down into three main categories:
        1) Day-to-day stock price volatility - Measured by STD
        2) Potential loss from crisis - Measured by Beta
        3) Management risk (Idiosyncratic Risk) - Measured by security pair correlation

        Model=>  [(%STD * I3) + (|Beta| * I4)] * (|Correlation|*I5)

    Annual % Change STD:
        _Def: Weighted avg of STD of daily percentage change to price in portfolio (by BV)

        Model=> [S1,S2,...,Sn] * [W1,W2,...,Wn]^T

        Sn:
            _Def: STD of daily % returns of security annualized. Using percentage returns as a way to ensure that all weighted returns from holdings have proportional effects on the outcome. Standard deviation is over daily percentage change. Provides analysis on deviation of expected %change rather than deviation away from an average as stock prices generally grow over time. 

            Model=> STD(%change stock closing price)   annualized

    |Beta|:
        _Def: Weighted avg of %Beta in portfolio (by BV)
        
        Model=> [B1,B2,...,Bn] * [W1,W2,...,Wn]^T

        Bn:
            _Def: Absolute value of the security's Beta. The absolute value of Beta is used so that the algorithm does not optimize towards negative Beta (if using + & - values then there would be an apparent benefit to volatility if beta is negative - will subtract from total volatility, which is not true). I also prefer to mitigate risk through general diversification instead of market hedging (which is where a negative Beta could come of use, if that was desirable). Beat is calculated using an even weighted proxy of these indexes ['^GSPC','^DJI','^GSPTSE','^IXIC']. 

             Model=>  |Beta|

    |Correlation|:
        _Def: Weighted avg of security pair correlations 

        Model=> [C12,C13,...,Cni] * [W12,W23,...,Wni]^T

        Cni:
            _Def: Correlation of security pairs n & i.

            Model=> Correlation(Security n_Data , Security i_Data)     
              **not explicity defining correlation - to be inferred**

        Wni:
            _Def: Weight assigned to security pair correlation. Calculated as the avg weight of weights in correlation pair

            Model=>  (Wn + Wi)/2