# Overview
This project is a reference implementation of farmstack to showcase restricting the usage of data by an application container running a node.js application. This reference implementation can be used to create usage policies that require constraining the usage of data for the specific purpose of the project and/or avoid unintended leak or misuse of data. Most of the data sharing agreements require that the data consumer use the data for that purpose for which data is being exchanged. This can be bundled as a node.js or python application (language independent) hosted inside of an application container and the data usage policy with p2p connectors can be used to restrict data usage beyond the container. Usage control also dovetails with the consent management framework enhancing the access control to finegrained enforceable restrictions. The usage control can be viewed as superset of the access control. 

FarmStack consists of a p2p connector which is a fork from the [trusted connector](https://github.com/industrial-data-space/trusted-connector/) provided by IDSA - Fraunhofer AISEC. The p2p connectors manage docker containers and are assigned identities through which they can mutually authenticate each other and encrypt messages. IDSA also provides an IDS communication protocol which creates a secure web socket between connectors and acts as a remote attestation endpoint. The p2p connectors can be installed and run on premise by respective participants and used to provide data which can be accessed through a filesystem or a set of flexible APIs. The architecture laid down in the [IDSA reference architecture](https://www.internationaldataspaces.org/wp-content/uploads/2019/03/IDS-Reference-Architecture-Model-3.0.pdf) (published by Fraunhofer) is a message/stream driven architecture which routes data using the open source [Apache Camel](https://camel.apache.org/docs/) framework. At the core of IDSA architecture is an [information model](https://github.com/International-Data-Spaces-Association/InformationModel) which provides the language independent description of digital resources (connectors, data description or any service etc). The information model is programmatically implemented in Java and the maven repositories are hosted in the public domain [here](https://jira.iais.fraunhofer.de/stash/projects/ICTSL/repos/ids-infomodel-demo/browse) by Fraunhofer IAIS. These classes are used to construct messages that are used to control the routing of data. The [available message types](https://htmlpreview.github.io/?https://github.com/IndustrialDataSpace/InformationModel/blob/feature/message_taxonomy_description/model/communication/Message_Description.htm) of IDSA is given here. The high level abstraction of data sharing using connectors is shown below.

<img src="data_sharing.png"  height="250">

## Trusted Connector details

<img src="connector_architecture.png"  height="250">

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


# Implementation
In this reference implementation, there is one provider and one consumer, both running a FarmStack p2p connector. The connectors mutually authenticate and encrypt data through the SSL certificates provided to them from a simulated certificate authority. The provider configures a usage policy that refers to the hash of a container that can access data. The data provider has one sample csv file. The data consumer receives the data in IDS protocol (a secured web socket protocol developed by Fraunhofer AISEC). IDSCP enables metadata exchange and remote attestation, creating a trusted tunnel between connector instances. It has a node application running within the container of the p2p connector that renders and displays the data in html format (browser).

The usage policy essentially constrains that data be not used by any other container or if the container is modified. This is a basic example that can be used to create multiple usage restrictions that require data being available and used for only specific applications.

## Data provider side
<img src="FS_UCDiagram-UC(Provider).png"  height="250">

## Data consumer side
<img src="FS_UCDiagram-UC(consumer).png"  height="250">

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
