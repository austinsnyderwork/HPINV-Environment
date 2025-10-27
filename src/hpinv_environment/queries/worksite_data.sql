
SELECT
    w.WorksiteId,
    w.WorksiteName,
    w.ParentWorksite as ParentWorksiteId,
    wd.TransactionId AS DetailActive,
    wd.PhoneArea + '-' + wd.Phone as Phone,
    w.City,
    w.Address1,
    w.Address2,
    w.Zip,
    w.State,
    wd.CallDate
FROM Worksite w
LEFT JOIN WorksiteDetail wd
    ON w.WorksiteId = wd.WorksiteId
