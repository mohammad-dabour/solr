
# KT for Solr Cluster Deploy
* #####  The scope of this document does not cover how ansible is working, nor it covers how solr is working.
* #####  It is trying to be a guide for which part is doing what part during Solr releases.
* ##### There are reasons why I did not use migs for this release on GCP. However next updates will be using migs.
* ##### Currently cluster supports multiple reagions and multiple zones.

### Components:

* Ansible
* ZK is not covered in this part (to be covred soon).

#### Create a cluster:

* Ansible roles for Solr cluster creation:
     * [Solr cluster template, for creating cluster](solr/roles/solr_gc_template) 
     * [Solr cluster create playbook](solr/cerate_solr_cluster.yml)

     ```
     # Running this playbook will initit the cluster
     $ ansible-playbook cerate_solr_cluster.yml  --tags "gc_template" -vvv
     
     ```
     
 * Take in consideration below configs from [defaults](solr/roles/solr_gc_template/defaults/main.yml
) :
 ```
     env: my-dummy-project
     sa_name: solr-service-sa
     machine_type: n1-highmem-2
     zones: {us-east1: [b,c,d], us-central1: [b,c,f]}
     fqd: "c.{{ env }}.internal:8983_solr"
     img: 'solr-image-name'
     zkcluster: 'clutster1'
     shards: 1
     replicas: 3
     collection_bucket: collections-bucket
     collections: [collection1,collection2,collection3]
     collectionConf: {collection1: 'all', collection2: 'all',collection3: [1]}
     maxShardsPerNode: 1
     postfix: "a"
 ```
 
 * Once cluster created there will be a file called hosts under /tmp directory. This represents a temp hosts inventory.
 * Create [Collections](solr/cerate_solr_collection.yml):
 
 ```
 $ ansible-playbook  -i ${IP}, cerate_solr_collection.yml --private-key=/home/deployer/.ssh/deployer-key --extra-vars="solr=${HOST}"
 ````
 
* Create [Replicas](solr/cerate_solr_replicas.yml):

```
ansible-playbook  cerate_solr_replicas.yml  --private-key=/home/deployer/.ssh/deployer-key --extra-vars="solr=${SOLR_HOST} region=${region}"
```


* [Mount gcsfuse](solr/mount_backup.yml):
```
$ ansible-playbook mount_backup.yml  -i /tmp/hosts --private-key=/home/deployer/.ssh/deployer-key
```

* IAM SA `solr-image-build@my-dummy-project.iam.gserviceaccount.com` holding the following roles:
   ```
    Compute Admin
    Compute Instance Admin (v1)
    Service Account Token Creator
    Service Account User
    Source Repository Writer
    Storage Object Admin
  ```


* Firewall rules are needed  to allow SSH into the image while packer building it. 
  So we used this [tag](solr/img-pakcer.json#L23)

