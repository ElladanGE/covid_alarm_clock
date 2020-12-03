# Covid-19 Alarm Clock


## Introduction

The purpose of this project was to create a dynamic alarm clock which can provide regular updates on covid-19 cases, the news and the weather.
Users can choose to submit alarm clocks will always provide a local covid-19 update with options to include top news stories and/or local weather. These alarm clocks will use vocal announcements. Additionnaly, text based notifications will be updated regularly providing covid-19, news and weather updates.

## Prerequisites
This project was written in Python 3. The user will need a working Python 3 interpreter.
The user will also need git installed.

## Installation

You can dowload the package from Github using:
```sh
$ git clone https://github.com/ElladanGE
$ cd COVID_AlarmClock
```

Create a new virtual environment using:
```sh
python3 -m venv <DIR>
source <DIR>/bin/activate
```
And then activate it using:
```sh
python3 -m venv <DIR>
source <DIR>/bin/activate
```

Additionnal packages required:
  - pyttsx3
  - flask
  - requests
  - json
  - uk-covid19
  - sched
  - time
  - logging

If you do not have these packages pre-installed, you can download them using:
```sh
$ pip install <package name>
```

## Getting started

First you will have to create your config file which must have the name:
```sh
config_file.json
```
Inside this file you must use this structure:
```sh
{
    "API_keys": {
      "news" : "<your news API key here>",
      "weather" : "<your weather API key here>"
    },
    "Location": {
      "my-city" : "<city name>",
      "country" : "gb"
    },
    "News-sources": {
      "my-sources": ["<source1", ..., "<sourceN>"]
    },
    "Notif_period": {
      "time": "<notification update time in seconds>"
    }
}
```
Once you have done this, save it in \COVID_AlarmClock\App.

Voila, the program is now ready to run.
To run the program, in \COVID_AlarmClock> simply type:
```sh
python main.py
```

### Usage
You can now go to:
```sh
http://127.0.0.1:5000/
```
To access the alarm clock.

To set alarm, select a date and time, select if you want to include news and/or weather, add a label and press submit.
The name of your alarm clock, when it is set and it's content should now appear on the left.
On the right hand side, you will see 3 notification boxes. One for COVID update, one for news and one for weather. These notifications will regurlaly be updated depending on what delay you put in the config file. The news stories will be the top news articles from the sources you provided and the weather will be the local weather from the city you provided.



## Testing
To run the test, in \COVID_AlarmClock directory, simply type:
```sh
$ pytest
```
## Developper documentation
### Tree
```sh
* COVID_AlarmClock
    * static
        * Images
            * favincon.jpg
        * style.css
    * templates
        * template.html
    * tests
        * __init__.py
        * gb-news.json
        * test_main.py
    * App
        * __init__.py
        * main.py
        * config_file.json
        * timer_conversion.py
    * license.md
    * README.md
    * setup.py
```


## Details
### Author
- **Duncan Watson**

### Link to source

[Link to Github](https://github.com/ElladanGE)

### Licence

This project is licensed under the MIT Licence - see the [license.md](license.md) for details.

### Acknowledgements
I would like to thank Dr. Matt Collison and all the TA's for their help during the developpement of this project.

