create user replication_user@'%' identified by 'replication_user';

# administrative 
GRANT SUPER, REPLICATION CLIENT, REPLICATION SLAVE, RELOAD on *.* to replication_user@'%';

# to re-run queries
GRANT INSERT, UPDATE, DELETE, SELECT, CREATE, DROP on *.* to replication_user@'%';

