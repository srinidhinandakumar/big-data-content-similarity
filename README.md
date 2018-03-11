# Clustering a Big Dataset using Tika-Similarity

This project uses a UFO sightings dataset.

Four more datasets (air pollution, drug poisoning, us cities, ufo dataset with latitude and longitude, cancer incedences) are used and a comprehensive dataset is formed.

The final dataset has the following columns:-

  * Description
  * Location
  * Sighted At (time)
  * Reported At (time)
  * Shape
  * Duration
  * Cancer incidences count in all races
  * Cancer incidences count in all white people
  * Cancer incidences count in all hispanics
  * SO2 Mean
  * CO Mean
  * O3 Mean
  * County
  * Population per county
  * Age adjusted death rate (due to drug poisoning)
  * Latitude
  * Longitude
  * Airport name (closest airport)
  * Airport distance (distance between current location and closest airport)

  ### File Structure
  ---
  - datasets
  	
    - original_datasets : contains original dataset copies for all datasets used
   
    - intermediate_datasets: contains any intermediate datasets used by us to reach final merged dataset

    - modified_datasets: final dataset

  - code: code files including python scripts and tika-similarity modified files

  - documents: readme and doc file with answers to questions

  - results: contains images and screenshots, graphs and maps to show inferences and conclusions from the analysis on the final dataset
  
  ### Scripts to run different files:-

- Files that contribute to data generation and merging of datasets are:-

  - aiprots_pollution_feature.py
  - Helper.py
  - Integrate_cancer.py 
  - integrate_drug.py
  - ufo_add_lat_long.py
  - ufo_airport_pollution_merge.py

- Files that contribute to visualization:-

  - visualization_air_quality.py
  - visualization_cancer.py
  - visualization_demographics.py
  - visualization_ufo.py

*Due to large size of dataset and high computation requirement, we divided the initial dataset into 8 parts and creates an instance on Azure cloud. We ran the location based merge of datasets on this instance to achieve max efficiency and relatively quick results*

- The command to run integrate_cancer.py

  `python integrate_cancer.py /path/to/cancer_dataset /path/to/ufo_dataset year outputfile`

- The command to run integrate_drug.py

  `python integrate_drug.py drug_dataset /path/to/uscities_dataset path/to/ufo_dataset start_year end_year outputfile`

 - The command to run visualiztion_cancer.py 

   `python visualization_cancer.py /path/to/cancer_dataset`

 - The command to run visualization_drug.py

   `python visualization_drug.py /path/to/merged_dataset year`

 - The command to run visualization_ufo.py
   
   `python visualization_ufo.py /path/to/merged_dataset year`

 - The command to run visualization_demographics.py
   
   `python visualization_demographics.py path/to/merged_dataset year`

 - Tika-Similarity changes:
 	
  **Jaccard changes** - Existing infrastructure ran the algorithm on the metadata, that too on the "key" and not on the "value". 

Now, one more functionality has been included which compares all the features of a single dataset using jaccard algorithm. 

Basically every entry has a "key" and "value" pair and the jaccard similarity algorithm is applied to the "value" as it makes more sense. 

Corresponding changes were made in circle_packing.py and cluster_scores.py so that correct the json object is passed on to circlepacking.html and cluster-D3.html

We have tried this algorithm only on a subset of our final dataset with 100 entries for better clarity and understanding. 

Ideal threshold :- 0.0001 t 0.0003

- running feature_jaccard.py
  `python feature_jaccard.py -f <filename>`

- running cluster_scores.py (ideal threshold value would be 0.0001 to 0.0004 if it is run on reduced_100.json dataset)
  `python cluster-scores.py [-t threshold_value]`

> For now, we have implemented this as a separate file, but later on we're planning to merge with the existing code and send a pull request to tika-similarity repository

