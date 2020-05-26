<h2><b>COVID19-STATS<b><h2>

To run this application you will need
<ol>
  <li>Docker</li>
  <li>Postman</li>
</ol>


#STEPS

1) In your terminal type 
       -> docker run 5000:5000 --name="your_container_name" abihaa/covid19-stats

2) Open Postman and make any of the following requests

3) They are different GET API's to save data of this request in our database
   
   -> For Global data send request to "localhost:5000/results"                      
   
   -> For Regional data send request to 'localhost:5000/regions"
   
   -> For data according to Map send request to 'localhost:5000/maps"
   
4) Now, to retrieve data 

   -> Globally send request to "localhost:5000/resultsoutput"
   
   -> Region wise send request to "localhost:5000/regionOutput"
   
    -> Acoording to map send request to "localhost:5000/mapOutput"
    
