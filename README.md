# myledger
## What is it?
This is a web application which helps a user to maintain his/her transactions in an easy way.
## What it does?
It tracks your expenses and splits payments (by using a normalization scheme) between your friends, and consequently, be able to settle them up.
## Why I made it?
This is my submission for IMG Winter Assignment 2021-22 for Developers. Name of the project is "The Royal _Split_ of Spain".

This is my first web dev project so my main aim in this was to learn and learn, so that in my next project I have less things to learn :) .
## How to use it?
Since I have not hosted it, So you can use/test it in a crude manner by running the code in VS Code or any editor of your choice. Make sure to first install Django.

**Note: Since this is a Django project so it cannot be hosted on GitHub**
## How to run the code?
After downloading the code, go to the same directory as `manage.py` file and in the Terminal type `python manage.py runserver` .

Then  it will show something like this:
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
March 20, 2022 - 10:55:37
Django version 4.0.2, using settings 'imgtry4.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```
Go to `http://127.0.0.1:8000/` and enjoy the website!
## What to do in the website?
The left part of the dashboard shows a list of groups the user belongs to. Next to each group's name there is a number which shows how much money you owe or you are owed by the members of that group (red color indicates that you owe them, grey color means neutral and green color means they owe you)

Right part shows all the transactions of the user. Clicking on a group shows its group panel on the right side. In the group panel, at the top it lists other users in the group and next to their usernames there is a number showing how much you owe them or they owe you (red color indicates that you owe them, grey color means neutral and green color means they owe you)

You can make groups by clicking on the button at the top right corner and then specifying its name.

Members can be added to the group by the _Add Member_ button in the group panel and then type the username of the user to search for him/her.

A transaction can be made by the _Add Transaction_ button in group panel and then specifying its details.
## What next?
Now I hope to host this sometime in future and also add some more CSS features to it when I get to learn more CSS (because I know it looks ugly).

Also I need to learn more about class based views as I have not used them here and I have read many articles saying that they are better than function based views.

Finally, I hope to reduce hardcoded parts in this project because I know it is full of these :( .
