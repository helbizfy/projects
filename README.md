# Overview

In my final project for CS50W I developed a carpool app, where people could input departure location and destination and applicable rides then would show up. Each ride shows pick-up date, time, location, car plate number, price, driver’s contact number, and seats taken / available. If there are free seats then the user is able to join the ride.

App allows you to post your rides, check rides where you are the passenger, and the archive of rides you are the driver.

There is also a user profile, where you can see some statistics of completed rides, average review rate, reviews left and reviews themselves.

Website is made mobile friendly by applying media queries and bootstrap.


# Distinctiveness and Complexity

1. In this project I am using Google Places API, so whenever you type a place it gives you options in the dropdown. I used 2 types of this API, namely "gecode" and "address".

2. Also I combined gecoding and Places API to see the exact location on the map, where is pick-up location, however, this is only seen on the admin panel under the Rides module.

3. To complete this project I worked more with pictures since users had the ability to upload user picture and car pictures. Also if the user did not provide a picture, the default picture got assigned.


# Files and functionality

## Layout (layout.html)

This is the base html file, where is navbar, logo, and user information + picture, if logged in. 

## Ride search (index.html)

Here you are presented with "from" and "to" inputs. Inputs are linked to Places API through Javascript (see script.js). These inputs are looking for places based on "geocode". Once inputs are completed, then rides.html is rendered and all the rides show up as per selection. If there are no rides, meaning the date of the ride is in the past, then a warning message will pop up saying that there are no rides for your selection.

Places API is configured through Javascript in a way that only locations in Latvia are showing up.

## Rides (rides.html)

This template renders all the rides based on the request. Rides are filtered by date and status - the date has to be after or at the date of the request and the ride cannot be completed(see views.py -> def rides(request)). If both conditions are fulfilled, the ride will show up and the user will be able to join the ride unless all the seats are taken.

rides.html has "ifchanged" condition so rides are grouped by date and layout is more user friendly.

## My rides (myrides.html)

Once you join the ride, this ride will show up under "My Rides". Here you can see the details of your upcoming ride and also check the pickup location via google maps, since href is set up the way it will show pick-up location on google maps.

Once the ride is completed you are presented with functionality to rate the ride. This function appears only when the driver completes the ride. When clicking on "rate ride" you will be presented with a pop-up, where you can leave the review and star rating. Once completed success message appears.

By clicking on the driver`s picture you are redirected to the user profile page (profile.html)

## Rides posted by me (myroutes.html)

Here you can see the rides where you are the driver and the user has the functionality to delete and complete rides. Once completed, passengers are able to leave a review. Rides are ordered from newest to oldest.

## Profile (profile.html)

Profile page shows user card with picture, name, rides completed, star rating, and reviews left. On the right side are all the reviews and there is a scroll-down functionality when reviews get too many.

## Login / Register / Logout

In the navbar there are login, register, logout functionality for which I used Django authentication functions. Additionally to the register function, the user is able to upload a profile picture, however, if the picture is not uploaded then the default image is assigned to the user.

## New ride (newride.html)

This template allows user to post their rides. The form requires leaving on a date, time, departure, destination, address, car plate number, seats, price, car image(optional). Leaving on date has JavaScript functionality so it does not let input dates in the past.

## Messages (messages.html)

I used Django messages library to show user-friendly success messages after rating the ride.

## Javascript (script.js) / Styles (styles.css)

I used Javascript to implement Places API and control inputs for new ride date input since you should not be able to submit rides.

styles.css contains some styling mostly to make the website mobile responsive. Mostly for design, I used Bootstrap.

# How to run the project

1. Download the distribution code from https://github.com/me50/helbizfy/blob/web50/projects/2020/x/capstone and unzip it.
2. In your terminal, cd into the carpool directory.
3. Run python manage.py makemigrations carpool to make migrations for the carpool app.
4. Run python manage.py migrate to apply migrations to your database.











