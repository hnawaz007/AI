-- View: public.product_sales

-- DROP VIEW public.product_sales;

CREATE OR REPLACE VIEW public.product_sales
 AS
 SELECT p.product_name AS product,
    p.product_subcategory_name AS productsubcategory,
    p.product_category_name AS productcategory,
    p.daystomanufacture,
    p.productnumber,
    c.customername,
    t.countryregioncode AS countrycode,
    t.territory_group AS region,
    t.countryregioncode AS "group",
    f.salesordernumber AS ordernumber,
    f.salesordernumber,
    f.orderdate,
    to_char(f.orderdate, 'YYYY'::text) AS year,
    to_char(f.orderdate, 'YYYY-Mon'::text) AS year_month,
    dd.date_day AS duedate,
    sd.date_day AS shipdate,
    f.orderqty AS orderquantity,
    f.unitprice,
    f.totaldiscount AS discountamount,
    f.salesamount,
    f.taxamt AS taxamount
   FROM sales f
     LEFT JOIN territory t ON f.territory_key = t.territory_key
     LEFT JOIN product p ON f.product_key = p.product_key
     LEFT JOIN customer c ON c.customer_key = f.customer_key
     LEFT JOIN date dd ON dd.date_key = f.duedate_key
     LEFT JOIN date sd ON sd.date_key = f.shipdate_key;

ALTER TABLE public.product_sales
    OWNER TO postgres;

