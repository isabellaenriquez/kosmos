# KOSMOS — your virtual makeup bag
<img src="https://github.com/isabellaenriquez/kosmos/blob/master/kosmos/static/kosmos/images/kosmos_banner.png">

## Index
- <a href="#tools-and-technologies">Tools and Technologies</a>
- <a href="#pre-requisites">Pre-requisites</a>
- <a href="#mission">Mission</a>
- <a href="#current-features">Current Features</a>
  - <a href="#watch-the-demo">Watch the Demo!</a>
- <a href="#future-features">Future Features</a>

## Tools and Technologies
### Languages
- Python 3.8.2
- JavaScript
- HTML
- CSS/Sass

### Frameworks
- Django

### Other
- Celery (task queue)
- RabbitMQ (message-broker)

## Pre-requisites
To run, please download the files in the requirements.txt file. Recommended browser: Google Chrome.
To run the email and notification functionality, you'll need to run the Celery task queue, and also change the EMAIL_HOST, EMAIL_HOST_USER, and EMAIL_HOST_PASSWORD to the SMTP server, email, and email password of your choice. 

## Mission
<!--img src="https://github.com/isabellaenriquez/kosmos/blob/master/kosmos/static/kosmos/images/logo.png"-->
<p>KOSMOS was designed to rid people of the burden of makeup expiry dates. It allows registered users to add products to their "virtual makeup bags," and input the expiry dates for these products. Upon expiry, the user will be notified via the site and email, reminding users to throw away those icky products and/or replace them. </p>
<p>Beyond the virtual makeup bags, KOSMOS allows users to curate "collections" of makeup products and even publish them for other KOSMOS users to see and "heart." While viewing makeup products from our database of over 900, users can read and write reviews for products. KOSMOS being a third-party website eliminates any bias or paid-for commentary of these products.</p>
<p>Overall, the main goal of KOSMOS is to make the makeup buying and maintaining process simple and transparent. We're here to make making you beautiful beautiful in itself.</p>

<!--
## How KOSMOS is Different From Other CS50W Projects
<p>KOSMOS is NOT an ecommerce website. There is no ordering or buying in place. When adding to makeup bags, it is assumed the user already owns these products. KOSMOS is a way to digitize one's physical collection of makeup products. The makeup bags not only digitize one's physical collection, but also let KOSMOS know which products one would like to be notified about. KOSMOS collections, on the other hand, provide users a way to curate lists of makeup products, perhaps for certain situations. KOSMOS collections are the only way users can directly interact with one another.</p>

<p>KOSMOS uses Python (Django), HTML, CSS/SASS, and JavaScript. JavaScript is used to dynamically create elements and carry out events, such as automatically calculating expiry dates based on the user's chosen opening date, editing collection and makeup bag details, heart functionality, etc. It communicates with the Django-powered server using the Fetch API. KOSMOS' database was imported from the <a href="makeup-api.herokuapp.com">Makeup API</a>, with modifications carried out by management commands I created, and average ratings calculated by user reviews.</p>

<p>I believe my project is sufficiently distinct from past CS50W projects and much more complex. I definitely had the most trouble with the email functionality, as it was difficult to sync the Django server with the Google SMTP server, the Celery task queue, and the RabbitMQ message broker software. I hope this project satisfies whoever is marking this, it's been a pleasure taking the course!</p>
-->

## Current Features
- Free user registration and login
- Responsive design
<br>![gif showing KOSMOS site responsive design](https://github.com/isabellaenriquez/kosmos/blob/master/capstone/kosmos/static/kosmos/responsiveness.gif)
- Database of over 900 makeup products
- Easy product browsing, complete with filters, sorts, and search functionality
- Detailed product pages, including information such as brand, price, reviews and average rating (powered by user-submitted reviews), available colours (including previews for each colour), types, categories, tags, and pictures
- My Makeup Bag: Users can add and remove products to their digital makeup bags. For each products, the user can add notes, an opening date, an expiry date, and enable notifications. If notifications are enabled, users will receive a notification on the site and via email when the respective product is expired.
- User profiles, including profile statistics and their most recently published collections
- User collection curation, allowing users to create collections of makeup with custom details and privacy settings
- Public collections page, where all published collections are available for anyone to view
- Notification via email and the on-site mailbox feature ijmplemented using an asynchronous task queue (Celery) and message broker (RabbitMQ)
<img src="https://github.com/isabellaenriquez/kosmos/blob/master/capstone/kosmos/static/kosmos/images/email.png">
<br>This is the template for the emails sent out to users when an expired product is detected. The actual functionality is carried out by Celery, living in celery.py and tasks.py. Assuming the servers are all up and running, expiry detection takes place at the start of every day (GMT-4). When a product is detected, the database is changed and an email is sent out to the respective user by RabbitMQ via Google SMTP.

### Management Commands
These commands were made to modify my large database, as doing it manually would've taken far too long.
- check_images : Goes through database and checks to see if images are valid. If not, remove the image link.
- import : Imported the database, with each entry as a MakeupProduct, with code to make sure the information fit the formats created in models.py.
- lip_fix : I noticed there was a lack of consistency with some of the lip products in the database (for example, the original database had lipstick as both a product type and category, with lip gloss and liner falling under the lipstick category). I decided to make it so there was an umbrella "lip product" product type, with lip stick, lip liner, lip gloss, and lip stain all falling as categories under it.

### Watch the Demo!
Click <a href="https://www.youtube.com/watch?v=4kyZ7RuZS3k&feature=youtu.be">here.</a>

Check out some screenshots <a href="https://github.com/isabellaenriquez/kosmos/tree/master/capstone/kosmos/static/kosmos/images">here.</a>

## Future Features
- Improved Filters: users can browse makeup by colour groups; filters can be applied to searches
- Improved Search: search not only through products, but for users, collections, etc.
- Custom Makeup Products: enable users to create custom makeup products to make up for those that aren't currently in the database
- Makeup Hacks: users can post makeup "hacks" for other users to read and even heart
- Private Collection Sharing: users can authorize others to view their private collections without making the collection public 
- Currency Conversion: users can browse products in their chosen currency
- Following: users can follow other users; a "Following" feed is created full of the collections of the people the user follows
- Profile Customization: users can set an avatar for themselves, a short biography, connect their other social media, and customize the look of their profiles and makeup bags with themes

## Credits
- <a href="makeup-api.herokuapp.com">Makeup API</a> (where database was originally imported from)
- Brian Yu @ CS50 for helping me learn Django and web development
