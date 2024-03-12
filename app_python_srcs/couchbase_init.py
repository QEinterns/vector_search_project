from couchbase.auth import PasswordAuthenticator
from couchbase.cluster import Cluster
from couchbase.options import (ClusterOptions, ClusterTimeoutOptions,QueryOptions)
from datetime import timedelta


def couchbase_init():

    username = "Administrator"
    password = "password"
    bucket_name = "b1"
    scope_name = "s1"
    collection_name = "cn1"

    auth = PasswordAuthenticator(
        username,
        password,
    )

    cluster = Cluster('couchbase://172.23.108.107', ClusterOptions(auth))
    cluster.wait_until_ready(timedelta(seconds=5))
    cb = cluster.bucket(bucket_name)
    cb_coll = cb.scope(scope_name).collection(collection_name)

    db = cluster.bucket(bucket_name)
    db_coll = db.scope(scope_name).collection("c3")

    eb = cluster.bucket(bucket_name)
    eb_coll = eb.scope(scope_name).collection("c6")

    rb = cluster.bucket(bucket_name)
    rb_coll = rb.scope(scope_name).collection("d1")
    
    ab = cluster.bucket(bucket_name)
    architect_coll = ab.scope(scope_name).collection("architect")

    return cb_coll,db_coll,eb_coll,rb_coll,architect_coll