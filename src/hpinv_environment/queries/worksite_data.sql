
SELECT
    w.WorksiteId,
    w.WorksiteName,
    w.ParentWorksite,
    COALESCE(wd.TransactionId, 'I') as TransactionId,
    wd.PhoneArea + '-' + wd.Phone AS Phone,
    w.city,
    w.Address1,
    w.Address2,
    w.zip,
    w.state,
    wd.CallDate
FROM Worksite w
LEFT JOIN WorksiteDetail wd
    ON w.WorksiteId = wd.WorksiteId