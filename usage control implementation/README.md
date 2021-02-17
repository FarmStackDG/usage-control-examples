## Data usage control
In information security, access control restricts access to digital resources. The term authorization is the process of granting permission to resources. Several access control models exist, such as Discretionary Access Control (DAC), Mandatory Access Control (MAC), Role-based Access Control (RBAC), Attribute-based Access Control (ABAC), etc. The XACML (eXtensible Access Control Markup Language) Standard is commonly used in the field of access control. XACML is a policy language to express ABAC rules. 

In contrast to access control, where access to specific digital resources (e.g., a service or a file) is restricted, the IDS architecture additionally supports data-centric usage control. The overall goal is to enforce usage restrictions for data after access has been granted though policies that bind to data being exchanged. At configuration time, these policies support developers and administrators in setting up correct data flows. Usage control itself does not establish trust in an endpoint. It rather builds upon an existing trust relationship and facilitates the enforcement of legal or technical requirements or data privacy regulations. 

To implement the usage policies, the policies need to be machine readable and based on common standards so that they can be enforced. The IDS usage policy language therefore relies on the Open Digital Rights Language (ODRL). ODRL is a W3C recommendation and specifies a vocabulary and data model for the description of digital and machine-readable contracts. The IDS further extends ODRL towards usage control descriptions and enforcement, provides explanations regarding the compliant interpretation of constructs and defines implications for real-world implementations. This is accomplished in the form of IDS subclass constructs to the according ODRL classes. The design preserves the structure of the introduced terminology, resulting in the compliance of IDS usage policy with ODRL recommendations. 

The fundamental building blocks for IDS Policies are the Contracts. Contracts present the container of any usage control statement and come in three different realizations: Requests, Offers, and Agreements. While all share a similar syntax, their interpretation is slightly different. 
 - Contract requests are created by data consumers and indicate a desire to achieve a certain contract. 
 - Contract offers are created by data providers and indicate willingness to exchange data or services as outlined in Contract Offers. 
 - Contract agreements represent a binding and final consent to the stated constraints and requirements. A contract agreement is the IDS terminology for a valid contract, which both sides accept and therefore is binding as far as the IDS is related.

It must be noted that contract requests and contract offers are purely informative pieces of information and do not bind any contract. The figure below represents the hierarchical structure of a usage policy.

<img src="uc_1.png"  height="250">


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
