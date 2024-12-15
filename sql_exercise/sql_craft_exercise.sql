-- Check that customer ID is unique
select
    id,
    count(*)
from customer_dimension
group by id
having count(*) > 1;

-- Check that date ID is unique
select
    id,
    count(*)
from date_dimension
group by id
having count(*) > 1;

-- Solution
create table customer_email_metrics
as
with
get_country_email_totals
AS
(
    select
  		country,
  		sum(esf.email_opens_cnt) as total_emails_sent_per_country
  	from emails_sent_fact esf
  	inner join customer_dimension cd
  		on esf.customer_id = cd.id
 	group by country
)
, get_metrics
AS
(
	select
		dd.year,
    	dd.month_name,
    	dd.month as month_number,
    	cd.country,
    	max(esf.email_opens_cnt) as max_emails_opened,
    	sum(distinct esf.customer_id) as total_customers
	from emails_sent_fact esf
	inner join date_dimension dd
		on esf.date_id = dd.id
	inner join customer_dimension cd
		on esf.customer_id = cd.id
	group by
		dd.year,
    	dd.month_name,
    	dd.month,
    	cd.country
	order By
		dd.year,
    	dd.month,
    	cd.country
)
select
	gm.year,
    gm.month_name,
    gm.month_number,
    gm.country,
    gm.max_emails_opened,
    gm.total_customers,
    gcet.total_emails_sent_per_country
from get_metrics gm
inner join get_country_email_totals gcet
	on gm.country = gcet.country


-- Validate
-- 304320
select sum(email_opens_cnt) from emails_sent_fact

-- 304320
with
dist_country_total
AS
(
	select
		distinct
  		country,
  		total_emails_sent_per_country as email_opens_cnt
	from customer_email_metrics
)
select sum(email_opens_cnt) from dist_country_total
