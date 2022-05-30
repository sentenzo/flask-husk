CREATE TABLE IF NOT EXISTS Counters (
    id int, 
    count int,
    CONSTRAINT counters_pk UNIQUE(id)
)
;
INSERT INTO Counters
VALUES (1, 0)
ON CONFLICT DO NOTHING
;
