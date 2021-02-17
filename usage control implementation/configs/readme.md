
## File structure

**docker-compose-provider.yaml:**</br>
    Instantiates the configuration of docker containers on provider connector like ports, networks etc. It also mounts the file that defines data routing at provider connector: example-provider-routes.xml </br>
    This is the file that needs to be executed to run the provider connector. To run the provider connector execute the command, docker-compose -f docker-compose-provider.yaml up</br>

**docker-compose-consumer.yaml:** </br> 
    Instantiates the configuration of docker containers on consumer connector like ports, networks etc. It also mounts the file that defines data routing at consumer connector: example-consumer-routes.xml </br>
    This is the file that needs to be executed to run the consumer connector. To run the provider connector execute the command, docker-compose -f docker-compose-consumer.yaml up</br>

**example-provider-routes.xml:** </br>
    Configures data routing at the provider connector using [CAMEL](https://camel.apache.org/).

**example-consumer-routes.xml:**</br>
    Configures data routing at the consumer connector using [CAMEL](https://camel.apache.org/).

## Contract agreement message flow
    Step 1: Data consumer (IDSCP2 - Client) requests contract and sends ContractRequestMessage
    Step 2: Data provider (IDSCP2 - Server) checks the contract offer and if ok, sends ContractResponseMessage
    Step 3: Data consumer checks the ContractOffer and sends back the ContractAgreementMessage

<img src="uc_2.png"  height="250">
In the current code, step1 is simulated by having a dummy ContractRequest.

## CAMEL Classes
    Following classes are used in the respective xml files in provider and consumer. The actual classes are hosted by Fraunhofer.
## Provider
1. Class name: ContractOfferCreationProcessor
    1. Function: 
        - takes ContractRequestMessage as input and gives ContractResponseMessage as output
        - Sets container uri property to a hash value thereby allowing use of data only by a specific container
        - Serializes ContractOffer to a json object
    2. Important methods:
        - ContractOfferBuilder() from de.fraunhofer.iais.eis.* 
        - [Utils](https://github.com/industrial-data-space/trusted-connector/blob/develop/camel-idscp2/src/main/kotlin/de/fhg/aisec/ids/camel/idscp2/Utils.kt)
        - [Constants](https://github.com/industrial-data-space/trusted-connector/blob/develop/camel-idscp2/src/main/kotlin/de/fhg/aisec/ids/camel/idscp2/Constants.kt)
    3. Where: the first step of the route

2. Class name: TypeExtractionProcessor
    1. Function: Extracts the type of the message
    2. Why: Need to know what is the message type to trigger necessary action
    3. Where: After Provider sends ContractResponseMessage ContractAgreementMessage is 
3. Class name: ContractAgreementReceiverProcessor
    1. Function:
        - Takes ContractAgreement as input and saves it to UsageControlMaps object 
        - Deserialize ContractAgreement and saves its properties like container uri and artifacturi to hashmap for quick lookup in ProviderDB object
    2. Important methods:
        - [ProviderDB](https://github.com/industrial-data-space/trusted-connector/blob/develop/camel-idscp2/src/main/kotlin/de/fhg/aisec/ids/camel/idscp2/Constants.kt)
        - [UsageCotnrolMaps](https://github.com/industrial-data-space/trusted-connector/blob/develop/camel-idscp2/src/main/kotlin/de/fhg/aisec/ids/camel/idscp2/UsageControlMaps.kt)
    3. Where: Last step of accepting agreement
4. Class name: ResourceUpdateCreationProcessor
    1. Function:
    Message indicating the availability and current description of a specific resource
    2. Important Methods: Covered in previous classes
    3. Where: While sending the data (resource)

## Consumer
1. Class name: ContractOfferProcessor
    1. Function:
        - Handles a ContractResponseMessage and creates a ContractAgreementMessage
    2. Saves contract
        - Important methods: covered in previous classes
    3. Where: The first message to consumer
2. Class name: TypeExtractionProcessor
    1. Covered in provider (same function here)
