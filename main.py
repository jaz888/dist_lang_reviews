#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request
from flask import make_response
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
import random
import sys
import inspect
from sqlalchemy import desc






app = Flask(__name__)
Bootstrap(app)
manager = Manager(app)

db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://webadmin:webadmin123.@s2.zhujieao.com/dist'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True



class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    pid = db.Column(db.Integer)
    email = db.Column(db.String(200))
    name = db.Column(db.String(500))
    date = db.Column(db.DateTime)
    point = db.Column(db.Float)
    content = db.Column(db.Text)

    def serialize(self):
        return {
            'id': self.id,
            'pid': self.pid,
            'email': self.email,
            'name': self.name,
            'date': str(self.date),
            'point': self.point,
            'content': self.content
        }


class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    home_page = db.Column(db.String(500))
    developer = db.Column(db.String(500))
    developer_email = db.Column(db.String(500))
    developer_home_page = db.Column(db.String(200))
    problem = db.Column(db.String(500))
    algorithm = db.Column(db.String(200))
    language = db.Column(db.String(500))
    language_version = db.Column(db.String(500))
    release_date = db.Column(db.Date)
    release_version = db.Column(db.String(500))
    platforms = db.Column(db.String(500))
    lines_total = db.Column(db.String(500))
    lines_pure = db.Column(db.String(500))
    applications = db.Column(db.String(500))
    additional_information = db.Column(db.String(500))
    additional_attributes = db.Column(db.String(500))
    list_on_dist_algo_web_site = db.Column(db.String(500))
    submitter = db.Column(db.String(500))
    submitter_email = db.Column(db.String(500))
    score = db.Column(db.Float)

    def __repr__(self):
        return '<project % r>' % self.title
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'home_page': self.home_page,
            'developer': self.developer,
            'developer_email': self.developer_email,
            'developer_home_page': self.developer_home_page,
            'problem': self.problem,
            'algorithm': self.algorithm,
            'language': self.language,
            'language_version': self.language_version,
            'release_date': str(self.release_date),
            'release_version': self.release_version,
            'lines_total': self.lines_total,
            'lines_pure': self.lines_pure,
            'platforms': self.platforms,
            'applications': self.applications,
            'additional_information': self.additional_information,
            'additional_attributes': self.additional_attributes,
            'list_on_dist_algo_web_site': self.list_on_dist_algo_web_site,
            'submitter': self.submitter,
            'submitter_email': self.submitter_email,
            'score': self.score
        }


# class ProjectWrapper():
#     def __init__(self, projects):
#         self.projects = projects
#         self.languages = {}
#         for project in self.projects:
#             lans = project.language.split(',')
#             lans = map(lambda x:x.strip(), lans)
#             for lan in lans:
#                 if lan != '':
#                     if lan in self.languages:
#                         if project.algorithm in self.languages[lan]:
#                             self.languages[lan][project.algorithm].append(project)
#                         else:
#                             self.languages[lan][project.algorithm] = [project]
#                     else:
#                         self.languages[lan] = {project.algorithm:[project]}
class ProjectWrapper():
    def __init__(self, projects):
        self.projects = projects
        self.languages = {}
        for project in self.projects:
            lans = project.language.split(',')
            lans = map(lambda x:x.strip(), lans)
            for lan in lans:
                if lan != '':
                    if lan in self.languages:
                        self.languages[lan].append(project)
                    else:
                        self.languages[lan] = [project]

class ProjectWrapperTest():
    def __init__(self, projects):
        self.projects = projects
        self.languages = {}
        for project in self.projects:
            lans = project.problem.split(',')
            lans = map(lambda x:x.strip(), lans)
            for lan in lans:
                if lan != '':
                    if lan in self.languages:
                        self.languages[lan].append(project)
                    else:
                        self.languages[lan] = [project]


@app.route('/')
def index():
    query = {}
    query['groupBy'] = request.args.get('groupBy','')
    response = make_response('web')
    response.set_cookie('test_cookie_key','test_cookie_value')
    projects = Project.query.order_by(desc(Project.score)).all()
    pw = None
    if query['groupBy'] == 'problem':
        pw = ProjectWrapperTest(projects)
        return render_template('index_groupby_problem.html', projects=pw.languages)
    else:
        pw = ProjectWrapper(projects)
        return render_template('index.html', projects=pw.languages)

@app.route('/index', methods=['POST', 'GET'])
def index2():
    query = {}
    query['groupBy'] = request.args.get('groupBy','')
    response = make_response('web')
    response.set_cookie('test_cookie_key','test_cookie_value')
    projects = Project.query.order_by(desc(Project.score)).all()
    pw = None
    if query['groupBy'] == 'problem':
        pw = ProjectWrapperTest(projects)
        return render_template('index_groupby_problem.html', projects=pw.languages)
    else:
        pw = ProjectWrapper(projects)
        return render_template('index.html', projects=pw.languages)




@app.route('/test')
def test():
    response = make_response('web')
    response.set_cookie('test_cookie_key','test_cookie_value')
    projects = Project.query.order_by(desc(Project.score)).all()
    pw = ProjectWrapperTest(projects)

    #print projects[0].title

    return render_template('index.html', projects=pw.languages)

@app.route('/user/<name>')
def user(name = 'world'):
    return render_template('user.html', name=name)

@app.route('/advanced')
def advanced():
    return render_template('advanced.html')

