WITH worksites_with_dentistry AS (
	SELECT DISTINCT WorksiteId
	FROM WorksiteDetail
	WHERE TypeId = 'DDS'
)
SELECT wa.WorksiteId,
        WorkHrsWeek,
		SUM(CASE WHEN WorksiteTitle = 'RDA' THEN 1 ELSE 0 END) as rdas,
		SUM(CASE WHEN WorksiteTitle = 'RDH' THEN 1 ELSE 0 END) as rdhs,
		SUM(CASE WHEN WorksiteTitle = 'DAT' THEN 1 ELSE 0 END) as dats
FROM WorksiteAuxilary wa
INNER JOIN worksites_with_dentistry wd
	ON wa.WorksiteId = wd.WorksiteId
GROUP BY wa.WorksiteId, WorkHrsWeek
