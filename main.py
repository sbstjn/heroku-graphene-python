#!/usr/bin/env python3

import graphene
import requests
import os
import json

from sanic import Sanic
from sanic_graphql import GraphQLView

class Person (graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    age = graphene.Int()

class Query(graphene.ObjectType):
    person = graphene.Field(Person, id=graphene.ID(required=True))
    people = graphene.List(Person)

    def resolve_person(self, info, id):
        r = requests.get("https://to23rx1sik.execute-api.us-west-1.amazonaws.com/Prod/person/" + id)
        data = json.loads(r.content)
        person = data['data']

        return Person(id=person['id'], name=person['name'], age=person['age'])
    def resolve_people(self, info):
        r = requests.get("https://to23rx1sik.execute-api.us-west-1.amazonaws.com/Prod/people")
        data = json.loads(r.content)

        people = []
        for person in data['data']:
          people.append(Person(id=person['id'], name=person['name'], age=person['age']))

        return people

schema = graphene.Schema(query=Query, types=[Person])

app = Sanic()

app.add_route(GraphQLView.as_view(schema=schema, graphiql=True), '/graphql')

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=os.environ.get('PORT') or 8000
    )