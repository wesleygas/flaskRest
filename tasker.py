from flask import Flask
from flask_restful import Api, Resource,reqparse

app = Flask(__name__)
api = Api(app)


tasks = dict()
tasks["0"] = {"title":'aeaeae',"body": 'efefefefefe'}
idCount = 0

class TaskListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, required=True,
                                   help='No task title provided',
                                   location='json')
        self.reqparse.add_argument('body', type=str, default="",
                                   location='json')
    
    def get(self):
        global tasks
        return tasks,200

    def post(self):
        global idCount, tasks
        args = self.reqparse.parse_args()
        idCount += 1
        tasks[str(idCount)] = {"title":args['title'],"body":args['body']}
        return tasks[str(idCount)], 200


class TaskAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('id', type = str, location = 'json')
        self.reqparse.add_argument('title', type = str, location = 'json')
        self.reqparse.add_argument('body', type = str, location = 'json')

    def get(self, id):
        global idCount, tasks
        if(id <= idCount):
            task = tasks[str(id)]
            if(task != None):
                return task,200
        return "No task {} not found.".format(id),200 

    def put(self, id):
        global tasks, idCount
        args = self.reqparse.parse_args()
        if(id <= idCount):
            task = tasks[str(id)]
            if(task != None):
                title = args['title']
                if(title != None and len(title) > 0): task['title'] =  title
                task['body'] = args['body']
                tasks[str(id)] = task
                return task,200                    
        return "No task {} not found.".format(id),200 

    def delete(self, id):
        global tasks, idCount
        if(id <= idCount):
            task = tasks[str(id)]
            if(task != None):
                tasks[str(id)] = None
            return '',200
        return '',200

api.add_resource(TaskListAPI, '/tasks', endpoint = 'tasks')
api.add_resource(TaskAPI, '/tasks/<int:id>', endpoint = 'task')

if __name__ == '__main__':
    app.run(debug=True)