@app.route('/API/search', methods=['POST', 'GET'])
def searchapi():
    query = {}
    query['title'] = request.args.get('title','')
    query['developer_email'] = request.args.get('developer_email','')
    query['additional_information'] = request.args.get('additional_information','')
    query['home_page'] = request.args.get('home_page','')
    query['language'] = request.args.get('language','')
    query['platforms'] = request.args.get('platform','')
    query['algorithm'] = request.args.get('algorithm','')
    query['problem'] = request.args.get('problem','')
    no_parameter = True
    lang = query['language']
    for q in query:
        if query[q] != '':
            no_parameter = False
            print q, query[q]
        query[q] = '%{0}%'.format(query[q])
    if no_parameter:
        return 'error'
    # tilte = '%{0}%'.format(tilte)
    # developer_email = '%{0}%'.format(developer_email)
    # additional_information = '%{0}%'.format(additional_information)
    # home_page = '%{0}%'.format(home_page)
    # language = '%{0}%'.format(language)
    # platforms = '%{0}%'.format(platforms)
    # algorithm = '%{0}%'.format(algorithm)
    # problem = '%{0}%'.format(problem)
    # print [ query[q] for q in query if query[q] != '%%' ]
    # print [ getattr(getattr(Project, q),'ilike')(q) for q in query if query[q] != '%%' ][0]
    # print Project.title.ilike('%Atomic%')

    qs = [ getattr(getattr(Project, k),'ilike')(query[k]) for k in query if query[k] != '%%' and query[k] != '']
    projects = Project.query.filter(  *qs ).order_by(desc(Project.score)).all()
        # Project.title.ilike(query['title']),\
        # Project.developer_email.ilike(query['developer_email']),\
        # Project.additional_information.ilike(query['additional_information']),\
        # Project.home_page.ilike(query['home_page']),\
        # Project.language.ilike(query['language']),\
        # Project.platforms.ilike(query['platforms']),\
        # Project.algorithm.ilike(query['algorithm']),\
        # Project.problem.ilike(query['problem'])
    # )

    return json.dumps([e.serialize() for e in projects])


@app.route('/search', methods=['POST', 'GET'])
def search():
    query = {}
    query['title'] = request.args.get('title','')
    query['developer_email'] = request.args.get('developer_email','')
    query['additional_information'] = request.args.get('additional_information','')
    query['home_page'] = request.args.get('home_page','')
    query['language'] = request.args.get('language','')
    query['platforms'] = request.args.get('platform','')
    query['algorithm'] = request.args.get('algorithm','')
    query['problem'] = request.args.get('problem','')
    no_parameter = True
    lang = query['language']
    for q in query:
        if query[q] != '':
            no_parameter = False
            print q, query[q]
        query[q] = '%{0}%'.format(query[q])
    if no_parameter:
        return 'error'
    # tilte = '%{0}%'.format(tilte)
    # developer_email = '%{0}%'.format(developer_email)
    # additional_information = '%{0}%'.format(additional_information)
    # home_page = '%{0}%'.format(home_page)
    # language = '%{0}%'.format(language)
    # platforms = '%{0}%'.format(platforms)
    # algorithm = '%{0}%'.format(algorithm)
    # problem = '%{0}%'.format(problem)
    # print [ query[q] for q in query if query[q] != '%%' ]
    # print [ getattr(getattr(Project, q),'ilike')(q) for q in query if query[q] != '%%' ][0]
    # print Project.title.ilike('%Atomic%')

    qs = [ getattr(getattr(Project, k),'ilike')(query[k]) for k in query if query[k] != '%%' and query[k] != '']
    projects = Project.query.filter(  *qs ).order_by(desc(Project.score)).all()
        # Project.title.ilike(query['title']),\
        # Project.developer_email.ilike(query['developer_email']),\
        # Project.additional_information.ilike(query['additional_information']),\
        # Project.home_page.ilike(query['home_page']),\
        # Project.language.ilike(query['language']),\
        # Project.platforms.ilike(query['platforms']),\
        # Project.algorithm.ilike(query['algorithm']),\
        # Project.problem.ilike(query['problem'])
    # )
    pw = ProjectWrapper(projects)
    search_by_lang = False
    for k in query:
        if query[k] != '%%' and query[k] != '' and k == 'language':
            search_by_lang = True

    if search_by_lang:
        for l in pw.languages:
            if str.lower(str(lang)) == str.lower(str(l)):
                lang = l
        return render_template('search.html', projects={lang: pw.languages[lang]})
    else:
        return render_template('search.html', projects=pw.languages)

@app.route('/API/comments/<pid>')
def getComments(pid):
    project = int(pid)
    comments = Comment.query.filter_by(pid=project).all()
    return json.dumps([e.serialize() for e in comments])

@app.route('/API/allProjects')
def allProjects():
    projects = Project.query.order_by(desc(Project.score)).all()
    return json.dumps([e.serialize() for e in projects])

@app.route('/API/project/<pid>')
def getProjects(pid):
    pid = int(pid)
    project = Project.query.filter_by(id=pid).first()
    return json.dumps(project.serialize())

@app.route('/submitComment/<pid>', methods=['POST', 'GET'])
def putComments(pid):
    project = int(pid)
    email = request.form.get('email','err')
    content = request.form.get('content','err')
    point = request.form.get('point','err')
    if email == 'err' or content == 'err' or point == 'err':
        return 'error'
    comment = Comment(pid=pid, email=email, content=content, point=point)
    db.session.add(comment)
    db.session.commit()
    return render_template('goBack.html')

def run_before_first_request():
    pass

def run_teardown_request(args):
    pass

if __name__ == '__main__':
    app.before_first_request(run_before_first_request)
    app.teardown_request(run_teardown_request)
    app.run(host= '0.0.0.0',port=5000, debug=True)
    #manager.run()
