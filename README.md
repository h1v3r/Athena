# Athena

## How to start up Athena

### Prerequirements
You need to install [**docker**](https://www.docker.com/) as well as [**docker-compose**](https://docs.docker.com/compose/). On an [**Arch Linux**](https://i.redd.it/tcdhu46p4y451.jpg) System this can be done with:

`sudo pacman -S docker docker-compose`

### Clone from GitHub
First you need to download the project from GitHub.

`git clone https://github.com/h1v3r/Athena.git`

After that you cange into the git folder you just downloaded. 

`cd Athena`

### Start the containers
Before you can start everything up, you need to change the the permissions for two scripts. You will need root privileges for that.  

`sudo chmod 645 init_athena.sh rm_athena.sh`

Now you can start the "init_athena" script. You need to do this as root too.

`sudo ./init_athena.sh`

Now everything is starting up. Probably there is a problem with Elasticsearch and permissions. Try 

`sudo chmod 777 ../Athena_Data`

in the git folder. It may solve the problem. 

### Set up NiFi
Next you need to implement the template for NiFi. NiFi will be available at: 

`localhost:8080/nifi/`

It may take a bit till it is up and running. On the NiFi web interface you need to navigate you curse over the grid. Then right click on it and select “Upload template”. A window will pop up where you can select the template you want to upload. Click on the icon with the magnifying glass. If you have done that, a window will open up where you can select the template you want to upload. Simply navigate to your git folder and select “NiFi-Template.xml”. After this you must click “upload” and the template will be uploaded. 

Now navigate to the icon with the name “Template” in the top bar and drag and drop it into the grid. Now you can choose what template you want to use. Select “NiFi-Template” and click “ADD”. The Template should appear on the grid. 

First you need to click somewhere on the grid to dis-select everything. The template consists of many processors (large and rectangular). At every processor you can find a red square which indicates that the processor is turned off. To turn a processor on you right click on it and select start. You need to do this for every processor. 

### Start the API
After you have set up NiFi you can start the API with: 

`python python_SendData_simultan.py`

To accept the default settings of the script click enter.

### Pause the Program
The following steps "Pause the Program", "Remove Athena" and "Portainer" are optional and not needed for the workflow. It provides addidional informations to maximize your docker experience or stop and remove the whole application when you are done.

You can bring all containers down by executing 

`sudo docker-compose down` 

inside the git folder. Use 

`sudo docker-compose up -d`

to bring them up again. However you need to setup NiFi again. 

### Remove Athena
First you want to stop the API. Simply click into the shell where you have started the API and press "Ctrl-C".
Next you simply have to execute the "rm_athena.sh" script. 

`sudo ./rm_athena.sh`

This will delete all data related to the project except the git repo and date in relation with docker. 

### Portainer
The "docker-compose" includes a Portainer container witch can be accessed at:

`localhost:9000`

## Analyse the data with Kibana
Kibana will be available at: 

`localhost:5601`

After you have entered the Kibana web interface you need to click on “Dashboard” at the menu on the left. At “Dashboards” select “Greenhouse_Dashboard”. 

If you are not able to see the dashboard and you get the message that you need to define an index first, than click on "Management" at the menu on the left. Under the header "Kibana" you will find the point "Saved Objects". After clicking that, there should be an option to import a kibana file which is located in your directory at "./zz-Archive/Kibana-save-1.ndjson
Now you should see a few rows added to the list including the index "testindex2" where our data is stored and "Greenhouse_Dashboard" where the Dashboard is located. Either click on it or go the menu point "Dashboards" at the menu on the left and choose the correct Dashboard.

Now you are at the Dashboard. On the top you will find a consol where you can group by “Sensor Name” or select ranges for the parameters. Below that you can find diagrams for the count of measurements per time interval and a pie chart where you can see the shars of each sensor. Under those diagrams you can find four more, each representing one parameter (Air Temperature, Fertilizer, Light and Soil Moisture (in percent)). Echt graph displays the maximum, minimum and median per time interval for the corresponding reading. 

If you get the message "No data available" at the dashboard screen, try changing the time window at the top right of the window to a different intervall (e.g. today).

## Analyse HDFS with Spark (example)
To open the spark shell you need to access the Spark container with: 

`sudo docker exec -it Athena-spark-master-1 /bin/bash`

Then you can open the spark shell.

`./spark/bin/spark-shell`

On the spark shell ypu first need to create a data frame. 

`val sensorDF = spark.read.json("hdfs://namenode:9000/GreenhouseArchiveTest1")`

With this data frame you can create a view: 

`sensorDF.createOrReplaceTempView("sensors")`

You can select from this view with sql statements and print the result.

`val all_data = spark.sql("select * from sensors")`

`all_data.show()`

You can fot example display all data in a certain time interval (in this example all data on "2020-06-14"),

`val max_for_time = spark.sql("select max(air_temperature), max(fertilizer), max(light), max(soil_moisture_percent) from sensors where time_measured like '2020-06-14%'")`

`max_for_time.show()`

or group by sensor.

`val avg_per_sensor = spark.sql("select name, avg(air_temperature), avg(fertilizer), avg(light), avg(soil_moisture_percent) from sensors group by name order by name")`

`avg_per_sensor.show()`

If you want to export the data you collected you can do that by saving the data at the “/spark-data” directory. This directory is mounted at “../Athena_Data/spark-data” at you host machine. 

`val op= avg_per_sensor.rdd.map(_.toString().replace("[","").replace("]", "")).saveAsTextFile("/spark-data/test")`









