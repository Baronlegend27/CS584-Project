# CS 584 Project Credit Card Fraud Detection

## INSTRUCTIONS

### Prerequisites

Need Docker to access the database on the cloud [JOEY]

Need to pip install seaborn psycopg2-binary scikit-learn if not already 

run: ```pip install seaborn psycopg2-binary scikit-learn```

### Steps

1. Run the docker container
2. Connect to it in the terminal
3. Run ```python Start.py```
4. When prompted with questions on data generation, type desired amount and press enter
   - The amount entered should be a positive value
   - The amount of perchases and payments should be roughly the same or at least very close
   - The amount of accounts should also be less then payments and perchases 
6. When the terminal's prompter returns, that means that the program has finished running
7. Find the results in the code folder. After running, there should now be 5 csv files
8. Look at modCompare.csv to check how accurate the predictions are compared to the known labels
9. Look at toResult.csv to see what labels the model has given to the unknown
