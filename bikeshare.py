import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    # Get the user to input their name. Characters, hypens and spaces are valid - numbers are not
    valid_characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ -_'
    while True:
        name = input("\nPlease enter your name, using only characters, spaces and hypens: ")
        if all(char in valid_characters for char in name):
            print('\nHello {}! Let\'s explore some US bikeshare data!'.format(name.title()))
            break
        print("\nNumbers are not valid inputs. Please try again.")

    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    # city_input = 'chicago'
    CITIES = ['chicago', 'new york city', 'washington']
    while True:
        city_input = input('\nPlease choose the city you would like to see data for: Chicago, New York City, Washington.\n').lower()
        if city_input in CITIES:
            print('\nThank-you for selecting {}!'.format(city_input.title()))
            break
        else:
            print("\nI'm not sure what city you are referring to. Please try again!")

    # TO DO: get user input for month (all, january, february, ... , june)
    # month_input = 'all'
    MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    while True:
        month_input = input('\nPlease choose from one or ALL of the following months: January, February, March, April, May, June or All. \n').lower()
        if month_input in MONTHS:
            print('\nThank-you for selecting {}!'.format(month_input.title()))
            break
        print("\nI'm not sure what month you are referring to. Please try again!")

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    # day_input = 'Thursday'
    DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    while True:
        day_input = input('\nPlease choose from one or ALL of the following days: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or All. \n').lower()
        if day_input in DAYS:
           print('\nThank-you for selecting {}!'.format(day_input.title()))
           break
        print("\nI'm not sure what day you are referring to. Please try again!")

    print('-'*40)
    return city_input, month_input, day_input


def load_data(city_input, month_input, day_input):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # Read csv for city_input using CITY_DATA dictionary to create df
    df = pd.read_csv(CITY_DATA[city_input])

    # Convert 'Start Time' and 'End Time' columns in df to datetime with pd.to_datetime function
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # Include month number in df using dt.month
    df['Start Month'] = df['Start Time'].dt.month

    # Include weekday in df using dt.weekday_name - note its format, e.g. Monday
    df['Start Day'] = df['Start Time'].dt.weekday_name

    # Include hour in df using dt.hour
    df['Start Hour'] = df['Start Time'].dt.hour

    ## Month
    if month_input != 'all':
        # Create a list of months based on months indices using .index(element)
        MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']
        # Python uses 0 indexing so we need to increase the values by 1 to correspond with month numbers
        month = MONTHS.index(month_input) + 1
        # Filter by month to create the new dataframe
        df = df[df['Start Month'] == month] # where month is the indexed version of the user input

    ## Day
    # Reformat day_input to Friday, for example
    day = day_input.title()

    if day != 'All':
        # Create a list of days
        DAYS = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday', 'Sunday', 'All']
        # Filter by day of week to create the new dataframe
        if day != 'All':
            df = df[df['Start Day'] == day]

    # Replace 'Trip Duration' with calculated version
    # This felt simpler than converting the number of seconds into days, hours, minutes, seconds ;)
    df['Trip Duration'] = df['End Time'] - df['Start Time']

    # print(df.head(20))
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...')
    start_time = time.time()

    ## TO DO: display the most common month
    # Method 1 (commented out below) converts the integer into a character - however, it can only return one value for the mode      # month_mode = df['month'].mode()[0] # The following 2 lines only work if one month is returned, hence [0] included.
    # MONTH_DATA = { 1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June'}
    # month_mode2 = MONTH_DATA[month_mode]
    # Method 2 can return multiple values for the mode. Help please - what is the best way for me to convert this integer into a character? TIA :)
    month_mode = df['Start Month'].value_counts()[df['Start Month'].value_counts() == df['Start Month'].value_counts().max()]
    print('\nThe most common month(s) in integer form (for example, 1=January), with counts:\n', month_mode)

    ## TO DO: display the most common day of week
    # day_mode = df['day'].mode().to_string(index=False)
    day_mode = df['Start Day'].value_counts()[df['Start Day'].value_counts() == df['Start Day'].value_counts().max()]
    print('\nThe most common day(s), with counts:\n', day_mode)

    # TO DO: display the most common start hour
    #hour_mode = df['hour'].mode().to_string(index=False)
    hour_mode = df['Start Hour'].value_counts()[df['Start Hour'].value_counts() == df['Start Hour'].value_counts().max()]
    print('\nThe most common hour(s), with counts:\n', hour_mode)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    start_station_count = df['Start Station'].value_counts()[df['Start Station'].value_counts() == df['Start Station'].value_counts().max()]
    print('\nThe most commonly used start station(s), with counts:\n', start_station_count)

    # TO DO: display most commonly used end station
    end_station_count = df['End Station'].value_counts()[df['End Station'].value_counts() == df['End Station'].value_counts().max()]
    print('\nThe most commonly used end station(s), with counts:\n', end_station_count)

    # TO DO: display most frequent combination of start station and end station trip
    df['Station'] = df['Start Station'] + " --- " + df['End Station']
    popular_station = df['Station'].value_counts()[df['Station'].value_counts() == df['Station'].value_counts().max()]
    print('\nMost popular combination of start --- end station, with counts:\n', popular_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...')
    start_time = time.time()

    # TO DO: display total travel time
    trip_duration_total = df['Trip Duration'].sum()
    print('\nThe total travel time:', trip_duration_total)

    # TO DO: display mean travel time
    trip_duration_mean = df['Trip Duration'].mean()
    print('\nThe mean travel time:', trip_duration_mean)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types_count = df['User Type'].value_counts()
    print('\nCount of user type:\n', user_types_count)

    # TO DO: Display counts of gender.
    # Missing from the Washington dataset. Missing for Customer's in Chicago and NY City datasets.
    try:
        df['Gender Reformatted'] = df['Gender'].fillna('Unknown')
        gender_count = df['Gender Reformatted'].value_counts()
        print('\nCount of gender:\n', gender_count)
    except:
        print('\nGender data is not available for this City. Please try another City.')

    # TO DO: Display earliest, most recent, and most common year of birth
    # Missing from the Washington dataset. Missing for Customer's in Chicago and NY City datasets.
    try:
        birth_year_min = df['Birth Year'].min().astype('int')
        print('\nEarliest birth year:', birth_year_min)
        birth_year_max = df['Birth Year'].max().astype('int')
        print('\nMost recent birth year:', birth_year_max)
        birth_year_mode = df['Birth Year'].mode().astype('int').to_string(index=False)
        print('\nMost common birth year:', birth_year_mode)
    except:
        print('\nBirth Year data is not available for this City. Please try another City.')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city_input, month_input, day_input = get_filters()
        df = load_data(city_input, month_input, day_input)

        # Can you please show me how to validate the input is only no or yes? I can't for the life of me get this to work with the loop. TIA :)
        i = 0
        rows_data = input("\nWould you like to see the first 5 rows of data for the city of {}, the month {} and day {} - type yes or no?\n".format(city_input.title(), month_input.title(),day_input.title())).lower()
        pd.set_option('display.max_columns',999) # Source: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.set_option.html

        while True:
            if  rows_data == 'no':
                break
            else:
                print(df[i:i+5])
                rows_data = input('\nWould you like to see the next 5 rows of data?\n').lower()
                i += 5
                continue

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
