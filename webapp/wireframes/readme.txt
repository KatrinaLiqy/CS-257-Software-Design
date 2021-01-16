With designing objectives being simple and visual, we build our wireframes with specific emphasis on visualization of datasets by using line charts, histogram, and an informative world map. Please refer to the names of each wireframe pictures for a description of the functionality of the page. Below are the user stories that we try to incorporate into our designs.
Map features
1. Volcanic_eruption_earthquake_tsunami_geological_relation (latitude/ longitude)
Input parameters needed: time (year/month), disaster_type(s)
STORY: As a geologist, I can find the disaster occurrence correlation between earthquake events and volcanic eruption in a specific date to investigate the activity earth crust.
IMPLEMENTATION: When outputting data related to one or more types of disaster worldwide, also output those disaster events information on the same month or year (as the user inputs). We will display a world map with each case pinned at the approximate location (latitude and longitude) in the map, different types of disasters will be represented using different icons.

Statistical features
1. Cumulative_event_count_comparison
Parameters: country, year range, tsunami and/or volcano and/or earthquake cases, 
STORY: As a citizen of a country that tsunamis usually occur, I wonder the number of times such natural disasters happen in history and whether the number of cases increases or decreases how the cases accumulate for the past years.
IMPLEMENTATION: We could add up all the tsunami cases that happen each year in each country and make a line chart for this country with the year in the x-axis and cumulative cases in the y-axis. We could also implement comparison between multiple types of disasters by drawing more than one line in the graph, in which each line of a different color represents a different disaster. We can also inform the user about the countries with most frequently happening tsunamis /other types of disaster. For more extension on this feature, users can use our “Country_cumulative_cases_comparison” feature


We can also direct our users to use the Country_cumulative_cases_comparison feature to look into the comparison regarding one specific disaster across different countries. 

2. Country_cumulative_cases_comparison
STORY: As a geography teacher, I can access the cumulative data of one particular disaster over three related or divergent countries to show comparison between countries.

IMPLEMENTATION: We could let the user choose up to 3 countries and 1 type of disaster for graphical display. We could draw a line chart in which the x-axis is the year, y-axis is the cumulative cases for the specific type of disaster, and that each country is represented in a line of different color.

3. Disaster_in_country_Intensity/magnitude_histogram
For all three disasters within the selected country, we are going to show the intensity/magnitude of the disasters using a histogram with the intensity/magnitude on the x-axis and frequency on the y-axis. 

