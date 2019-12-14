As explained in our documentation file, our platform allows advertisers to upload their advertisements and select
service providers will then be able to run these ads to display these ads their clients and earn a commission.
Although we were not able to enable all the features we had in mind, the foundation of our project (the ability
for advertisers to upload video's and for service providers to run them) functions. This naturally implies that
there are two user interfaces, one for the service providers and one for the advertisers.

When registering, users input a username/company name, password, and if they are an advertiser, select the
checkbox which indicates whether or not the user is an advertising company. This information is then stored in
an SQL database called Accounts with the columns: id (int), username (text), hash (text), and advertiser
(boolean). Using form.get we determine whether or not the user is an advertiser and use session to pass this
information to our layout html which determines what pages the user has access to. A user will have access to an
Account tab (user_account.html), a Run Ads tab (runads.html), the Homepage, and Logout. An advertiser will have
access to an Account tab (advertiser_account.html), an Upload tab (upload.html), the Homepage, and Logout. This
is the same for login. When not logged in users will have access to the homepage, team page, register page, and
login page.

For advertisers, the upload tab displays a form that allows the submission of a youtube embed url. The
url must be a youtube embed link as in our runads.html, we utilize an iframe carousel that requires the source
to be of the form https://www.youtube.com/embed/example. We would have liked to make our application parse
through the inputted url and put it into the proper format. However, we did not have enough time to make this.
Upon uploading a properly formatted url, the url is stored in an SQL table titled videos.

For users/service providers, the runads tab displays an iframe carousel with ten randomly chosen videos from
the SQL table videos. This was the most difficult to get to work properly. We first pulled all the urls from
the videos table and put the 'link' values into a list such that we had a list of youtube urls. We then select
a random sample of 10 to create a new list with. Unfortunately, as I mention in the source code, there was an
issue running json.dumps on the entire list that made it so we could not access any of the list entries. To work
around this we run json.dumps on each list entry and pass them to runads.html. In the runads.html we have a set
of ten carousel slides with iframes. In order to dynamically update the source of each iframe we utilized
javascript code and the urls we passed to the html. The carousel will rotate through each video allowing viewers
to choose one they want to view. If a viewer chooses to watch a video, the carousel pauses for the duration of
the video and automatically resumes once it is finished.

Both Account pages for the advertisers and users/service providers are simply html pages that we wanted to
display important information relevant to the account. However, we did not have time to make it dynamic.


