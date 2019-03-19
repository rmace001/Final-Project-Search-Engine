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
    - Ubuntu Virtual Machine on Virtualbox
  
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
    - Pose queries through RESTful API over HTTP requests (`HEAD`, `GET`, `POST`, etc.)
    
    (d) Limitations
    - Only search within `title` fields per web-document

# Extension : Web Interface Front-end
  - Please refer to our `FrontEnd` repository which can be found here:
      - https://github.com/McCuaslandBrett/FrontEnd
  - Allow User Queries
  - Display Ranked List of .edu Webpage Documents
  -(Add Screenshot of webpage?)
  -(Explain the Web Interface lightly, maybe limitations?)
   
   
# Compiling and Running Instructions
