================================================================================
Contents:
================================================================================
ProjectReport.pdf - project report
src - source code repo
	preprocessing - code to preprocess
		ML Project Flatten Train.ipynb - code to flatten train dataset
		ML Project Preprocess Train.ipynb - code to preprocess train dataset
		ML Project Flatten Test.ipynb - code to flatten test dataset
		ML Project Preprocess Test.ipynb - code to preprocess test dataset
	training - code to train different models
================================================================================		

================================================================================
Prerequisites:
================================================================================
	Python3
	Jupyter notebook
================================================================================

================================================================================
Required libraries in Python
================================================================================
	sklearn 
	pandas 
	numpy 
	urllib
	matplotlib
	datetime
	lightgbm
	xgboost
=================================================================================

=================================================================================
Instructions to run:
=================================================================================
	Download train_v2.csv and test_v2.csv from https://www.kaggle.com/c/ga-customer-revenue-prediction/data
	Open jupyter notebook in the same folder where you saved these files
	Preprocessing:
		train_v2.csv:
			Open "ML Project Flatten Train.ipynb" in jupyter notebook
			Run the notebook
			It will flatten "train_v2.csv" and give you 16 files "flatten_train_{partition_number}.csv"
			Open "ML Project Preprocess Train.ipynb" in jupyter notebook
			Run the notebook
			It will give you a single preprocessed file "finalEncodedData.csv". Use this for training.
			
		test_v2.csv:
			Open "ML Project Flatten Test.ipynb" in jupyter notebook
			Run the notebook
			It will flatten "test_v2.csv" and give you 16 files "flatten_test_{partition_number}.csv"
			Open "ML Project Preprocess Test.ipynb" in jupyter notebook
			Run the notebook
			It will give you a single preprocessed file "finalEncodedTestData.csv". Use this for testing.
	Training:
		Open "ML_Train.ipynb" in jupyer notebook
		Xgboost and LightGBM libraries should be installed
		Run the notebook with "finalEncodedData.csv" and "finalEncodedTestData.csv" in the same directory.
		It will log evaluation metrics to the console using GradientBoosting Regressor.
		To run with different algorithms and its configurations, uncomment and comment relevant parts.
		PCA computation is commented as it gives worst results. 
		For faster training, 10% training sampling can be used. 
		