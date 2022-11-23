# Nerds of Prey DKP Accounting
Series of scripts to parse Classic Loot Manager JSON exports into the Google raid attendance and loot tracker

#### Assumptions
* you have enabled the google drive api with a service account
* you have shared the google drive folder with your service account
* creds are stored in a config file outside of the repo
* json files contains the first list in the string for either loot or points

#### TODO
* JSON cleaner - currrent JSON copy/paste string can't be easily imported
** find first list for single export selection
** multiple export selections

## Limitations
* JSONs only contain some events, excluding manual adjustments and things that happen outside of an active raid

