from datetime import datetime, timedelta
import time
import traceback


"""
convert_game_time converts from 24 hour est clock to 12 hour pst clock for games
:gameTime: time in 24 hour est format
"""
def convert_game_time(gameTime):
    pst_time_diff_from_est = 3
    if not gameTime:
        return "TBA"

    try:
        #Time formatted in 24 hour format in EST timezone as naive time object
        time_object = datetime.strptime(gameTime, "%H:%M:%S")

        #Change gametime to PST timezone (3 hour difference between EST and PST)
        #Unfortunately scorestrip.json time is not in a standardized UTC format
        #so can't make time_object timezone aware and use libraries for
        #converting between different timezones
        #Making major assumption that scorestrip time
        #is in DST time (if applicable), otherwise time would be off an hour
        t = timedelta(hours=pst_time_diff_from_est)

        time_object = time_object - t
        #Create timezone string (12hour time, with AM/PM at end) EX: 5:15PM
        gameTime = time_object.strftime("%I:%M%p")

    except Exception:
        print ("Can't convert game time")
        print(traceback.format_exc())
        gameTime = "TBA"
    return gameTime
