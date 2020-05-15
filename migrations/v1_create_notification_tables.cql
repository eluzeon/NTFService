/* Cassandra migration for keyspace notifications.
   Version 1 - 2020-05-13T19:34:12.113794+00:00

   create notification tables */
create table notification (
    id uuid primary key,
    message text,
    img_url text
) with default_time_to_live = 1209600; -- 14 days


create table user_notification (
    nid uuid,
    user_id int,
    lesson_id int,
    show_after timestamp,
    read boolean,
    primary key (user_id, show_after)
) with default_time_to_live = 1209600; -- 14 days
