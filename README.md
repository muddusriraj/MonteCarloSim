Simple Monte Carlo Simulation

- Utilized a lognormal distribution to generate values for price prediction
        - For this simulation, 10,000 samples were generated for each simulation, ran a total of 10,000 times for each ticker
- Retrieved the past year of data for each inputted ticker using the yfinance module
- Utilized multiprocessing in order to run simulations in parallel
        - Kept track of simulations already processed using trackedTickers.csv
        - Stored mean price output values in tickerOutput.csv