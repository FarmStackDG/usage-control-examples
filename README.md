# Overview
This project is a reference implementation of farmstack to showcase restricting the usage of data by an application container running a node.js application. This reference implementation can be used to create usage policies that require constraining the usage of data for the specific purpose of the project and/or avoid unintended leak or misuse of data. Most of the data sharing agreements require that the data consumer use the data for that purpose for which data is being exchanged. This can be bundled as a node.js or python application (language independent) hosted inside of an application container and the data usage policy with p2p connectors can be used to restrict data usage beyond the container. Usage control also dovetails with the consent management framework enhancing the access control to finegrained enforceable restrictions. The usage control can be viewed as superset of the access control. 

FarmStack consists of a p2p connector which is a fork from the [trusted connector](https://github.com/industrial-data-space/trusted-connector/) provided by IDSA - Fraunhofer AISEC. The p2p connectors manage docker containers and are assigned identities through which they can mutually authenticate each other and encrypt messages. IDSA also provides an IDS communication protocol which creates a secure web socket between connectors and acts as a remote attestation endpoint. The p2p connectors can be installed and run on premise by respective participants and used to provide data which can be accessed through a filesystem or a set of flexible APIs. The architecture laid down in the [IDSA reference architecture](https://www.internationaldataspaces.org/wp-content/uploads/2019/03/IDS-Reference-Architecture-Model-3.0.pdf) (published by Fraunhofer) is a message/stream driven architecture which routes data using the open source [Apache Camel](https://camel.apache.org/docs/) framework. At the core of IDSA architecture is an [information model](https://github.com/International-Data-Spaces-Association/InformationModel) which provides the language independent description of digital resources (connectors, data description or any service etc). The information model is programmatically implemented in Java and the maven repositories are hosted in the public domain [here](https://jira.iais.fraunhofer.de/stash/projects/ICTSL/repos/ids-infomodel-demo/browse) by Fraunhofer IAIS. These classes are used to construct messages that are used to control the routing of data. The [available message types](https://htmlpreview.github.io/?https://github.com/IndustrialDataSpace/InformationModel/blob/feature/message_taxonomy_description/model/communication/Message_Description.htm) of IDSA is given here. The high level abstraction of data sharing using connectors is shown below.

<img src="data_sharing.png"  height="250">

## Trusted Connector details

<img src="connector_architecture.png"  height="250">

# Implementation
In this reference implementation, there is one provider and one consumer, both running a FarmStack p2p connector. The connectors mutually authenticate and encrypt data through the SSL certificates provided to them from a simulated certificate authority. The provider configures a usage policy that refers to the hash of a container that can access data. The data provider has one sample csv file. The data consumer receives the data in IDS protocol (a secured web socket protocol developed by Fraunhofer AISEC). IDSCP enables metadata exchange and remote attestation, creating a trusted tunnel between connector instances. It has a node application running within the container of the p2p connector that renders and displays the data in html format (browser).

The usage policy essentially constrains that data be not used by any other container or if the container is modified. This is a basic example that can be used to create multiple usage restrictions that require data being available and used for only specific applications.

## Data provider side
<img src="FS_UCDiagram-UC(Provider).png"  height="250">

## Data consumer side
<img src="FS_UCDiagram-UC(consumer).png"  height="250">
