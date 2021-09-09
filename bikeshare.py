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
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = input('We have Chicago, New york city and Washington, please enter your desired city: \n').strip().lower()
            if city in CITY_DATA:
                break
            print("The city you entered does not exist in the collection")
        except Exception as e:
            print(e)
            
     
    
    # TO DO: get user input for month (all, january, february, ... , june)
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    while True:
        try:
            month = input('\nPlease enter the day of the week to filter data. Choose from any of {}:\n'\
                          .format(', '.join(str(m) for m in months))).strip().lower()
            if month in months:
                break
            print('Please enter a month from {}'.format(', '.join(str(m) for m in months)))
        except ValueError:
            print(e)
    
    month = months.index(month)
    
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    while True:
        try:
            day = input('\nPlease enter the day of the week to filter data. Choose from any of {}:\n'.format(', '.join(str(d) for d in days))).strip().lower()
            if day in days:
                break
            print('Please enter a day from {}'.format(', '.join(str(d) for d in days)))
        except ValueError:
            print(e)
            
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    filename = CITY_DATA[city]
    #load the data for the City
    df = pd.read_csv(filename)
    
    # extract month and day of week from Start Time to create new columns
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name


    # filter by month if applicable (0 - all)
    if month > 0:
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    #calculate the mode for the month to get the most frequent month
    most_common_month = df['month'].mode()[0]
    print('The most frequent month is {} from a total of {} records'.format(most_common_month, len(df.index)))

    # TO DO: display the most common day of week
    most_common_dow = df['day_of_week'].mode()[0]
    print('The most frequent day of the week is {} from a total of {} records'.format(most_common_dow, len(df.index)))

    # TO DO: display the most common start hour
    # extract hour from the Start Time column to create an hour column
    df['hour'] =  df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]
    print('The most frequent hour is {} from a total of {} records'.format(most_common_hour, len(df.index)))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print('The most commonly used start station is {}'.format(df['Start Station'].value_counts().idxmax()))

    # TO DO: display most commonly used end station
    print('The most commonly used end station is {}'.format(df['End Station'].value_counts().idxmax()))

    # TO DO: display most frequent combination of start station and end station trip
    most_frequent_combination = df.groupby(['Start Station', 'End Station']).size().idxmax()
    #print('The frequent start station and end station occured at {}'.format(df[['Start Station', 'End Station']].value_counts().idxmax()))
    print('The frequent start station and end station occured at {}'.format(most_frequent_combination))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print('The Total travel time is: {}'.format(df['Trip Duration'].sum()))

    # TO DO: display mean travel time
    print('The Average travel time is: {}'.format(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    #check if user type column exist in the dataset
    if 'User Type' in df.columns:
        print('\nFind below the summary of user types for this filter: \n')
        user_types = df['User Type'].value_counts() 
        print(user_types)
    else:
        print('\nPlease note that this dataset does not contain user type information\n')


    # TO DO: Display counts of gender
    #check if gender column exist in the dataset
    if 'Gender' in df.columns:
        print('\nFind below the summary of available gender for this filter: \n')
        gender = df['Gender'].value_counts() 
        print(gender)
    else:
        print('\nPlease note that this dataset does not contain gender information\n')

    # TO DO: Display earliest, most recent, and most common year of birth
    #check if birth year column exist in the dataset
    if 'Birth Year' in df.columns:
        #get the min, max and mode and store in their respective variables
        earliest_year, latest_year, most_common_year = df['Birth Year'].min(), df['Birth Year'].max(), df['Birth Year'].mode()[0]
        print('\nThe earliest, most recent, and most common year of birth are as follows {}, {}, {} respectively.'. \
            format(earliest_year, latest_year, most_common_year))
    else:
        print('\nPlease note that this dataset does not contain Birth year information\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    start_loc = 0
    while True:
        if start_loc == 0:
            view_data = input("Would you like to view 5 rows of individual trip data? Enter yes or no? ")
        else:
            view_data = input("Would you like to view 5 more rows of individual trip data? Enter yes or no? ")
        
        if view_data.lower() == 'no' or view_data.lower() == 'n':
            break
            
        print(df.iloc[start_loc:start_loc+5])
        start_loc += 5
        

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        #display the city data
        display_data(df)
            
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
    
   

if __name__ == "__main__":
	main()