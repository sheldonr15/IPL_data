# Data Analysis on IPL dataset
EDA, data cleaning, data analysis, data visualization of the IPL dataset.
Also, creating a dashboard using Streamlit app and deploying the app on Heroku.

The dataset has been taken from [Kaggle - matches.csv.](https://www.kaggle.com/manasgarg/ipl#matches.csv)

The Streamlit Dashboard deployed can be found on this [LINK.]( https://vast-garden-60234.herokuapp.com/)
-----------------------------
Use the checkboxes to view its respective sections.



<br/>

## Getting Started
These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites:
- [Jupyter](https://test-jupyter.readthedocs.io/en/latest/install.html) for Jupyter Notebooks.

- The other prerequisites are mentioned in `requirements.txt`. To install all packages from it run :
```
pip install -r requirements.txt
```

- For instructions on using Google Sheets as a source for your dataset using the Sheets API refer to this [video](https://www.youtube.com/watch?v=cnPlKLEGR7E).
Include your `creds.json` file in the main project directory alongside `sheets.py`.

### Setup:
- #### Streamlit
Running the Streamlit app on your local machine:

Go to the project directory and run :
```
streamlit run run.py
```  

- #### Heroku Deployment
For Deploying the Streamlit Dashboard on your Heroku Account :
Follow these [instructions](https://gilberttanner.com/blog/deploying-your-streamlit-dashboard-with-heroku) 

`Procfile` and `setup.sh` is already present in the repo. 

**Note** : Edit your email-id in the `setup.sh` file.

<br/>
<br/>

## Breakdown 
**src/  :**
- app.py : Contains the main bulk of the code. Includes code for data analysis and Streamlit
- preprocess.py : Contains the code for data cleaning.

**notebooks/ :** Jupyter Notebooks 

**procGen.py :** Run before the Heroku Deployment to generate Procfile

**run.py :** To run the Streamlit app

**sheets.py :** For Google Sheets connection
