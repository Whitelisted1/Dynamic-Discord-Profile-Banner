# Discord Profile Image Creator (DPIC)
* DPIC is a web app that allows you to show your discord profile as an SVG for use in a readme, as an example.
* The main benefit is that, with this web app, you no longer have to update an image or link whenever you change your handle, display name, profile picture, etc.

## Example usage
The below SVG of my Discord Profile is from the webserver. It allows you to see my handle, display name, and more without me having to update the information whenever my profile changes

<a href="https://discord.com/users/513501267377782791">
    <img src="https://discordsvgcreator.pythonanywhere.com/getUserProfile/513501267377782791?">
</a>

## How to use
* In order to use this, all you have to do is link to the web URL in your readme, or other source. Follow this template:
    `https://discordsvgcreator.pythonanywhere.com/getUserProfile/<userid>?`
* Please note that the `?` at the end of the URL is necessary, at least from my testing in order to update Github's cache
* Also note that it can take up to a day for the cache to update

## URL parameters
You are able to use the following settings in order to modify your response
* `showBadges`: determines if the returned svg should the profile show the user's badges
* `showBanner`: determines if the returned svg should the profile show the user's banner?
* `showID`: determines if the returned svg should show the user's ID
* `showHandle`: determines if the returned svg should show the user's handle
* Example: `https://discordsvgcreator.pythonanywhere.com/getUserProfile/513501267377782791?showBadges=false&showID=false`
* Please note that all these parameters are assumed to be `true`. You must turn them off with the `false` value

## Badge sources
* Thank you to all the contributers of [Discord SVG Badges by Mattlau04](https://github.com/Mattlau04/Discord-SVG-badges) for making it easy to integrate all the Discord badges for profiles

## How does it work?
* The program works with Discord's developer API which allows us to fetch information about a user from their ID