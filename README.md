# Athena

## How to start up Athena

First you need to download the project from GitHub

`git clone https://github.com/h1v3r/Athena.git`

After that you cange into the git folder you just downloaded. 

`cd Athena`

Before you can start everything up, you need to change the the permissions for two scripts. You will need root privileges for that.  

`sudo chmod 645 init_athena.sh rm_athena.sh`

Now you can start the "init_athena" script. You need to do this as root too.

`sudo ./init_athena.sh`

Now everything is starting up. 


Next you need to implement the template for NiFi. NiFi will be available at: 

`localhost:8080/nifi/`

It may take a bit till it is up and running. On the NiFi web interface you need to navigate you curse over the grid. Then right click on it and select “Upload template”. A window will pop up where you can select the template you want to upload. Click on the icon with the magnifying glass. If you have done that, a window will open up where you can select the template you want to upload. Simply navigate to your git folder and select “NiFi-Template”. After this you must click “upload” and the template will be uploaded. 

Now navigate to the icon with the name “Template” and drag and drop it into the grid. Now you can choose what template you want to use. Select “NiFi-Template” and click “ADD”. The Template should appear on the grid. 

First you need to click somewhere on the grid to dis-select everything. The template consists of many processors (large and rectangular). At every processor you can find a red square which indicates that the processor is turned off. To turn a processor on you right click on it and select start. You need to do this for every processor. 


After you have set up NiFi you can start the API with: 

`python python_SendData_simultan.py`

To accept the default settings of the script click enter. 







