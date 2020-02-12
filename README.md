# MLApp_CheapFlights
App to find Cheap Flights

## Introduction:

In 2014, the cheapest fare from New York to Vienna was found to be around $800, but according to the advertised fares, where for a select no. of dates, these tickets were between $350 and $450. 

It all seemed to be a good deal and one might wonder if whether it is true or not. The industry does mistake the occasional mistakes on fares, because airlines occasionally and accidentally do happen to post fares that exclude fuel surcharges. Normally, it is expected that the advanced algorithms employed by these airlines would be updating fares that takes into account large number of factors, however due to the order generations of systems in place, mistakes do happen.

## Dataset:

The data was primarily obtained from scraping the HTML available from google flights. 

## Breakdown of this Notebook:

- Sourcing the flight data
- Inspecting and visualising the price and city data
- Finding outliers in the data using the Generalised Extreme Studentised Deviate (GESD) method along with the Q-Q plot.
- Set up IFTTT with SMS and Webhooks services to send alerts via text messages

## Summary:

From this project, I've learnt how to scrape the HTML for flight data by working with DOM to find elements to parse. Utilised the GESD as a technique to handle the univariate time-series data and identifying outliers (which are the airline's mistake pricing on certain tickets). Further, I have also learnt how how setup IFTTT to send text alerts with the code made using the web requests. 

## To run the 'cheapFlight_alerter.py' file:

Open command line and navigate to the folder/directory. then type in "python cheapFlight_alerter.py 'Sydney' 'Europe' '2020-03-01' '2020-03-15' 'Edinburgh'" as an example.

## Libraries and requirements:

The following are the required libraries to run the code.
1. Numpy
2. BeautifulSoup
3. Selenium
4. Requests
5. Scipy
6. PyAstronomy
7. Datetime
8. Time
9. Pandas
10. Matplotlib
11. Pickle

These files will require a Secret Key or API Key from IFTTT to run. Please ensure that the KEY ('IFTTT API KEY') is saved in a folder called 'IFTTT API key', notice the capitalised letters between the key and the folder. The entire folder should be saved in the same directory as the files. 

The API key can be found from IFTTT webpage by following the instructions in the notebook. It can be seen/found as the shown in the diagram below:

![9_Test it](https://github.com/ylee9107/MLApp_CheapFlights/blob/master/IFTTT%20Screenshots/9_Test%20it.png)


## Set up IFTTT service:

IFTTT - If This Then That, is a free service that allows for connection with a huge number of services with a series of triggers and actions. Using this service requires signing up for an account at www.ifttt.com. 

Set-up instructions:
1. Sign up for an account.
2. Next is to sign up for a Marker Channel (ifttt.com/maker_webhooks), this allows for the creation of IFTTT recipes by sending and receiving HTTP requests.
3. Followed by signing up for the SMS channel.
4. After the above, click on the 'My Applets' within the homepage and create a new apple using 'New Applet'.
5. See the Jupyter notebook for the entire service implementation at Section 3.9.

