## Udactiy 4th project Item project catalog
This is a project required to graduate from Udacity with a nano degree.


###Brief description of the project
 The Item catalog application, allows the user to create catagories and list for those categories with
 a brief description. When the user logs in using google oauth(google account). The application allows
 the user to do crud operations. Cread Read Up Delete

 - Allows for user to use JSON endpoints
 - Allows for user to only add to the sqlite database if they are authenicated.



##Getting the project up and running

1. In order to use this project you will need to download vagrant[Vagrant](https://www.vagrantup.com/downloads.html).

2. Download and install Virtual Box(note project will not work with out the virtual box vm, as it uses a linux shell)
    [VirtualBox](https://www.virtualbox.org/) - download the version 5.2 under older version on the virtualbox site

3. Using the terminal of choice type in 
```bash git clone https://github.com/udacity/fullstack-nanodegree-vm``` to download the
Vagrant config files.
        -Once clone open the folder and go to the subfolder > vagrant
        -with the termial of choice cd into the vagrant sub folder and type
           ```bash
             vagrant up
           ```
the above allows for vagrant to grab the premade vagrant file and install the linux distro and all the packeges needed
for the project to run.

##NOTE:
  ####this process does take some time please refer to the repo [here](https://github.com/udacity/fullstack-nanodegree-vm)

4.After the vagrant vm is created using the following commands
```bash
vagrant up
````
doing this process will, take you the the linux VM(Vagrant), cd into the vagrant folder.
Navigate to the catalog project  and upgrade flask.
  ```bash
    sudo python -m pip install --upgrade flask
    ```
    
    Once upgraded and your cdinto the catalog folder type
         ```bash
    python  database_setup.py
    ```
    
    
 this will create you sqlite data base , when completed  run the following command

```bash
python app.py
```
 #####this will run the application on http://0.0.0.0:8000, in order for Google oAuth to work use 'http://localhost:8000/'

