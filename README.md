# Docotor Who Collection Management


Web Scraping utility & front end to manage status of epsiodes from the Doctor Who serials.

As a base it leverages this URL: 
http://www.thedoctorwhosite.co.uk/doctorwho/episodes/


This URL is used for the initial building of the database. 

The data structure includes: 

Title nvarchar(75),  --  Name of Story 
Series_Run nvarchar(25),  -- 1963 or 2005 iteration
Season nvarchar(25),  -- Series #
Story_Aired nvarchar(25), -- Sequential Number for original
Season_URL nvarchar(500), -- Link to page.
Episodes nvarchar(25), -- # in Serial/Episodes
Doctor_Incarnation nvarchar(25),  -- Doctor #
Actor nvarchar(75),  -- Actor Playing Doctor
Companions nvarchar(255),  -- Character Names
Monster nvarchar(75),  -- "Dalek" et cettera
Setting nvarchar(75),  -- Where .. ie : "Scaro" 
Synopsis nvarchar(500),  -- Short Description
Collected nvarchar(10),  -- Default = No 
PRIMARY KEY (Title, Series_Run)  -- Control Point 

Upon launch it will build the databse so it may take a couple of minutes depending on your internet connection to build out. 

After the initial launch it will use that initial build to record your collection status based on your use & updates in the interface.  This is a very basic flow w/ limited capabilities. I built as a first test project to learn about web scraping and how to structure code. So any and all feedback is welcome. 

To launch from the command line run the __main__.py in the parent folder. 

Enjoy. 

Thank You 