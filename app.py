from flask import Flask, request, jsonify, Response, abort
import sqlite3
import json

app = Flask(__name__)
conn = sqlite3.connect('testing.db',check_same_thread=False)


# FOR CREATE
@app.route('/', methods=['POST'])
def create():
    content = request.json

    # data = json.loads(participants)
    # data_list = data["participants"]
    try:
        if content['audioFileType'] == 'song':
            conn.execute(f'''INSERT INTO SONG (NAME, DURATION)
                        VALUES('{content['audioFileMetadata']['name']}',
                        '{content['audioFileMetadata']['duration']}' )''')
            conn.commit()
            return jsonify(content)
        elif content['audioFileType'] == 'podcast':
            participants = content["audioFileMetadata"]["participants"]

            print(content["audioFileMetadata"]["participants"])
            cur = conn.cursor()
            cur.execute(f'''
                    INSERT INTO PODCAST(NAME, DURATION, HOST)
                    VALUES('{content['audioFileMetadata']['name']}',
                            '{content['audioFileMetadata']['duration']}',
                            '{content['audioFileMetadata']['host']}')
                    ''')
            last_id = cur.lastrowid
            conn.commit()
            for value in participants:
                conn.execute(f'''
                        INSERT INTO PARTICIPANTS(P_ID, NAME)
                        VALUES('{last_id}', '{value}')
                        ''')
            conn.commit()
            return jsonify(content)

        elif content['audioFileType'] == 'audiobook':
            cur = conn.cursor()
            cur.execute(f'''
                        INSERT INTO AUDIOBOOK(TITLE,AUTHOR,NARRATOR,DURATION)
                        VALUES('{content['audioFileMetadata']['title']}',
                        '{content['audioFileMetadata']['author']}',
                        '{content['audioFileMetadata']['narrator']}',
                        '{content['audioFileMetadata']['duration']}')
                    
            ''')
            conn.commit()
            return jsonify(content)
        else:
            return Response("{ISSUE: path does not exist}", status=400, mimetype='application/json')
    except Exception as e:
        print (e)


@app.route('/<audioFileType>', defaults={'audioFileId': None})
@app.route('/<audioFileType>/<audioFileId>')
def read(audioFileType, audioFileId):
    # response ="nonne"
    try:
        if audioFileType == "song" and audioFileId == None:
            cur = conn.cursor()
            cur.execute('''
            SELECT * FROM SONG
            ''')
            return jsonify(cur.fetchall())

        elif audioFileType == "song" and audioFileId!=None :
            cur = conn.cursor()
            statement = '''
            SELECT ID, NAME, UPLOADED FROM SONG WHERE ID = ?'''
            cur.execute(statement,[audioFileId])
            return jsonify(cur.fetchone())

        elif audioFileType == "podcast" and audioFileId==None:
    #         return only one podcast
            cur = conn.cursor()
            statement = '''
            SELECT PODCAST.ID, PODCAST.NAME, PODCAST.DURATION, PODCAST.UPLOADED, 
            PODCAST.HOST, PARTICIPANTS.NAME 
            FROM PODCAST 
            INNER JOIN PARTICIPANTS
            ON PODCAST.ID = PARTICIPANTS.P_ID
             
            '''

            cur.execute(statement)
            return jsonify(cur.fetchall())
        elif audioFileType == "podcast" and audioFileId!=None:
            cur = conn.cursor()
            statement = '''
            SELECT PODCAST.ID, PODCAST.NAME, PODCAST.DURATION, PODCAST.UPLOADED, 
            PODCAST.HOST, PARTICIPANTS.NAME 
            FROM PODCAST 
            INNER JOIN PARTICIPANTS
            ON PODCAST.ID = PARTICIPANTS.P_ID
    
            '''
            statement_for_participants='''
            SELECT PARTICIPANTS.NAME 
            FROM PODCAST
            
            INNER JOIN PARTICIPANTS
            ON PODCAST.ID = PARTICIPANTS.P_ID
            '''
            # parti = list(cur.execute(statement_for_participants))

            # print("parti")
            # print(parti)
            cur.execute(statement)
            return jsonify(cur.fetchone())


        elif audioFileType == "audiobook" and audioFileId == None:
            cur = conn.cursor()
            cur.execute('''
            SELECT * FROM AUDIOBOOK
            ''')
            return jsonify(cur.fetchall())

        elif audioFileType == "audiobook" and audioFileId!=None :
            cur = conn.cursor()
            statement = '''
            SELECT ID, TITLE, AUTHOR, NARRATOR,  UPLOADED FROM AUDIOBOOK WHERE ID = ?'''
            cur.execute(statement,[audioFileId])
            return jsonify(cur.fetchone())
        else:
            return Response("{ISSUE: path does not exist}", status=400, mimetype='application/json')
    except:
        raise Exception("invalid input or wrong path")





@app.route('/<audioFileType>/<audioFileId>', methods=['PATCH'])
def update(audioFileType, audioFileId):

    content = request.json
    try:
        if audioFileType == "song":
            cur = conn.cursor()
            statement = '''
            UPDATE SONG SET NAME = ?, DURATION =? WHERE ID = ? 
            '''
            cur.execute(statement, [content['name'], content['duration'], audioFileId])
            conn.commit()
            return {
                'UPDATED': 'TRUE'
            }
        elif audioFileType == "podcast":
            curr = conn.cursor()
            print("I'm here")
            statement = '''
            UPDATE PODCAST SET NAME = ?, DURATION = ?, HOST  = ? WHERE ID = ? 
            '''
            curr.execute(statement, [content['name'], content['duration'],content['host'], audioFileId])
            conn.commit()
            return {
                'UPDATED': 'TRUE'
            }
        elif audioFileType == "audiobook":
            curr = conn.cursor()
            statement = '''
                UPDATE AUDIOBOOK SET TITLE = ?, AUTHOR = ?, NARRATOR = ? WHERE ID = ? 
            '''
            curr.execute(statement, [content['title'],content['author'],content['narrator'], audioFileId])
            conn.commit()
            return {
                "UPDATED": "TRUE"
            }

        else:
            return Response("{ISSUE: path does not exist}", status=400, mimetype='application/json')
    except Exception as e :
        # raise Exception("entered invalid wrong path or invalid input in the body")
        print(e)


@app.route('/<audioFileType>/<audioFileId>', methods=['DELETE'])
def delete(audioFileType, audioFileId):
    try:
        if audioFileType=="song":
            cur = conn.cursor()
            statement = '''
            DELETE FROM SONG WHERE ID = ? 
            '''
            cur.execute(statement, [audioFileId])
            conn.commit()
            return {
                "DELETED": "TRUE"
            }
        elif audioFileType == "podcast":
            cur = conn.cursor()
            statement = '''
            DELETE FROM PODCAST WHERE ID = ? 
            '''
            cur.execute(statement, [audioFileId])
            conn.commit()
            return {
                "DELETED": "TRUE"
            }
        elif audioFileType == "audiobook":
            cur = conn.cursor()
            statement = '''
            DELETE FROM AUDIOBOOK WHERE ID = ? 
            '''
            cur.execute(statement, [audioFileId])
            conn.commit()
            return {
                "DELETE": "TRUE"
            }
        else:
            return Response("{ISSUE: path does not exist}", status=400, mimetype='application/json')
    except:
        raise Exception("entered invalid wrong path or invalid input")



if __name__== "__main__":
    app.run(debug=False)