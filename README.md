# Solr Build and Deployment
* Build Solr image and Deploying solrCloud. currently this is intiial version for deploying solr over google cloud GCP, soon i will publish the AWS version:
* Both ```solr-ansible/solr/files/replicaStatus.py``` and ```solr-ansible/solr/files/solrutil.py``` are NOT meant for the deployment purposes, i will document thm soon.
#### Image Build details:
* [Image build](ImageBuild.md)

#### Cluster deployment details:
* [Cluster Deployment](SolrCluster.md)

####  TODO soon. Improvments for the GCP version. Sepcificaly over Solr versions >=7.1
* Using MIGs, with solr versions >=7.1
* Allowing Autohealing based on customchecks, Solr versions >=7.1.
