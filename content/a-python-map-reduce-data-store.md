Title: A Python Map Reduce Data Store
Date: 2012-12-03 10:20
Category: Python
Tags: python, postgresql
Slug: a-python-map-reduce-data-store
Author: James Casbon
Summary: Short version for index and feeds


I'm pleased to announce the release of a data store with python map reduce
capabilities that is also fully ACID compliant, supports SQL as a query
language, foreign keys and joins.  It is also well supported by numerous
companies and already available in many hosted environments.  Just kidding: I'm
talking, of course, about PostgreSQL. I only recently discovered the [excellent
python support](http://www.postgresql.org/docs/9.2/static/plpython.html) in Postgres, 
which allows you to run python functions inside queries.  This allows you to
create a python map reduce system with very little effort.  Of course, the point
of map reduce is more about distributing the computation, but if you're prepared
to don some [wooden headphones](http://en.wikipedia.org/wiki/Cargo_cult) for a 
moment...

First you need to install the plpython package (something like `postgresql-plpython-9.2`)
and install it in your database `postgres createlang plpython3u DBNAME`.

Now create our pymap function: 

    :::plpgsql
    CREATE FUNCTION pymap (src text, table_name text)
       RETURNS SETOF json
    AS $$
    import json
    exec src
    for row in plpy.execute("SELECT key, value FROM %s" % table_name):
        for emission in map_fn(row["key"], json.loads(row["value"])):
            yield json.dumps(emission)
     
    $$ LANGUAGE plpythonu; 

A test table, which is a key value table:

    :::plpgsql
    create table kv (key serial, value json);
    insert into kv (value) values ('{"foo": 100}');
    insert into kv (value) values ('{"foo": 200}');
    insert into kv (value) values ('{"bar": 300}');

Now we can use our pymap function by passing in a table name and python source
(which defines a map_fn):

    :::plpgsql
    select pymap('kv;', '
    def map_fn(k, v):
      if "foo" in v:  
        yield {k: v["foo"]}'
    '');
    
       pymap    
    ------------
     {"1": 100}
     {"2": 200}
    (2 rows)
        
But this is python, so lets do something more interesting, like use scipy to
calculate the gamma function...

    :::plpgsql
    select pymap('kv;', '
    def map_fn(k, v):
      import scipy.special
      if "foo" in v:  
        yield {k: scipy.special.gamma(float(v["foo"])/1000)}'
    '');

               pymap           
    ---------------------------
     {"1": 9.5135076986687324}
     {"2": 4.5908437119988026}
    (2 rows)

I'll leave the implementation of reduce as an exercise to the reader.  I hope
this has shown how useful having a full python interpreter in the database can
be.  There are currently versions for both python 2 and 3, but it would be
really nice if we had a link to libpypy-c which would then give JITed functions.

One potential use of plpython is that you can use it to create indexes on
computed values. If you've ever worked on a system that stores serialized
objects in a database, you'll understand what I mean.  To add an index to these,
you have to alter your database *and* code to store extra the extra data and then index it.
With plpython you could generate the index in the database without altering your data storage code:

    :::plpgsql
    CREATE FUNCTION two_of_foo (v json)
      RETURNS integer
    AS $$
      import json
      obj = json.loads(v)
      if 'foo' in obj: 
        return 2 * obj['foo']
      else:
        return None
     $$ LANGUAGE plpythonu IMMUTABLE;
    CREATE INDEX i_two_of_foo ON kv (two_of_foo(value));



Update: Anja Skrba kindly translated this page into [Serbo-Croatian](http://science.webhostinggeeks.com/skladistenje-podataka)

