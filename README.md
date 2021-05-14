# Web-scraping-bot.

Web scraping is a pocess of extracting content and data from the website using automated tools. Web scraping allows to acquire non-tabular or poorly structured data from websites and convert it into a usable, structured format, such as a CSV file or spreadsheet. In this project i am web scraping Github website.

GitHub is a provider of Internet hosting for software development and version control of the projects using Git. It offers the distributed version control and source code management (SCM) functionality of Git. It provides access control and several collaboration features such as bug tracking, feature requests, task management, continuous integration and wikis for every project.

I have writen a python script  to responsible scrape the Github repository for top 25 topics and under each topic, for top 25 repositories. I have sent quries to download top 25 project topics in githubs website using requests module within the github topic's webpage. Used the Beautiful soup module to parse the downloaded html contents into tree like structure for data extraction. The extracted data is converted into tabular format using pandas and downloaded as .csv file.



