# Finalproject-LightSABR
finalproject-lightsabr created by GitHub Classroom

# Team Members
- Shiyao Feng 
- Alexander Yee
- Brett McCausland
- Rogelio Macedo 

# Search Engine

- Web Crawler

    (a) Architecture.
    
    - Multi-threaded design
    
    - Duplicate detection
        
    (b) The Crawling or data collection strategy
    
    - Using multiple threading to get the URL from seed web, and extract links from it to other docs (URLs) without duplicates by        concurrent.futures and regular expression.
    
    - Using multiple threading to download each HTML file to a local folder by 16 multi-task.
    
    - In the data folder, the application creates a different level folder to keep the files.
    
    - The application allows user input the number of pages to crawl and number of levels to limit application.
    
    - The default setting of application: if the application gets the file over 1GB in some arbitrary level K, the application will stop when it finished web crawling in level K.
    
    - If the user wants to input the limit by page or level, the memory wouldn’t be limit by 1 GB
    
    - When web crawling reaches the max level, the application will stop until the job is at max level.

        
    (c) Data Structures employed.
    
    - Python lists
    - Dictionaries
    - Queues
    - Time
    - Hurry filesize(file size)
    - re(regular expression)
    - The BeautifulSoup library
    - The urllib.request module
    
    (d) Limitations
    - the multi-process of python is hard to control the shared variable-page_number, so the application will stop at Max ~ Max + 15. The reason why the application will stop at Max +15 is that I set 16 task to run the process.  
        
- Structure HTML Data
    - Parse `.html` and convert to `.json` format

- Indexer
    
    (a) Architecture
    - Ubuntu Virtual Machine on Virtualbox serving as Elasticsearch cluster
  
    (b) Index Structures
    - JSON Mapping Structure of a Web-document
        - {
           - id: number,
           - title: string,
           - url: string,
           - level: string,
           - filename: string,
           - body: string
           - }

    (c) Search Algorithm
    - Pose queries through RESTful API over HTTP requests (HEAD, GET, POST, etc.)
    - Retrieve results based on multi-match of web-document fields: title, body

    (d) Limitations
    - Due to virtual cluster, only the host machine of the cluster may successfully make HTTP requests and thus run the application

# Extension : Web Interface Front-end
  - Please refer to our `FrontEnd` repository which can be found here:
      - https://github.com/McCuaslandBrett/FrontEnd
  - Frameworks used: 
    - Express and Node.js
    - Ping the cluster when executing the application
    - Allow user queries through a search bar and submit button
    - Display ranked list of .edu web page documents
  - Limitations
    - We wish to modify the Embedded JavaScript file (.ejs) to search for the matched words in a query and only highlight those
    - The only way to access the virtual cluster is directly through the host running the virtual machine
   
# Compiling and Running Instructions
- Web Crawler
    - When running the python web crawler (`multi-threading.py`), the text interface walks you through a number of crawling options
    - See web crawler section under "The Crawling or data collection strategy" for the various options of web crawling
- Converting to `json` Format
    - running `html_to_json.py` takes the `data/` folder and outputs `data.txt`
- Setting Up the Virtual Cluster
    - Use VirtualBox (or whatever other virtual machine/local machine used to host the Elasticsearch server)
    - Assuming that the virtual machine is already set up with Elasticsearch, this is step where the user logs into their virtual machine
    - Save `data.txt`as `.json` extension, and bulk-load `data.json` with a `PUT/POST` request
- Front End
    - To connect to the cluster, the user would have to modify the host's login information in `FrontEnd/app.js` to match their own login information
    - When connected to the Elasticsearch cluster, running the node application `FrontEnd/app.js` which will initially ping the cluster to make sure the server is online
    - At this point, you may now launch the website (`localhost:3000`) and begin searching 
