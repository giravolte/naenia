Naenia
--------
Simple library for Bencode encoding/decoding.
This is an updated version of the original [bencode parser](https://github.com/bittorrent/bencode), originally written by **Petru Paler**.

- http://en.wikipedia.org/wiki/Bencode
- https://wiki.theory.org/BitTorrentSpecification#Bencoding

Usage
--------
I'm too lazy to publish it on PyPI, so just download the file, add it to your project, and import it manually.
The main functions provided are:

- `bencode`: encodes data into the Bencode format.
- `bdecode`: decodes Bencoded data back into Python types.
