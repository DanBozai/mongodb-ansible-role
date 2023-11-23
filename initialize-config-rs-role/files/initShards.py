#!/home/mongodb/miniconda3/envs/pymongo_env/bin/python

from pymongo import MongoClient
import yaml

def read_config(yaml_file):
    with open(yaml_file, "r") as stream:
        try:
            config= yaml.safe_load(stream)
            primarySvrs = config['primary']
            replicaSvrs = config['replica']

        except yaml.YAMLError as exc:
            print(exc)
        finally:
            stream.close()

    return primarySvrs, replicaSvrs


config_file = "/home/mongodb/Downloads/shards_config.yaml"
primary, replica = read_config(config_file)


totalSv=len(primary)+len(replica)

mongo_prefix='mongodb://'
def buildShardMembers(primarySv,rs1,rs2):
    replica_config={
        '_id': 'shsv1',
        'members':[
        {'_id': 0, 'host': primarySv},
        {'_id': 1, 'host': rs1},
        {'_id': 2, 'host': rs2}
        ]}
    return replica_config

count_index=0

if (totalSv)%3==0:
    try:

        for it in primary:

            URI=mongo_prefix+it

            client = MongoClient(URI)
            db = client['admin']
            rs_config= buildShardMembers(it,replica[count_index],replica[count_index+1])

            db.command('replSetInitiate',rs_config)
            client.close()
            count_index+=2
            rs_config=None
            URI.strip()

    except Exception as err:
        print(err)
    finally:
        client.close()
else:
   print("ERROR: Number of servers mismatch, specify 2 replica servers for each primary server in 'shards_config.yaml")
