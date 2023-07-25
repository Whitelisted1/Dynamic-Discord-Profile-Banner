# Discord User SVG Creator
* Discord SVG Creator is a web app that allows you to show your discord profile as an SVG for use in a readme, as an example.
* The main benefit is that, with this web app, you no longer have to update an image whenever you change your handle, display name, profile picture, etc.

## Example usage
The below SVG is from the webserver, which allows you to see my handle, display name, etc.

<a href="https://discord.com/invite/TPFR8T5JG4" target="_blank">
    <img src="https://discordsvgcreator.pythonanywhere.com/getUserProfile/513501267377782791">
</a>

## How to use
* In order to use this, all you have to do is link to the web URL in your readme, or other source. Follow this template:
    `https://discordsvgcreator.pythonanywhere.com/getUserProfile/<userid>`

## How does it work?
* The program works with Discord's developer API which allows us to fetch information about a user from their ID.