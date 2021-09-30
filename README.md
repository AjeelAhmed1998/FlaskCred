# FlaskCred
Back end API simulating an Audio server

# FlaskCred Documentation



Back end engineering project simulating an Audio Server using Flask and SQLite.

As I had not used SQL in a long time I saw this coding exercise as as opportunity to revise some of the concepts such as foreign keys and joins. 

Where full URLs are provided in responses they will be rendered as if service
is running on 'http://127.0.0.1:5000/'.

## Open Endpoints



Open endpoints require no Authentication.

* Get Specific Song/Podcast/Audiobook: `GET /{audioFileType}/{audioFileId}
Body: None
Response: [
    3,
    "seigfried",
    "2021-09-25 17:11:32"
]`

* Get All Songs/Podcasts/Audiobooks: `GET /{audioFileType}
Body: None
Response: [
    [
        3,
        "seigfried",
        120,
        "2021-09-25 17:11:32"
    ],
    [
        5,
        "nikes",
        120,
        "2021-09-30 11:12:11"
    ]
]`

* Create Song : `POST /
Body: {
    "audioFileType": "song", 
    "audioFileMetadata":{
        "name": "nikes", 
        "duration": 120
    }
}

Response: {
    "audioFileMetadata": {
        "duration": 100,
        "host": "80",
        "name": "cs101",
        "participants": [
            "joe",
            "ali",
            "jess"
        ]
    },
    "audioFileType": "podcast"
}
`

* Create Podcast : `POST /
Body: {
    "audioFileType": "podcast", 
    "audioFileMetadata": {
        "name": "cs101", 
        "duration": 100, 
        "host": "80", 

        "participants": ["joe", "ali","jess"]

    }
}

Response: {
    "audioFileMetadata": {
        "duration": 100,
        "host": "80",
        "name": "cs101",
        "participants": [
            "joe",
            "ali",
            "jess"
        ]
    },
    "audioFileType": "podcast"
}`

* Create Audiobook : `POST /
Body: {
    "audioFileType": "audiobook", 
    "audioFileMetadata": {
    "title":"Story of Ajeel", 
    "author": "Ajeel Ahmed", 
    "narrator": "Ajeel Ahmed", 
    "duration": 120
    }
}

Response: {
    "audioFileMetadata": {
        "author": "Ajeel Ahmed",
        "duration": 120,
        "narrator": "Ajeel Ahmed",
        "title": "Story of Ajeel"
    },
    "audioFileType": "audiobook"
}   `

* Update Song: `PATCH /song/{id}
Body: {

    "name": "selfcontrol", 
    "duration": "130"
    
}
Response: {
  "UPDATED":"TRUE"
}`

* Update Podcast: `PATCH /podcast/{id}
Body: {

    "name": "selfcontrol", 
    "duration": "130", 
    "host": "Frank Ocean"
    
}
Response: {
  "UPDATED":"TRUE"
}`

*Update Audiobook:  `PATCH /audiobook/{id}
Body: {

    "title": "AJ", 
    "author": "Ajeel", 
    "narrator": "Ahmed"
    
}
Response: {
  "UPDATED":"TRUE"
}


*Delete Song/Podcast/Audiobook: `DELELTE /{audioFileType}/{audioFileId}`
Response: {
  "DELETED":"TRUE"
}
`


### Unit Testing




* test_index : Checks whether hitting GET /song/1 returns a HTTP 200 code. 
* test_audio_content: Checks whether the response content type is application/json form. 
* test_audio_body: Checks whether the response body returns the desired result the user asked for. 


