
# KT for Solr Cluster Deploy
* #####  The scope of this document does not cover how ansible is working, nor it covers how solr is working
* #####  It is trying to be a guild for which part is doing what part during Solr releases

### Job build components:
* Packer
* Ansible

#### Packer related configs/scripts:

* [Packer config](solr/img-pakcer.json) : It containes packer confiurations, including ansible provisioner.
* Ansible roles for Solr image build:
     * [Solr role for pkg installation](solr/roles/solr) 
     * [Common role](solr/roles/common) for Java installation
     * [SolrBuild Playbook](solr/SolrBuild.yml)
     
* IAM SA `solr-image-build@my-dummy-project.iam.gserviceaccount.com` holding the following roles:
   ```
    Compute Admin
    Compute Instance Admin (v1)
    Service Account Token Creator
    Service Account User
    Source Repository Writer
    Storage Object Admin
  ```

* To build an image you might need to run this command:
  ```
    $ packer build solr/img-pakcer.json
    Knowing that this is desgined to run within Docker container and that container will be having all dependacies. 
  ```

* Firewall rules are needed  to allow SSH into the image while packer building it. 
  So we used this [tag](solr/img-pakcer.json#L27)



