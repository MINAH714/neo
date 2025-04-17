OPTION (SKIP=1)
load data
infile 'myterror.csv'
insert into table myterror
fileds terminated by ','
trailing nullcol(
    event_id
    iyear,
    imonth,
    country,
    country_txt,
    region,
    region_txt,
    prostate,
    city,
    latitude,
    logitude
)