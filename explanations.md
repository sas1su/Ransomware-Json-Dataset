
https://github.com/codingo/Ransomware-Json-Dataset/blob/master/ransomware_overview.json
1.	Given this JSON as a sample, how will you write a short script/program to process this json and store into databases
2.	Explain selection of coding language and DB of your choice.
    Language: Python, DB: SQLite3
3.	Given that its large set of data, how will you ensure that no records are missed when writing into the DB
    The code has been wriiten in such a way, it can be rerun as many times. If the record is missing in the next run it will add it. Implementing a logging mechanism and ability to process record from certain part of the input file we can minimize the impact of missing data.
4.	In the case of duplicate entries, how will you handle them?
    There are two approach to this. I have implemented 1)
    1) In the table rans_name, I use uniqueId (primary key) for ransomware name. This constraint is checked to make sure the insertion happens only if the name of the ransomware does not exist in the table. 
    2) Same as time series DBS, using an insertion datetime along with record and let the duplicate to be entered all the time. While fetching it make sure to fetch the latest entries based on datetime. As the record increases make sure to set a retention period and purge the data
   

push it to public git
Screenshot of the data in the DB
Scheema
Explanation of 2, 3, 4 