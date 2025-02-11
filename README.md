#### How we got here: 

I asked my so to share their work schedule with my on Google Calendar. She said, 

> Yeah, I can send you the link to import the calendar when they update release the work schedule for this month.

I asked myself, “why tf...so they send you this link every time they have to update the schedule? How often do they-” 

She sends me the link (`https://sm-cal.apple.com/cal/{hash}`) 

> [!NOTE]
>
> notice how it's using a unique hash? This is fascinating because:
>
> - It's security through obscurity - the URL itself is the authentication
> - It's temporary/disposable - suggesting Apple wants to maintain control
> - It's centralized - everything routes through sm-cal.apple.com
> - It's opaque - you can't derive meaning from the hash

Now, I want to see her work events on my Google Calendar and assign them to a specific color...

oh no, this process is messy; I can’t simply add the events. I have to import, essentially *subscribe* to a public calendar via a URL

![Adding Calendar to Google](./assets/add-calendar-google.png)

> [!CAUTION]
>
> It might take up to 12 hours for changes to your Apple Calendar to show in your Google Calendar. [Learn more](https://support.google.com/calendar/answer/37100?hl=en&ref_topic=1672445) about how Google syncs external calendars.

okay so... this is unacceptable. Unless you want to do what your told and use iCal like the good lil’ blue bubble you are. Pay for iCloud storage, and Apple Care, and Apple Music, etc... Pay it. Pay for all of them. 

![Calendar Integration](./assets/calendar-integration.png)

---

Although Google is nothing to praise, I use Google Calendar for everything.

 

>  [!IMPORTANT]
>
> Google Calendar primarily accepts iCal/iCalendar (.ics) format URLs. 
>
> This isn't random - iCalendar (RFC 5545) became the standard because it was one of the first widely adopted calendar data formats that could handle recurring events, time zones, and other calendar complexities in a standardized way.
>
> There are actually several calendar data formats:
>
> - iCalendar (.ics) - The grandfather of them all
> - CalDAV - A more modern protocol for calendar sync
> - RSS/Atom feeds (with date elements)
> - Various proprietary formats (like Microsoft's old .vcs)

Google Calendar creates separate calendars because:

- Data provenance - maintaining the source of truth
- Conflict avoidance - prevents overwriting existing events
- User control - easier to toggle/delete all events from one source ig
- Trust boundaries - keeping external data segregated and still synced

These systems are built around different assumptions about data ownership and control. Apple's system assumes centralized control (typical Tim Cook Era Apple), while Google's system assumes federation but with clear boundaries.

---

#### Breaking Free

Look, we were sitting here dealing with:

- Monthly "here's your new schedule URL" emails
- That annoying Google Calendar import workflow
- A sidebar full of "Work Schedule (April)", "Work Schedule (May)" calendars
- Tim Cook talking about "it just works" somewhere 

What we ACTUALLY want:

- iCal is just a text format we can parse
- Google Calendar API is solid and well-documented
- Python has libraries for both
- No new calendars, no 12-hour sync BS, no toggles (unless we want toggles)

Here's how we're doing it:
1. Using Python's `icalendar` library to understand Apple's iCal format
2. Google Calendar API for direct event creation, and curation
3. A dash of timezone handling (because time is hard apparently)
4. Error handling for when Apple's URLs inevitably expire

The result? Your work schedule, your calendar, your way. No more calendar segregation, no more toggle dance. (until she switches shifts with someone and I have no way of obtaining that data to push up and sync so we’re stuck in a still-shitty-but-my-kinda-shitty spot🍻)

---

#### God Bless [developers.google.com](https://developers.google.com/calendar/api/quickstart/python)

Follow the instructions for a quick-and-dirty quickstart.py script run

![Project Files Structure](./assets/project-files.webp)

Using the quickstart.py as a template; 

1. Change the `SCOPES` (remove .readonly)
2. Add new function `fetch_and_parse_ical(url)`
3. Replace everything in the `try` with our own instructions
4. spend 53 minutes trying to understand why I kept getting thrown `timezone` errors

> [!TIP]
>
> Here's why all this timezone stuff matters:
>
> 1. The problem:
>
>     - Apple sends times in their local timezone
>     - Google Calendar needs times in a consistent format
>     - Your so might view the calendar in different timezones
>     - Events need to show the correct time regardless of who's viewing them
>
> 2. Why we use `.astimezone(timezone.utc)`
>
>     - Converts any time to UTC (Universal Coordinated Time)
>     - sounds promising out the gate “universal”
>     - Google Calendar handles the conversion back to local time for viewers
>
> 3. The `isinstance` check:
>
>     - iCal can send two types of events:
>
>         - Regular events (with specific times) -> `datetime `objects
>
>         - All-day events (like holidays) -> date objects
>
>     - All-day events don't need timezone conversion (a birthday is a birthday regardless of timezone)

---

###### It worked!

![Working Calendar Integration](./assets/working-integration.png)

 
