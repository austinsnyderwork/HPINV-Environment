
SELECT
    WorksiteId,
    TransactionId,
    PhoneArea + '-' + Phone AS full_phone,
    TypeId,
    CallDate
FROM WorksiteDetail