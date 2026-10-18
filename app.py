import os
from flask import Flask,request,jsonify
from flask_cors import CORS
app=Flask(__name__);CORS(app)
songs={1:{'id':1,'title':'Yellow','artist':'Coldplay','lyrics':'Look at the stars'},2:{'id':2,'title':'Believer','artist':'Imagine Dragons','lyrics':'First things first'}}
collection=None
if os.getenv('MONGO_URI'):
    try:
        from pymongo import MongoClient
        collection=MongoClient(os.getenv('MONGO_URI'),serverSelectionTimeoutMS=2000).capstone.songs
        collection.database.client.admin.command('ping')
    except Exception as exc:
        print('MongoDB unavailable, using in-memory data:',exc);collection=None
def all_data():
    if collection is None: return list(songs.values())
    return list(collection.find({}, {'_id':0}))
@app.get('/health')
def health():return jsonify(status='OK')
@app.get('/songs')
def list_songs():return jsonify(all_data())
@app.get('/song')
def song_query():
    song_id=request.args.get('id',type=int)
    if song_id is None:return jsonify(all_data())
    item=next((x for x in all_data() if x['id']==song_id),None)
    return (jsonify(item),200) if item else (jsonify(error='Not found'),404)
@app.get('/song/<int:song_id>')
def get_song(song_id):
    item=next((x for x in all_data() if x['id']==song_id),None)
    return (jsonify(item),200) if item else (jsonify(error='Not found'),404)
@app.post('/song')
def add_song():
    data=request.get_json(silent=True) or {}
    if not data.get('title') or not data.get('artist'):return jsonify(error='title and artist required'),400
    entries=all_data();data['id']=max((s['id'] for s in entries),default=0)+1
    if collection is None:songs[data['id']]=data
    else:collection.insert_one(dict(data))
    return jsonify(data),201
@app.put('/song/<int:song_id>')
def put_song(song_id):
    data=request.get_json(silent=True) or {}
    if not any(x['id']==song_id for x in all_data()):return jsonify(error='Not found'),404
    updates={k:v for k,v in data.items() if k in ('title','artist','lyrics')}
    if collection is None:songs[song_id].update(updates);result=songs[song_id]
    else:collection.update_one({'id':song_id},{'$set':updates});result=next(x for x in all_data() if x['id']==song_id)
    return jsonify(result)
@app.put('/song')
def put_query():return put_song(request.args.get('id',type=int) or 1)
@app.delete('/song/<int:song_id>')
def delete_song(song_id):
    if not any(x['id']==song_id for x in all_data()):return jsonify(error='Not found'),404
    if collection is None:del songs[song_id]
    else:collection.delete_one({'id':song_id})
    return jsonify(message='Deleted')
@app.delete('/song')
def delete_query():return delete_song(request.args.get('id',type=int) or 1)
if __name__=='__main__':app.run(host='0.0.0.0',port=5002)
