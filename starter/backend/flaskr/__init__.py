import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from models import setup_db,User,NewsLetter,db

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)
  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
  app.run(host="0.0.0.0",port=5000)
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, PUT')
    return response 





  @app.route('/users',methods=['GET'])
  def user_profile():
        user=[owner.format() for owner in User.query.order_by(User.id).all()]
        return jsonify({
          'success':True,
          'user':user,
          'method':request.method
              
        },200)
  @app.route('/users',methods=['POST'])
  def insert_user():  
          try:
            body=request.get_json()
            username=body.get('username',None)     
            first_name=body.get('first_name',None)
            last_name=body.get('last_name',None)
            user=User(username=username,first_name=first_name,last_name=last_name)
            user.insert()
            return jsonify({
              'success':True,
              'user':user.format(),
              'method':request.method,
            },200)
          except:
            abort(422)


  

  @app.route('/users/<int:user_id>',methods=['GET'])
  def get_user_details(user_id):
        user=User.query.get(user_id)
        newsletter=[arg.description for arg in  db.session.query(NewsLetter).join(User).filter_by(id=user.id).all()]

        if not user:
              abort(400)
        return jsonify(
          {
            'success':True,
            'user':user.format(),
            'newsletter':newsletter

          }
        )                 
  @app.route('/users/<int:user_id>',methods=['DELETE'])
  def delete_user(user_id):
        try:
          user=User.query.get(user_id)
          if user == None:
                 abort(400)
          user.remove()
          return jsonify({
            'success':True,
            'method':request.method,
            'username':user.username
          },200)
        except:
          abort(422)



  @app.route('/users/<int:user_id>',methods=['PATCH'])
  def edit_user(user_id):
        try:
          user=User.query.get(user_id)
          body=request.get_json()
          if user is None :
                   abort(400)
        
          if 'username'.lower() in body :
                username=body.get('username',None)
          if 'first_name'.lower() in body: 
                first_name=body.get('first_name',None)
          if 'last_name'.lower() in body:
                last_name=body.get('last_name',None)
          user.username=username
          user.first_name=first_name
          user.last_name=last_name
          user.update()
        
          return jsonify({
            'success':True,
            'updated details':user.format(),
            'methods':request.method
          })
                
            
        except:
          abort(422)


  
  @app.route('/users/<int:user_id>',methods=['PUT'])
  def full_edit_user(user_id):
          try:
            body=request.get_json()
            user=User.query.get(user_id)
            username=body.get('username',None)     
            first_name=body.get('first_name',None)
            last_name=body.get('last_name',None)
            user.username=username
            user.first_name=first_name
            user.last_name=last_name
            user.update()
            return jsonify({
              'sxuccess':True,
              'user':user.format()
            })
          except:
            abort(422)

  @app.route('/users/<int:user_id>/newsletter',methods=['POST'])
  def user_newsletter(user_id):
      
          body=request.get_json()
          user_id=User.query.get(user_id)
          if user_id == None:
              abort(400)
          if request.method == 'POST':
            try:
              description=body.get('description',None)
              new=NewsLetter(description=description,owner=user_id)
              new.insert()
              return jsonify({
                'success':True,
                'newsletter':new.description,
                'posted by':new.owner.username

              })
            except:
               abort(422)



  @app.route('/newsletters',methods=['GET'])
  def get_newsletter():
        user=request.args.get('username')
        id=request.args.get('id')
        try:
          if user or id :  
            if user:         
              newsletter=[news.description for news in db.session.query(NewsLetter).join(User).filter_by(username=user).all()]
              usernames=[users.username for users in User.query.filter_by(username=user)]
            if id:
              newsletter=[[news.description ,news.id] for news in db.session.query(NewsLetter).join(User).filter_by(id=id).all()]
              usernames=[users.username for users in User.query.filter_by(id=id)]
           
          else:
            newsletter=[news.description for news in db.session.query(NewsLetter).join(User).all()]
            usernames=[news.username for news in db.session.query(User).join(NewsLetter).all()]

              
          return jsonify({
            'success':True,
            "newsletter":newsletter,
            'username':[usernames]
          
              })
        except:
         abort(422)


 
  @app.route('/newsletters/<string:username>',methods=['GET'])
  def get_user_newsletter(username):
        user=User.query.filter_by(username=username).first()
        if user:           
          newsletter=[news.description for news in db.session.query(NewsLetter).join(User).filter_by(username=user.username).all()]
          usernames=user.username
        
        return jsonify({
          'success':True,
          "newsletter":newsletter,
          'username':usernames
          
            })
  @app.route('/newsletters/<int:user_id>',methods=['GET'])
  def get_user_newsletter_id(user_id):
        user=User.query.get(user_id)
        if user:           
          newsletter=[news.description for news in db.session.query(NewsLetter).join(User).filter_by(id=user.id).all()]
          user_iden=user.id  
        return jsonify({
          'success':True,
          "newsletter":newsletter,
          'username':[user_iden,user.username]
          
            })

  @app.route('/newsletters/<int:news_id>',methods=['DELETE'])
  def delete_newsletter(news_id):
        newsletter=NewsLetter.query.get(news_id)
        if newsletter:
              newsletter.remove()
        else:
              abort(404)
        return jsonify({
          'success':True,
          "deleted":newsletter.format()
          })

            
              


        
              


  
  return app

    