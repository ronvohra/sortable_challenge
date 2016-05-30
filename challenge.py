import json
import io
import urllib2
import tarfile


def get_inputs(challenge_source, listings_filename, products_filename):

    source_file = urllib2.urlopen(challenge_source)

    # Code snippet (source: http://stackoverflow.com/a/18624269) to handle data files seamlessly
    tmp_file = io.BytesIO()
    while True:
        # Download a piece of the file from the connection
        s = source_file.read(8192)

        # Once the entire file has been downloaded, tarfile returns b''
        # (the empty bytes) which is a falsey value
        if not s:
            break

        # Otherwise, write the piece of the file to the temporary file.
        tmp_file.write(s)

    source_file.close()

    tmp_file.seek(0)

    t = tarfile.open(fileobj=tmp_file, mode='r:gz')

    listings_fileobj = t.extractfile(listings_filename)
    listings = []
    for line in listings_fileobj:
        listings.append(json.loads(line, encoding='utf8'))

    products_fileobj = t.extractfile(products_filename)
    products = []
    for line in products_fileobj:
        products.append(json.loads(line, encoding='utf8'))

    return listings, products


def get_matches(listings, products):

    count = 0
    matches = []

    for product in products:
        match = {}
        matched_listing = []
        match['product_name'] = product['product_name']
        for listing in listings:
            if product['manufacturer'] in listing['title'] and product['model'] in listing['title']:
                if listing not in matched_listing:
                    matched_listing.append(listing)
                match['listings'] = list(matched_listing)
        if len(matched_listing) > 0:
            matches.append(match)
            count += 1

    return matches


def main():

    challenge_link = 'https://s3.amazonaws.com/sortable-public/challenge/challenge_data_20110429.tar.gz'
    listings_file = 'listings.txt'
    products_file = 'products.txt'

    listings, products = get_inputs(challenge_link, listings_file, products_file)
    matches = get_matches(listings, products)

    with io.open('results.txt', 'w', encoding='utf-8') as f:
        for item in matches:
            s = json.dumps(item, ensure_ascii=False, encoding='utf8')
            f.write(s + u'\n')

if __name__ == '__main__':
    main()
