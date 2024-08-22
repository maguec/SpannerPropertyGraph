GRAPH PropertyGraph
MATCH (p:Property) 
RETURN p.address, p.bedrooms, p.bathrooms limit 10


GRAPH PropertyGraph
MATCH (p:Property)-[h:HAS_OWNER]->(o:Owner)
RETURN p.address,h.create_date, o.name limit 10

GRAPH PropertyGraph
MATCH (p:Property)-[h:HAS_OWNER]->(o:Owner)
WHERE h.create_date > '2023-01-01'
RETURN p.address,h.create_date, o.name limit 10


GRAPH PropertyGraph
MATCH (p:Property)-[x:IN_COUNTY]->(c:County)
RETURN AVG(p.bedrooms) as beds, c.postcode
ORDER By beds DESC
LIMIT 10
