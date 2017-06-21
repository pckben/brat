#!/usr/bin/env python
# -*- Mode: Python; tab-width: 4; indent-tabs-mode: nil; coding: utf-8; -*-
# vim:set ft=python ts=4 sw=4 sts=4 autoindent:

from peewee import *
import data_config as config

db = MySQLDatabase(config.db, host=config.host, user=config.user, passwd=config.passwd)


class Collection(Model):
    path = CharField(unique=True)

    class Meta:
        database = db


class Entity(Model):
    collection = ForeignKeyField(Collection, related_name='entities')
    name = CharField(100)
    unused = BooleanField(default=False)

    class Meta:
        database = db


class Relation(Model):
    collection = ForeignKeyField(Collection, related_name='relations')
    name = CharField(100)
    role1 = CharField(100, default='Arg1')
    type1 = CharField(100)
    role2 = CharField(100, default='Arg2')
    type2 = CharField(100)
    reltype = CharField(100, default='')

    class Meta:
        database = db


class Event(Model):
    collection = ForeignKeyField(Collection, related_name='events')
    name = CharField(100)
    unused = BooleanField(default=False)

    class Meta:
        database = db


class EventRole(Model):
    event = ForeignKeyField(Event, related_name='roles')
    name = CharField(100)
    rtype = CharField(100)
    specs = CharField(10, default='')

    class Meta:
        database = db


class Attribute(Model):
    collection = ForeignKeyField(Collection, related_name='attributes')
    name = CharField(100)
    rtype = CharField(100)
    value = CharField(256)
    
    class Meta:
        database = db


def create_entity(collection, name):
    response = {}
    try:
        db.connect()
        collection = collection.rstrip('/')
        rs = list(Collection.filter(path=collection))
        if len(rs) == 0:
            c = Collection(path=collection)
            c.save()
        else:
            c = rs[0]
        en = Entity(collection=c, name=name)
        en.save()
    finally:
        db.close()
    return response

def setup():
    try:
        db.connect()
        db.create_tables([Collection, Entity, Relation, Event, EventRole, Attribute], safe=True)
    finally:
        db.close()

def drop():
    try:
        db.connect()
        db.drop_tables([Collection, Entity, Relation, Event, EventRole, Attribute], safe=True)
    finally:
        db.close()

def scaffold():
    try:
        db.connect()
        c = Collection(path=u'/mseg/testdb')
        c.save()
        en1 = Entity(collection=c, name=u'Product')
        en2 = Entity(collection=c, name=u'Action')
        en1.save()
        en2.save()
    finally:
        db.close()
