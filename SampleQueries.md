# Sample Queries

Here are some sample queries to get you started with progressively more complex queries.

## Show me a Property
 
```
GRAPH RealEstateGraph
MATCH (p:Property) 
RETURN p.address, p.bedrooms, p.bathrooms limit 10
```

## Show me a Property using SQL
Data is stored as SQL tables making it easy to read and write with SQL too

```
SELECT * from Property limit 10;
```

## Show me a Property in my price range
 
```
GRAPH RealEstateGraph
MATCH (p:Property)  where p.price < 500000
RETURN p.address, p.price, p.bedrooms, p.bathrooms 
ORDER BY p.price limit 10
```

## Show me some sales

```
GRAPH RealEstateGraph
MATCH (p:Property)-[h:HAS_OWNER]->(o:Owner)
RETURN p.address,h.create_date, o.name limit 10
```

## Properties Sold After 1/1/23


```
GRAPH RealEstateGraph
MATCH (p:Property)-[h:HAS_OWNER]->(o:Owner)
WHERE h.create_date > '2023-01-01'
RETURN p.address,h.create_date, o.name limit 10
```

## Top 10 Average price bedroom counts per Zip Code


```
GRAPH RealEstateGraph
MATCH (p:Property)-[x:IN_COUNTY]->(c:County)
RETURN AVG(p.bedrooms) AS beds, AVG(p.price) AS price, c.postcode
GROUP BY c.postcode
ORDER BY price DESC
LIMIT 10
```

## What is the spread on credit ratings for jumbo loan holders

```
GRAPH RealEstateGraph
MATCH (p:Property)-[:HAS_OWNER]->(o:Owner)-[:HAS_CREDIT_REPORT]->(c:CreditReport)
WHERE p.price >= 766550
RETURN MIN(c.score) AS min_score, MAX(c.score) AS max_score, AVG(c.score) AS avg_score, c.bureau
GROUP BY c.bureau
```

## Who paid the most property tax in 2023?

Here we get to a query that would be very long in SQL and very slow

```
GRAPH RealEstateGraph
MATCH (o:Owner)<-[h:HAS_OWNER]-(p:Property)-[x:IN_COUNTY]->(c:County)
WHERE h.create_date <= '2023-21-31'
RETURN o.name AS OwnerName, ROUND((p.price*c.tax_rate/100),2) AS TaxPaid, c.name AS County 
ORDER BY TaxPaid DESC LIMIT 10
```

## Find me 100 of Owner id 7's people up to thrice removed

Basically a waste of time to try this using SQL, but super easy in Graph

```
GRAPH RealEstateGraph
MATCH (o:Owner{id: 7})-[e:KNOWS]->{1,3}(q:Owner)
WHERE o != q
RETURN o.name AS SRC, q.name AS DEST,  ARRAY_LENGTH(e) AS path_length
ORDER BY path_length  LIMIT 100
```

## This query needs to get fixed but as a general idea of the power of influence

```
GRAPH RealEstateGraph
MATCH (o:Owner)-[e:KNOWS]->{0,2}(q:Owner)<-[:HAS_OWNER]-(p:Property)
WHERE o != q
RETURN o.name AS SRC, sum(p.price) AS assets
ORDER BY assets DESC  LIMIT 25
```

# Hybrid Queries

Use Vector Search, Full Text Search and Graph to show the power of multi-model queries.

## Vector Queries

### Find me five closest properties to this description


```
SELECT id, COSINE_DISTANCE(
  embedding, 
  (SELECT embeddings.values
    FROM ML.PREDICT(  MODEL DescriptionModel,
      (SELECT "A Tudor House with charm and hardwood floors that needs some remodeling" AS content)
    )
  )
) AS distance from Embed
ORDER BY distance LIMIT 5;
```

### Use a vector query as the entry point for more information

```
GRAPH RealEstateGraph
  MATCH (p:Property)-[h:HAS_OWNER]->(o:Owner)
  WHERE p.id IN (
  SELECT id FROM(
   SELECT id, COSINE_DISTANCE(
     embedding,
      (SELECT embeddings.values
        FROM ML.PREDICT(  MODEL DescriptionModel,
          (SELECT "A Tudor House with charm and hardwood floors that needs some remodeling" AS content)
        )
      )
    )
   AS distance FROM Embed ORDER BY distance LIMIT 5
  )
) RETURN p.id, p.price, o.name AS owner, p.bathrooms, p.bedrooms 
```

## Search Queries

### Look over the company descriptions

```
SELECT id, description FROM Company LIMIT 10;
```

### Do a search for some tokens

**Note you will need to find the tokens in the simulated data**

```
SELECT id FROM Company WHERE SEARCH(description_Tokens, 'CHANGE_ME OR CHANGE_ME')
```

### Use the tokens to search

```
GRAPH RealEstateGraph
MATCH (o:Owner)-[EMPLOYED_BY]->(c:Company)
WHERE c.id IN (SELECT id From Company WHERE SEARCH(description_Tokens, 'CHANGE_ME OR CHANGE_ME'))
RETURN o.name AS owner, c.name AS company, c.id AS companyid, c.description LIMIT 10
```

### Sum up the prices by search entry point

```
GRAPH RealEstateGraph
MATCH (p:Property)-[h:HAS_OWNER]->(o:Owner)-[EMPLOYED_BY]->(c:Company)
WHERE c.id IN (SELECT id From Company WHERE SEARCH(description_Tokens, 'CHANGE_ME OR CHANGE_ME'))
RETURN SUM(p.price) AS total_value, c.name AS company 
GROUP BY company
```
