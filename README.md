# Experiment Script #
This project is for all the experiments in the graduate school.

Most of the script files will be written in python. There are two reasons why I do so.

  - I'm not very fimiliar with matlab, so I choose use other programming language to do the pre-process the raw data and then use matlab to do other statistical works. Also some scripts can link different matlab step together.
  - Many people says `A coder should learn a script language`, so, here I choose python to be my first script languange. At the same time of doing my experiment, I can become more familiar with python.

## Friends and Family ##
The file(s) in the `/friends_and_family` folder is the experiment script(s) based on the [MIT Friends and Family dataset](http://realitycommons.media.mit.edu/friendsdataset.html).

The script `data-preprocess.py` converts call logs, sms logs and proximity records between dyads from csv files into one observation matrix and stores into one csv file which canbe used to do data analysis in the matlab. The proximity records in the matrix are counted by five different types, including `bed`, `work-day`, `work-day`, `work-night`, `weekend-day`, `weekend-night`.

Unfortunately, the dataset is not meet my demands very much, so there is only one script file in the directory.

## Social Evolution ##
The file(s) in the `/social_evolution` folder is the experiment script(s) based on the [MIT Social Evolution dataset](http://realitycommons.media.mit.edu/socialevolution.html).

Before use the scripts in the folder to pre-process the files of the dataset, some other operations have been done, such as remove every records which has unknown target user in these files.

The script `data-preprocess.py` converts call logs, sms logs, proximity records and campus organization records between dyads from csv files into one observation matrix and stores into one csv file which can be used to do data analysis in the matlab. The proximity records in the matrix are counted by three different types, including `work-day`, `work-night`, `weekend`. The campus organization records are the total organization amount that the dyads attend together.

Then matlab can use the outputed matrix to do the Factor Analysis or Principal Component Analysis and store the result score in to a csv file. After that, the script `score-relation-merge.py` can merge the dyads score and relationship from survey together. The script can count the amount of `Close Friends`, `Asymm Close Friends` and `None Close Friends` dyads in different region of score, for example every deciles of the total score range. Finally, the script can produce a file of the counting result and the matlab can use the result file to draw a bar graph of the relationship distribution.

The `proximity-process.py` is similiar to `data-preprocess.py`. But it do not consider sms logs, call logs and activity records. It only counts proximity times by 48 types, including work-day 0 o'clock to 23 o'clock and weekend 0 o'clock to 23 o'clock. Also the result was stored in a csv file, can be analyzed by matlab, can use `score-relation-merge.py` to merge dyads and scores and can draw a bar graph to show the distribution.

The `week-prox-proc.py` counts proximity times in 24 * 7 hours of different relationship types. The result is a 3 * 168 matrix.

The `wlan-precluster.py` analyze the access records in the 24 * 7 hours of every wifi access points. The result is for the analysis of wifi-ap cluster and know the clusters' meaning.

The `wlan-postcluster.py` try to merge the wlan-ap cluster type to the proximity records. So, we can know where a proximity happened. The final result can add information to the proximity records and can help prove the result of classification.