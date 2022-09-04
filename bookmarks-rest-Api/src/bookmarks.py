import json
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
        #set the pagination configuration
        page = request.args.get('page',1,type=int) #pagination flask
        per_page= request.args.get('per_page',5, type=int)
        bookmarks=Bookmark.query.filter_by(user_id=current_user).paginate(page=page,per_page=per_page) 
        #get the item you want to get using the id
        
        data =[]
        for bookmark in bookmarks.items: #loop through the item and return an object
            data.append({
                'id':bookmark.id,
            'url':bookmark.url,
            'short_url':bookmark.short_url,
            'visit':bookmark.visits,
            'body':bookmark.body,
            'created_at':bookmark.created_at,
            'updated_at':bookmark.updated_at
                
            })
            #overwrite the paginate
            meta={
                "page":bookmarks.page,
                'pages':bookmarks.pages,
                'total_count':bookmarks.total,
                'prev':bookmarks.prev_num,
                'next_page':bookmarks.next_num,
                'has_next':bookmarks.has_next,
                'has_prev':bookmarks.has_prev,
                
            }
        return jsonify({'data':data,'meta':meta}),200 #return the data

#get a single bookmark from the  db
@bookmarks.get("/<int:id>")
@jwt_required()#protect the rout
def get_single_bookmark(id):
    #get current user
    current_user = get_jwt_identity()
    single_bookmark = Bookmark.query.filter_by(user_id=current_user,id=id).first() #send a query to the db to get the single page
    if not single_bookmark: # if not found then return the message
        return jsonify({
            "message":"Item not found"
        }),404
    return jsonify({ # if found return a json object
        'id':single_bookmark.id,
            'url':single_bookmark.url,
            'short_url':single_bookmark.short_url,
            'visit':single_bookmark.visits,
            'body':single_bookmark.body,
            'created_at':single_bookmark.created_at,
            'updated_at':single_bookmark.updated_at
    }),200
#update a single item in the database   
@bookmarks.put("/<int:id>")
@bookmarks.patch("/<int:id>") #handles both patch and put updates
@jwt_required() #protect the route
def update_single_bookmark(id):
    current_user =get_jwt_identity()# get the current user
    try:
        single_bookmark = Bookmark.query.filter_by(user_id=current_user,id=id).first()#look for a single bookmark in the database
        if not single_bookmark:
            return jsonify({
                "message":"Item not found" #if there is no bookmark found return this
            }),404
        body= request.get_json().get("body","") # if a single bookmark exist get the body
        url=request.get_json().get("url","")#get a url also from the single bookmark
        
        if not validators.url(url): #validate the url to ensure it's valid
            return jsonify({
                "error":"Enter a valid url"
            }),400
            
        single_bookmark.url=url
        single_bookmark.body=body
        database.session.commit()
        return jsonify({
            'id':single_bookmark.id,
            'url':single_bookmark.url,
            'short_url':single_bookmark.short_url,
            'visit':single_bookmark.visits,
            'body':single_bookmark.body,
            'created_at':single_bookmark.created_at,
            'updated_at':single_bookmark.updated_at
        }),200
        
        
    except:
        return jsonify({
            "message":"There was an error "
        })
    
#deleting an item
@bookmarks.delete("/<int:id>") #The route for deletion
@jwt_required()#secure routes
def delete_single_bookmark(id):
    try:
        current_user=get_jwt_identity() #check who the user is 
    
        single_bookmark = Bookmark.query.filter_by(user_id=current_user,id=id).first() #chek if the user created it
        if not single_bookmark:
            return jsonify({
                "message":"item not found"
            }),404
        database.session.delete(single_bookmark)
        database.session.commit()
        
        return jsonify({}),204
        
    except:
        return jsonify({
            "message":"an error ocurred"
        })
