#
#
#

create or replace table ipc3 as select pub,tri,count(*) as ct from ipc group by pub, tri;
create or replace index ind_ipc3_pub on ipc3 (pub);

create or replace table ipcprimary as
select a.pub, a.tri, a.ct
from ipc3 a
inner join (
    select pub, max(ct) ct
    from ipc3
    group by pub
) b on a.pub = b.pub and a.ct = b.ct

create or replace table dups as select pub from ipcprimary group by pub having count(*) > 1;
create or replace index ind_dups on dups (pub);

delete from ipcprimary where pub in (select pub from dups);

(select 'pub','tri' limit 0) union
(select pub,tri from ipcprimary
   into outfile 'D:/pubtri.csv'
   fields terminated by ','
   enclosed by '"' lines
   terminated by '\n');


# Create a ipc table at the group level
create or replace table ipcgroup as
    select pub,concat(sec,cla,subc,LPAD(grp,3,'0')) as ipc, count(*) as ct
        from ipc group by pub,concat(sec,cla,subc,grp);

