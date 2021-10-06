# TestGorilla Scraper

- The script currently has to log in every time it needs some information from the site.
- This is because some HTML elements go stale during page elements loading/unloading.
- I was able to solve this problem late into development, by zooming out to 30% of the browser window. For some reason elements don't go stale this way. It's perhaps because selenium requires al clicked elements to be visible, so giving it the most visual space is the smart choice.
- Needess to say, I have to refactor the code to reflect this new fix. This will probably remove the need to log in every time just to get one student's answers.