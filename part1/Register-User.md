```mermaid
sequenceDiagram
    participant User
    participant API
    participant BusinessLogic
    participant Database

    User->>API: Register User
    API->>BusinessLogic: Validate and Process Request
    BusinessLogic->>Database: Save User Data
    Database-->>BusinessLogic: Confirm Save
    BusinessLogic-->>API: Return Response
    API-->>User: Return Success/Failure
