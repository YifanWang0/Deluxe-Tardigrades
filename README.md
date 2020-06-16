## Locker Swapper by Deluxe Tardigrades

### Description:
With many students unsatisfied with their assigned lockers, Stuyvesant has had a problem with “illegal” locker trading. Using our website, students will be able to legally trade lockers over one all-encompassing platform. Our platform will require students to fill out basic information of the type of locker they have when registering and some personal info for their profile. After making an account, they can put their locker in the market to trade and look for lockers that they want. Once they find someone willing to swap lockers, the locker info on their profile page will swap and they will get each other’s lockers. Our website also provides a way for people to find locker buddies. The user must complete a survey about themselves and their preference if they want to find a locker buddy with a locker (or put up their own locker as one to share with someone else). The buddy system has a thorough survey format to find the exact person and locker the user needs. To find the locker that the user desires, we have provided an easy-to-use filter system to narrow down the search for the perfect locker. We will notify the other trader/buddy-to-be of your request and once the request for a trade or buddy is accepted or rejected, there will be a notification. We also provided some basic graphs and stats that give an overview of the locker market.

### Team Members:
- Amanda Chen
  - Styling all pages using Bootstrap
  - Sign-in/Login pages and invalid login handling
  - Updating edited information
- Elizabeth Doss
  - Locker market status and keeping track of requests
  - Creating/implementing the locker search/filter system
  - Editing user, locker, and transaction tables
- Amanda Zheng
  - Responsible for facilitating information passage from databases
  - Notification system
  - Creating/implementing Buddy search and filter system
- Yifan Wang (PM)
  - Stats and d3 graph and chart rendering
  - User profile and home page
  - Locker and Profile Survey

### Video Demo Here:

### How to Run
<!-- TODO: add details!!! -->
First clone our repo.
```
git clone https://github.com/YifanWang0/Deluxe-Tardigrades.git
```

Create a virtual environment and run our program in there so that when you exit the virtual environment nothing will be affected on your machine. Note the space in the second line.
```
python3 -m venv locker_venv
. locker_venv/bin/activate
```

Go into the folder you cloned before. This is where all our project materials are.
```
cd Deluxe-Tardigrades/
```

Install the requirements file.
```
pip3 install -r requirements.txt
```

Go into the app folder.
```
cd app/
```

Then run our program.
```
python3 __init__.py
```

When you are finished, terminate the running processes and deactivate the virtual environment.
```
Ctrl + C
deactivate
```
