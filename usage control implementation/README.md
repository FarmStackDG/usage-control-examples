## Code structure
Config/
 - Includes the configuration related files:<br>
    - Docker configuration for provider and consumer connectors (yaml files)
    - Data routing configurations of provider and consumer (xml files)<br>

Src/
 - Includes the demo nodejs application code

Cert stores/
 - Includes the certificate files issued by certificate authority

## To run connectors on single machine
 - To run provider node
    - change directory to IDSA-FS-DEMO/configs run $docker-compose -f docker-compose-provider.yaml up
 - To run the consumer node
    - Change directory to IDSA-FS-DEMO/configs run $docker-compose -f docker-compose-consumer.yaml up

## To run connectors separately on provider and consumer

 ### Add following lines in the respective files
        a. In the directory Configs/ add in the file docker-compose-provider.yaml following line in the provider-core docker service
        extra_hosts: - "consumer-core:your-consumer-machine-ip"

        b. In the directory Configs/ add in the file docker-compose-consumer.yaml following line in the consumer-core docker service
        extra_hosts: - "provider-core:your-provider-machine-ip"

## To test usage control(UC)
The current UC integration is provisioned to facilitate no-tampering in the running data-application consumer container using the digest(docker image’s id) which contains SHA256 hash, In case there is any change in the running data-application consumer container the image hash won’t match and the transfer would get rejected.

### Steps to prepare for UC integration :

Assuming we are in configs folder<br>
docker build ../src/consumer-apps/merge-csv-nodejs -t merge-csv-nodejs -q<br>
output - image-hash<br>
save merge-csv-nodejs > merge-csv-nodejs.tar<br>
docker load -i merge-csv-nodejs.tar<br>
docker tag image-hash merge-csv-nodejs<br>
