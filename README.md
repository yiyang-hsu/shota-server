# Gallery

The tiny backend of [boys-love.club](https://boys-love.club).

## Supports

1. Display a (set of) random pictures.
2. Display the latest pictures.
3. Store the uploaded pictures and their meta info.
4. Download the pictures stored from telegram bot API. The file ids are required to be already stored in the Leancloud storage. Or else you need to manually edit the `utils.py` accordingly.

## Notice

1. The whole server is supposed to be served at the subdir `$ROOT_URL\shota\` (e.g., [/shota/random](https://boys-love.club/shota/random/), be careful it's NSFW). Some strings are hardcoded in the source code, you need to change them manually.
2. The image server is not included. You need to implement it (by a reverse proxy or just a static folder) at `$ROOT_URL\img\shota\$ID.jpg`.

