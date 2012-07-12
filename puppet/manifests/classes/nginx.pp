# Red Hat, CentOS, and Fedora think Apache is the only web server
# ever, so we have to use a different package on CentOS than Ubuntu.
class nginx {
    case $operatingsystem {
        ubuntu: {
            package { "nginx":
                ensure => present,
                before => File['/etc/nginx/sites-enabled/hrcek.conf'];
            }

            file { "/etc/nginx/sites-enabled/hrcek.conf":
                source => "$PROJ_DIR/puppet/files/nginx-hrcek.conf",
                owner => "root", group => "root", mode => 0644,
                require => [
                    Package['nginx']
                ];
            }

            service { "nginx":
                ensure => running,
                enable => true,
                require => [
                    Package['nginx'],
                    File['/etc/nginx/sites-enabled/hrcek.conf']
                ];
            }

        }
    }
}
