#!/usr/bin/env python3
"""
Improve 12-log_stats.py by adding the top 10 of the most present IPs in
the collection nginx of the database logs
"""
from pymongo import MongoClient


if __name__ == "__main__":
    """provides stats about nginx logs"""
    client = MongoClient('mongodb://127.0.0.1:27017')
    coll = client.logs.nginx
    print("{} logs".format(coll.count_documents({})))
    print("Methods:")
    for method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
        count = coll.count_documents({'method': method})
        print("\tmethod {}: {}".format(method, count))

    status_get = coll.count_documents({'method': 'GET', 'path': "/status"})
    print("{} status check".format(status_get))

    print("IPs:")
    ips = coll.aggregate([
        {"$group":
            {
                "_id": "$ip",
                "count": {"$sum": 1}
            }
         },
        {"$sort": {"count": -1}},
        {"$limit": 10},
        {"$project": {
            "_id": 0,
            "ip": "$_id",
            "count": 1
        }}
    ])

    for ip in ips:
        print(f"\t{ip.get('ip')}: {ip.get('count')}")
