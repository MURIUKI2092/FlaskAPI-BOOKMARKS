from flask import Blueprint,request
import validators
from flask.json import jsonify
from src.database import Bookmark,database
from flask_jwt_extended import get_jwt_identity,jwt_required

bookmarks= Blueprint("bookmarks",__name__,url_prefix="/api/v1/bookmarks")

#create different endpoints using one blueprint

@bookmarks.route('/',methods=['POST','GET'])
@jwt_required() #secure this route
def handle_bookmarks(): #bookmark function
    current_user= get_jwt_identity() #get the current user using the jwt 
    
    
    if request.method=='POST': #check the method which has been established by user

        body=request.get_json().get("body",'') # if it's post obtain the body and the url
        url=request.get_json().get('url','')

        if not validators.url(url):
            return jsonify({
                "error":"Enter a validated url"
            }),400

        if Bookmark.query.filter_by(url=url).first():
            return jsonify({
                "error":"The url already exist"
            }),409
            
            
        bookmark = Bookmark(url=url,body=body,user_id=current_user)
        database.session.add(bookmark)
        database.session.commit()
        
        return jsonify({
            'id':bookmark.id,
            'url':bookmark.url,
            'short_url':bookmark.short_url,
            'visit':bookmark.visits,
            'body':bookmark.body,
            'created_at':bookmark.created_at,
            'updated_at':bookmark.updated_at
        }),201
        
    else:
        #if method is get
        bookmarks=Bookmark.query.filter_by(user_id=current_user) #get the item you want to get using the id
        data =[]
        for item in bookmarks: #loop through the item and return an object
            data.append({
                'id':bookmark.id,
            'url':bookmark.url,
            'short_url':bookmark.short_url,
            'visit':bookmark.visits,
            'body':bookmark.body,
            'created_at':bookmark.created_at,
            'updated_at':bookmark.updated_at
                
            })
        return jsonify({'data':data}),200 #return the data


