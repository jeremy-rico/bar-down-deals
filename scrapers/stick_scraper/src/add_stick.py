"""
This is a utility script to manually add a new stick and set up for tracking.
For each stick you must manually enter the following:
1. msrp, current MAP price (at time of adding), flex options, flex, and urls for
each variation (Senior, Intermediate, Junior, Youth)
2. various details in the stick_info dict
3. upload images to s3 and add them in the image_urls list

Its a pain in the ass, I know. But it only has to be done once per stick.
"""

from datetime import datetime, timezone

from api.src.sticks.models import Stick, StickImage, StickURL
from scrapers.stick_scraper.src.database import get_session

session = get_session()

# Database configuration
DB_CONFIG = (
    "dbname=bar_down_deals_db "
    "user=postgres "
    "password=ut2VDdjkqd0n5OvPmB3Q "
    "host=bar-down-deals-db.cvsyy2gmax9g.us-west-1.rds.amazonaws.com "
    "port=5432"
)

conn = psycopg2.connect(DB_CONFIG)
cur = conn.cursor()

# Details for each variation
variations = {
    # "Senior": {
    #     "msrp": 399.99,
    #     "price": 399.99,
    #     "flex": 70,
    #     "flexes": "70,75,80,85",
    #     "urls": [
    #         ["bauerHockeyUS", ""],
    #         ["ccmHockeyUS", ""],
    #         ["discountHockey", ""],
    #         ["hockeyMonkeyUS", ""],
    #         ["iceWarehouseS", ""],
    #         ["peranisHockeyWorld", ""],
    #         ["pureHockey", ""],
    #     ],
    # },
    "Intermediate": {
        "msrp": 349.99,
        "price": 271.99,
        "flex": 55,
        "flex_options": "55, 65",
        "urls": [
            # ["bauerHockeyUS", ""],
            [
                "ccmHockeyUS",
                "https://us.ccmhockey.com/Sticks/Shop-All-Sticks/Jetspeed/HSFT7P-IN.html",
            ],
            [
                "discountHockey",
                "https://discounthockey.com/products/ccm-hsft7p-in?variant=40891649425471",
            ],
            [
                "hockeyMonkeyUS",
                "https://www.hockeymonkey.com/ccm-hockey-stick-jetspeed-ft7-pro-int.html",
            ],
            [
                "iceWarehouse",
                "https://www.icewarehouse.com/CCM_Jetspeed_FT7_Pro/descpage-JFT7P.html",
            ],
            [
                "peranisHockeyWorld",
                "https://www.hockeyworld.com/CCM-Jetspeed-FT7-Pro-Hockey-Stick-Int",
            ],
            [
                "pureHockey",
                "https://www.purehockey.com/product/ccm-jetspeed-ft7-pro-grip-composite-hockey-stick-intermediate/itm/63165-31/",
            ],
        ],
    },
    "Junior": {
        "msrp": 259.99,
        "price": 207.99,
        "flex": 40,
        "flex_options": "40, 50",
        "urls": [
            # ["bauerHockeyUS", ""],
            # ["ccmHockeyUS", ""],
            [
                "discountHockey",
                "https://discounthockey.com/products/ccm-hsft7p-jr?variant=40891657945151",
            ],
            [
                "hockeyMonkeyUS",
                "https://www.hockeymonkey.com/ccm-hockey-stick-jetspeed-ft7-pro-jr.html",
            ],
            [
                "iceWarehouse",
                "https://www.icewarehouse.com/CCM_Jetspeed_FT7_Pro/descpage-JFT7P.html",
            ],
            [
                "peranisHockeyWorld",
                "https://www.hockeyworld.com/CCM-Jetspeed-FT7-Pro-Hockey-Stick-Jr",
            ],
            [
                "pureHockey",
                "https://www.purehockey.com/product/ccm-jetspeed-ft7-pro-grip-composite-hockey-stick-junior/itm/63165-21/",
            ],
        ],
    },
    "Youth": {
        "msrp": 199.99,
        "price": 159.99,
        "flex": 30,
        "flex_options": "30",
        "urls": [
            # ["bauerHockeyUS", ""],
            # ["ccmHockeyUS", ""],
            # ["discountHockey", ""],
            [
                "hockeyMonkeyUS",
                "https://www.hockeymonkey.com/ccm-hockey-stick-jetspeed-ft7-pro-yt.html",
            ],
            # ["iceWarehouse", ""],
            [
                "peranisHockeyWorld",
                "https://www.hockeyworld.com/CCM-Jetspeed-FT7-Pro-Hockey-Stick-Yth",
            ],
            [
                "pureHockey",
                "https://www.purehockey.com/product/ccm-jetspeed-ft7-pro-grip-composite-hockey-stick-youth/itm/63165-11/",
            ],
        ],
    },
}

