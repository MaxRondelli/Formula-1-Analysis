# Formula 1 - Data Analysis
 
## Project Description
The aim of this project is to create scripts to analyse and study Formula 1 telemetry. 

## How to Install and Run the Project
The data used for this project are taken from `fastf1` library. 
If it is your first time with this library, you have to install the library with the following command in the prompt. 
```shell
pip install fastf1
```
Note that Python 3.8 or higher is required. (The live timing client does not support Python 3.10, therefore full functionality is only available with Python 3.8 and 3.9).

After that, to use the API functions, of course, you have to import the library into your project.
```python
import fastf1 as ff1
```

## How to Use the Project
### Caching
Since every weekend produce a huge amount of data, it takes time to load the data itself. The library gives us caching functionality that stores the data from a race weekend in a folder.
You have to create a folder called 'cache' and enable the caching. 
```python
ff1.Cache.enable_cache('cache') # the argument is the name of the folder. Be careful at your folder path. 
```
### Load session data
To load the data from a session, you gotta to specify three parameters:
1. The year
2. The Grand Prix
3. The Session

From the following code, we load the Race of the 2022 Imola Grand Prix.
```python
race = ff1.get_session(2022, 'Imola', 'R')
```
### Documentation
Fastf1 has its [documentation](https://theoehrly.github.io/Fast-F1/), where you can find all its functionality. 
