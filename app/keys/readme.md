**Quarter Collective's Quarter Weather Site**


**Ankita Saha, Evan Chan, and Jady Lei**


**SoftDev**

<br>

**API List and Description**


Dictionary API split into two keys,<code>key_merriam_webster.txt</code> for the full collegiate dictionary and <code>key_merriam_webster_e.txt</code> for the elementary version  
OpenWeatherMap API has one key with 1 million calls at <code>key_openweathermap.txt</code>
NYT API has one key that can be used for multiple APIS at <code>key_NYT.txt</code> 

APIS:
- Merriam-Webster API: retrieves a word related to the weather (from API) and uses it to create a Wordle for a NYT/Spec+ style game.
- New York Times API: retrieves articles related to weather for that particular day(topic of articles can be very broad, and key words like “snow” or “rain” will be used to fetch related articles.
- OpenWeatherMap API: Retrieves the weather for a specific city which will be answered by the user. This API affects how the homepage looks as well as travel destinations, forecasts, and activities for that weather.
