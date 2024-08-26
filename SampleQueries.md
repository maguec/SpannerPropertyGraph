## Show me a Property
 
```
GRAPH PropertyGraph
MATCH (p:Property) 
RETURN p.address, p.bedrooms, p.bathrooms limit 10
```


## Show me a Property in my price range
 
```
GRAPH PropertyGraph
MATCH (p:Property)  where p.price < 500000
RETURN p.address, p.price, p.bedrooms, p.bathrooms 
ORDER BY p.price limit 10
```

## Show me some sales

```
GRAPH PropertyGraph
MATCH (p:Property)-[h:HAS_OWNER]->(o:Owner)
RETURN p.address,h.create_date, o.name limit 10
```

## Properties Sold After 1/1/23


```
GRAPH PropertyGraph
MATCH (p:Property)-[h:HAS_OWNER]->(o:Owner)
WHERE h.create_date > '2023-01-01'
RETURN p.address,h.create_date, o.name limit 10
```

## Top 10 Average price bedroom counts per Zip Code


```
GRAPH PropertyGraph
MATCH (p:Property)-[x:IN_COUNTY]->(c:County)
RETURN AVG(p.bedrooms) as beds, AVG(p.price) as price, c.postcode
GROUP by c.postcode
ORDER By price DESC
LIMIT 10
```

## What is the spread on credit ratings for jumbo loan holders

```
GRAPH PropertyGraph
MATCH (p:Property)-[:HAS_OWNER]->(o:Owner)-[:HAS_CREDIT_REPORT]->(c:CreditReport)
WHERE p.price >= 766550
RETURN MIN(c.score) as min_score, MAX(c.score) as max_score, AVG(c.score) as avg_score, c.bureau
GROUP BY c.bureau
```

## Who paid the most property tax in 2023?

```
GRAPH PropertyGraph
MATCH (o:Owner)<-[h:HAS_OWNER]-(p:Property)-[x:IN_COUNTY]->(c:County)
WHERE h.create_date <= '2023-21-31'
RETURN o.name as OwnerName, ROUND((p.price*c.tax_rate/100),2) as TaxPaid, c.name as County 
ORDER BY TaxPaid DESC LIMIT 10
```

## Find me 100 of Owner id 7's people up to thrice removed

```
GRAPH PropertyGraph
MATCH (o:Owner{id: 7})-[e:KNOWS]->{1,3}(q:Owner)
WHERE o != q
RETURN o.name as SRC, q.name as DEST,  ARRAY_LENGTH(e) AS path_length
ORDER BY path_length  LIMIT 100
```

## This query needs to get fixed but as a general idea of the power of influence

```
GRAPH PropertyGraph
MATCH (o:Owner)-[e:KNOWS]->{0,2}(q:Owner)<-[:HAS_OWNER]-(p:Property)
WHERE o != q
RETURN o.name as SRC, sum(p.price) as assets
ORDER BY assets DESC  LIMIT 25
```

## [Hybrid Query Example](https://cloud.google.com/spanner/docs/reference/standard-sql/graph-sql-queries) 
## Find me all properties with a description that matches

```
SELECT embeddings.values
FROM ML.PREDICT(
  MODEL EmbeddingsModel,
  (SELECT "A Tudor House with charm and hardwood floors that needs some remodeling" as content)
);
```

