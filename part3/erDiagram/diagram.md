erDiagram
    USER {
        int id
        string first_name
        string last_name
        string email
        string password
        boolean is_admin
    }
    PLACE {
        int id
        string name
        string description
        int owner_id
    }
    REVIEW {
        int id
        string text
        int user_id
        int place_id
    }
    AMENITY {
        int id
        string name
    }
    PLACE_AMENITY {
        int place_id
        int amenity_id
    }

    USER ||--o{ PLACE : "owns"
    USER ||--o{ REVIEW : "writes"
    PLACE ||--o{ REVIEW : "has"
    PLACE }|--|{ AMENITY : "has many"
    PLACE ||--o{ PLACE_AMENITY : ""
    AMENITY ||--o{ PLACE_AMENITY : ""
