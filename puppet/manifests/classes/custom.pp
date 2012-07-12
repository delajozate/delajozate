# You can add custom puppet manifests for your app here.
class custom {

    file { "${PROJ_DIR}/delajozate/localsettings.py":
        source => "${PROJ_DIR}/delajozate/localsettings.py.example",
        owner => "vagrant",
        group => "vagrant",
        mode => 0644,
    }

    file { "/home/vagrant/rundz.sh":
        source => "$PROJ_DIR/puppet/files/rundz.sh",
        owner => "vagrant",
        group => "vagrant",
        mode => 0755,
    }

    exec { "/home/vagrant/.synced":
        creates => "/home/vagrant/.synced",
        command => "touch /home/vagrant/.synced",
        require => Exec["syncdb"],
    }

    exec { "syncdb":
        command => "python ${PROJ_DIR}/delajozate/manage.py syncdb --noinput",
        user    => "vagrant",
        require => File["${PROJ_DIR}/delajozate/localsettings.py"],
        before  => [
            Exec["/home/vagrant/.synced"],
            Exec["migrate"],
            ],
        unless  => "/usr/bin/test -f /home/vagrant/.synced",
        logoutput => "on_failure",
    }

    exec { "migrate":
        command => "python ${PROJ_DIR}/delajozate/manage.py migrate --noinput",
        user    => "vagrant",
        require => File["${PROJ_DIR}/delajozate/localsettings.py"],
        before  => [
            Exec["/home/vagrant/.synced"],
            Exec["loaddata"],
            ],
        unless  => "/usr/bin/test -f /home/vagrant/.synced",
        logoutput => "on_failure",
    }

    exec { "loaddata":
        command => "python ${PROJ_DIR}/delajozate/manage.py loaddata ${PROJ_DIR}/delajozate/fixtures/delajozate.json",
        user    => "vagrant",
        require => File["${PROJ_DIR}/delajozate/localsettings.py"],
        before  => Exec["/home/vagrant/.synced"],
        unless  => "/usr/bin/test -f /home/vagrant/.synced",
        logoutput => "on_failure",
    }

}
