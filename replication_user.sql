create user replication_user@'%' identified by 'replication_user';
GRANT SUPER, REPLICATION CLIENT on *.* to replication_user@'%';

