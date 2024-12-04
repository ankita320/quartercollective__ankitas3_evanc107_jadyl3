# Quarter Weather by Quarter Collective

## Roster

#### Ankita Saha - Project Manager & API Person

#### Evan Chan - Favorites/User Dashboard Page Developer

#### Jady Lei - Database & CSS Developer

## Project Description

Our website will essentially be a weather news site similar to “The Stuyvesant Spectator,” NYT, and other news publications, but just for weather with more personalized features. Our website will showcase the daily weather of a certain city (typically where they live) which will be taken with their login info. It will then generate articles based on that day’s weather. For instance, if it is a snowy day, there could be articles about indoor hobbies for snowy days. That is the news part of the site. With the NYT or the Stuyvesant Spectator, there are news+ features to them as well that include crossword puzzles, word searches, wordle, and more! That is something we will implement in our website too. We will have a wordle game that will be based on weather or climate-related words.


# Install Guide:
  To install, go to the top of the page and click the green button that says "Code". In the dropdown that appears, click "Download Zip" at the bottom. Extract the zip from your downloads into your home directory. <br>

OR
  
  To clone the repository, go to the top of the page and click the green button that says "Code". In the dropdown that appears, choose either "HTTPS" or "SSH" under the "Clone" section and copy the provided URL. Open up your computer's terminal and type "git clone {URL HERE}"

  
# Launch Codes:
  **Instructions:**
  1. Make a python virtual environment

      a. Open up your device's terminal

      b. Type ```$ python3 -m venv {path name}``` or ```$ py -m venv {path name}```

      c. Type in one of the commands into your terminal for your specific OS to activate the environment

        i. Linux: ```$ . {path name}/bin/activate```
    
        ii. Windows Command Prompt: ```> {path name}\Scripts\activate```

        iii. Windows PowerShell: ```> . .\{path name}\Scripts\activate```

        iv. MacOS: ```$ source {path name}/bin/activate```

      (If successful, the command line should display the name of your virtual environment: ```({path name})$ ```)

      d. When done, type ```$ deactivate``` to deactivate the virtual environment

  3. Ensure your virtual environment is activated

  4. Access the repository by typing ```$ cd quartercollective__ankitas3_evanc107_jadyl3```

  5. Type ```$ pip install -r requirements.txt``` to install the required modules

     a. If terminal returns ```zsh: command not found: pip```, type ```$ pip3 install -r requirements.txt``` because ```$ pip``` is for python2.

  6. Type ```$ python3 app/app.py``` to run the application

  7. Copy / type "http://127.0.0.1:5000" or "http://localhost" onto a browser to view the website
