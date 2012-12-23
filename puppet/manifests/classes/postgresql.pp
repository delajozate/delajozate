# Get postgresql up and running
class postgresql {
    $userexists = "psql --tuples-only -c 'SELECT rolname FROM pg_catalog.pg_roles;' | grep '^ ${DB_USER}$'"
    $user_owns_zero_databases = "psql --tuples-only --no-align -c \"SELECT COUNT(*) FROM pg_catalog.pg_database JOIN pg_authid ON pg_catalog.pg_database.datdba = pg_authid.oid WHERE rolname = '${DB_USER}';\" | grep -e '^0$'"

    package {
        [ "postgresql-9.1", "postgresql-client-9.1"]:
        ensure => installed;
    }

    exec { "create-db-user":
        command => "createuser -d -S -R ${DB_USER}",
        user    => 'postgres',
        unless  => $userexists,
        require => Package["postgresql-9.1"];
    }

    exec { "create-db":
        command => "createdb -E utf-8 -T template0 -O ${DB_USER} ${DB_NAME}",
        user    => 'postgres',
        onlyif  => "$userexists && $user_owns_zero_databases",
        require => Exec["create-db-user"];
    }

    service { "postgresql":
        ensure => running,
        enable => true,
        require => Package['postgresql-9.1'];
    }
}
