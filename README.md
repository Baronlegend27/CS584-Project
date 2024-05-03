# CS 584 Project Credit Card Fraud Detection

Joseph Coco, Tony Zhang

### Comments

We couldnt get it to connect with the cloud so we had to just go with manually creating a local database to use

### Instructions/Steps to run

1. Grab Code
   1. Download Final_Proj folder and extract it
2. SQL setup
   1. Go in pgAdmin and make a new server / database
   2. Inside the database, using the query tool, paste in the sql code from the Database/init.sql file (ignore first 2 lines)
   3. Run that and it should create the necessary tables and schemas
3. Python setup
   1. Have seaborn, psycopg2-binary, and scikit-learn installed ```pip install seaborn psycopg2-binary scikit-learn```
   2. Go into db_config.json and fill in your postgres login info
4. Running Code
   1. Run ```python Start.py```
   2. When prompted with questions on data generation, type desired amount and press enter
      - The amount entered should be a positive value
      - The amount of perchases and payments should be roughly the same or at least very close
      - The amount of accounts should also be less then payments and perchases 
   3. When the terminal's prompter returns, that means that the program has finished running
5. Looking at the results
   1. Find the results in the code folder. After running, there should now be 5 csv files and a png
   2. Look at *modCompare.csv* to check how accurate the predictions are compared to the known labels
   3. Look at *toResult.csv* to see what labels the model has given to the unknown
      - How to understand: Info in the table: output_id, result, avg_cluster
        - output_id is just the id of the transactions
        - result is the given labels: 0 if false (fraud), 1 if true (legit), 2 if left empty (unknown)
        - avg_cluster is the average of the clustering and labeling. ***If this value is greater then 0.5, it is labeled as legit, otherwise fraud***
