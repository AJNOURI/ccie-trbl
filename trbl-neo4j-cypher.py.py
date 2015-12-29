
# coding: utf-8

# In[10]:

#-------------------------------------------------------------------------------
# Name:        CCIE-TRBL
# Purpose:     CCIE Troubleshooting Neo4j graph db analysis
#
# Author:      AJ NOURI ajn.bin@gmail.com
#
# Created:     25/03/2014
# Copyright:   (c) AJ NOURI 2014
#-------------------------------------------------------------------------------
#!/usr/bin/env python
from py2neo import neo4j, cypher
import yaml
import logging
import sys

def main():

    credfile = 'localhost.neo4j'
    try:
        stream = open(credfile)
        cred = yaml.load(stream)
    except IOError:
        logging.error('File %s NOT found: ',credfile)
        sys.exit(0)        
    if cred:
        server = cypher.cypher_escape(cred['server'])
        directory = cypher.cypher_escape(cred['directory'])
        login = cypher.cypher_escape(cred['login'].strip('\r\n'))
        password = cypher.cypher_escape(cred['password'])
        serverurl = cred['server'] + cred['directory']
        serverurl = cypher.cypher_escape(serverurl)
        print serverurl, server,directory,login,password
        
    else:
        logging.error('Server credential file %s is empty: ',credfile)
        sys.exit(0)        
            
    print server, directory, login, password
    
    neo4j.authenticate(server, login, password)
   
    
    print serverurl
    graph = neo4j.Graph(serverurl)

    
    print(graph.neo4j_version)    
        
    """     TODO: 
    ### create 2 new nodes + relationship between them
    #query = neo4j.CypherQuery(db, "CREATE (a {name:{name_a}})-[ab:KNOWS]->(b {name:{name_b}})"
    #                              " RETURN a, b, ab")
    #print a,b,ab

     
    Check methods before change
        CheckNodebyid
        
        CheckNode for duplicate attribute before adding new one
        Checkrel
    explore methods
       List_NodesByLabel(s) one or more (feature & or technology)
       List_NodesByAttributes  one or more (name & or version)
       List_RelByAttribute  one or more (feature & or technology)
       
    Add new node: CreateNode_nRel
       mendatory attributes(name)
       default attributes(version=5, track=rs)
       check for duplicate attribute inside the rel
    Add new rel: CreateNode_nRel
       read direction as var
       mendatory attributes(name)
       default attributes(version=5, track=rs)
       check for duplicate attribute inside the rel
    
    #############
    
    #list nodes by label: technology, feature, issue
    MATCH (a:label)--(b)
    WITH collect(DISTINCT a) as f
    RETURN f
    """
        

    def Search_ByLabel(label):
        """ Search node by label """
        cypher = "MATCH (n:" + label + ") RETURN id(n)"
        try:
            print graph.cypher.execute(cypher)
            return True
        except Exception, e:
            print "Node Doesn't exist"
            return False

    def Search_ByAttr(attr, value):
        """ Search node by label """
        cypher = 'START n=node(*) WHERE n.'+ attr + '="' + value +'" RETURN id(n)'
        print cypher
        try:
            print graph.cypher.execute(cypher)
            return True
        except Exception, e:
            print "Node Doesn't exist"
            return False

    
    def CreateNode_nRel(n1label, n1attr,n1attrvalue, n2value):
        """ Search node by label """
        cypher = 'START n2=node('+ str(n2value) +') CREATE (n1:feature {' + n1attr +': "'+ n1attrvalue +'" }) CREATE (n1)-[:BELONGS_TO ]->(n2)'
        print cypher
        try:
            print graph.cypher.execute(cypher)
            return True
        except Exception, e:
            print "Node Doesn't exist"
            return False
       
        
    def Search_Nid(nid):
        """ Search for a node by id """
        cypher = 'START n=node('+ str(nid) +') WHERE (n)-[*]-() RETURN id(n)'
        print cypher
        try:
            print graph.cypher.execute(cypher)
            return True
        except Exception, e:
            print "Node Doesn't exist"
            return False

    def Search_PropValue(val):
        """ search for a node by id """
        try:
            query = neo4j.CypherQuery(db, "MATCH (n) WHERE n.nomo={value} RETURN id(n)")
            n = query.execute(value=val).data[0]
            print n
            return True
        except Exception, e:
            print "Node Doesn't exist"
            return False

    def Search_NodeDirRel(id,r):
        """ Search whether the node related by the given relationship """
        try:
            query = neo4j.CypherQuery(db, "START n=node({nid}) MATCH (n)-[:{rel}]-(b) RETURN n,b")
            n = query.execute(nid=id,rel=r).data[0]
            print n
            return True
        except Exception, e:
            print "Node Doesn't exist"
            return False

    """ 
    # methods
    ex: Search_ByLabel('technology')
    ex: Search_Nid(1300)
    ex: Search_ByAttr('track', 'rs')

    ex: Creating multiple features and add to a technology
    elist = ["HSRP",\
                 "VRRP",\
                 "Router Redundancy and Object Tracking",\
                 "Router ICMP Settings",\
                 "IP Event Dampening"]
    n2id = 129
    for entity in elist:
        CreateNode_nRel('feature','name',entity, n2id)
    """    

if __name__ == '__main__':
    main()

