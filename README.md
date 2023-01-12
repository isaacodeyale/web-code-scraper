<b><i>DISCLAIMER : This project is only for educational purposes and should only be used in such manner. </b></i>

<b>| How it works </b>

o Choose an existing directory or create a result folder through the scirpt.

o Choose a file name, a check will occur whether the desired name is taken already

o After the initial questions, the script requests for the original website url which will be used throughout the script in order to retrieve the location of the files in the source.

o The script will ask whether you want to use a cache/downloaded page or allow the script to retrieve the code from the URL entered previously.

o Afterwards it systematically processes through the tags that could potentially have files and downloads them.

o Few changes are made to the page's source code but, after the necessary files are downloaded. The new code is saved as the desired filename and can be used as you please whether for snippets or to alter.

<b>| Techniques </b>

OS

o Checking whether a file or directory exists; creating files and folders to match with site.                             

Tkinter

 o Used for GUI (UI) to select directory that result should be saved instead of relying on text input which user error is most likely to occur.

Requests

 o Library is used to download files onto the chosen directory. 

BeautifulSoup & LXML

 o Provides script functionality of querying through HTML & CSS files; helping with retrieval and altering of specific data.

Regular Expressions
 o Used in the CSS parse function in order to capture the value of the URL attriibute in the different CSS blocks.


<b>| Functions </b>

...