# Details that are the same across all variations
stick_info = {
    "model_name": "CCM Jetspeed FT7 Pro",
    "brand": "CCM",
    "line": "Jetspeed",
    "handedness": "Left",
    "curve": "P28",
    "curve_options": "P90TM, P28, P29, P88",
    "release_year": 2024,
    "updated_at": datetime.now(timezone.utc),
    "created_at": datetime.now(timezone.utc),
    "description": "Experience unmatched speed and puck feel with the JETSPEED FT7 PRO hockey stick, designed for the ultimate performance. Engineered with the latest Nanolite shield carbon technology, this stick is lightweight and incredibly responsive. Its hybrid kickpoint is tailored for speed and versatility, allowing you to beat the goalies with all types of shots. The highlight of the FT7 PRO is its new and advanced blade, crafted to enhance your puck handling and control. With its sleek design and superior performance, this stick is your key to dominating the game with speed and puck feel.",
    "kickpoint": "Hybrid",
    "currency": "USD",
    "price_drop": False,
    "historical_low": False,
}

# link to s3 URL
image_urls = [
    "https://bar-down-deals-bucket.s3.us-west-1.amazonaws.com/images/sticks/CCM+Jetspeed+FT7+Pro/191520768720-1_37.webp",
    "https://bar-down-deals-bucket.s3.us-west-1.amazonaws.com/images/sticks/CCM+Jetspeed+FT7+Pro/191520768720-2.webp",
    "https://bar-down-deals-bucket.s3.us-west-1.amazonaws.com/images/sticks/CCM+Jetspeed+FT7+Pro/191520768720-3.webp",
    "https://bar-down-deals-bucket.s3.us-west-1.amazonaws.com/images/sticks/CCM+Jetspeed+FT7+Pro/191520768720-4.webp",
    "https://bar-down-deals-bucket.s3.us-west-1.amazonaws.com/images/sticks/CCM+Jetspeed+FT7+Pro/191520768720-5.webp",
    "https://bar-down-deals-bucket.s3.us-west-1.amazonaws.com/images/sticks/CCM+Jetspeed+FT7+Pro/191520768720-6.webp",
    "https://bar-down-deals-bucket.s3.us-west-1.amazonaws.com/images/sticks/CCM+Jetspeed+FT7+Pro/191520768720-icon.webp",
]

for variation, variation_details in variations.items():
    stick_info["size"] = variation
    stick_info["msrp"] = variation_details["msrp"]
    stick_info["price"] = variation_details["price"]
    stick_info["flex"] = variation_details["flex"]
    stick_info["flex_options"] = variation_details["flex_options"]
    discount = ((stick_info["msrp"] - stick_info["price"]) / stick_info["msrp"]) * 100
    stick_info["discount"] = round(discount, 2)
    stick = Stick(**stick_info)
    session.add(stick)
    session.commit() w

    cols = (", ").join([col for col in stick_info.keys()])
    vals = (", ").join(["%s" for _ in range(len(stick_info.keys()))])

    query = f"""
        INSERT INTO stick ({cols})
        VALUES ({vals})
        RETURNING id;
    """

    cur.execute(query, list(stick_info.values()))
    stick_id = cur.fetchone()[0]

    for image_url in image_urls:
        query = f"""
            INSERT INTO stickimage (url, stick_id)
            VALUES (%s, %s)
            RETURNING id;
        """
        values = [image_url, stick_id]
        cur.execute(query, values)

    price_urls = variation_details["urls"]
    for price_url in price_urls:
        query = f"""
        INSERT INTO stickurl (spider_name, url, stick_id)
        VALUES (%s, %s, %s)
        """
        price_url.append(stick_id)
        cur.execute(query, price_url)

conn.commit()
cur.close()
conn.close()
