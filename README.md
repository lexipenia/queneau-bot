# queneau-bot

This bot tweets out potential sonnets from Raymond Queneau’s *Cent mille milliards de poèmes*.

Since the sonnets are longer than 280 characters, it renders them first as an image.

Follow the bot here:
https://twitter.com/100000milliards

Buy the original book:
https://www.gallimard.fr/Catalogue/GALLIMARD/Hors-serie-Beaux-Livres/Cent-mille-milliards-de-poemes

## Dependencies
```
pip install pillow tweepy
```
The bot also relies on Twitter API keys from a `config.py` file and an array containing the lines of *Cent mille milliards de poèmes* in `lines.py`, which are not included here.
