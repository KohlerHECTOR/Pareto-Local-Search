# MADMC Project

## Get MMR per query plot from saved data (results in the report) (2 minutes run time)

```
cd save
python3 plot_data.py
```

Plots are saved as comparison_20objectsPcriteria.png .

## Get new data on a 20 objects knapsack instance for p = 3,4,5 criteria (at least 5 hours run time)

```
python3 get_data_elic_vs_rbls.py
```

Data is saved as .npy archives in /save .

## Generate an approximated pareto front using PLS on knapsack pbm (20 possible objects, 3 criteria) (few seconds run time)

```
python3 study_multi_objs.py
```

Data is saved as .txt in data_multi_objs/ .
Code can be changed to work for p = 3,4,5 criteria.

## Launch a simple RBLS procedure on a 20 objects, 3 criteria instance with OWA agreg (few seconds run time)

```
python3 rlbs.py
```

Code can be change to work on a different instance or with WS agreg.

## Launch a simple incremental elicitaion on a saved approximated Pareto front (on a 20 objects, 3 criteria instance with OWA agreg) (few seconds run time)

```
python3 elicitation.py
```

Code can be change to work on a different instance or with WS agreg.

## Launch a comparison of PLS1 PLS2 PLS3 PLS4 in bi-objs with a 100 objects instance (generate results fron Appendices) (1 hour run time)

```
cd bi_objs
python3 main.py
```

Plot is saved in /bi_objs as comparison_pareto_fronts.png . Execution times are printed in terminal.

## TODO : use an argparser for simplicity
