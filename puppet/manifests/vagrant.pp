#
# Playdoh puppet magic for dev boxes
#
import "classes/*.pp"

$PROJ_DIR = "/home/vagrant/project"

# You can make these less generic if you like, but these are box-specific
# so it's not required.
$DB_NAME = "delajozate"
$DB_USER = "vagrant"

Exec {
    path => "/usr/local/bin:/usr/bin:/usr/sbin:/sbin:/bin",
}

class dev {
    class {
        init: before => Class[postgresql];
        postgresql: before  => Class[python];
        python: before => Class[nginx];
        nginx: before => Class[custom];
        memcached: ;
        custom: ;
    }
}

include dev
