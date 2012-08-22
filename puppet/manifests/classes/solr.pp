#
class solr {
    $hostarch = "dpkg-architecture | grep DEB_HOST_ARCH= | cut -d= -f2"

    exec { "wget-solr":
        command => "/usr/bin/wget http://www.kiberpipa.org/~hruske/odhd/delajozate-solr.tar.bz2 -O /home/vagrant/delajozate-solr.tar.bz2",
        creates => "/home/vagrant/delajozate-solr.tar.bz2";
    }

    exec { "extract-solr":
        command => "tar jxvf /home/vagrant/delajozate-solr.tar.bz2",
        creates => "/home/vagrant/solr",
        cwd => "/home/vagrant",
        require => Exec["wget-solr"];
    }

    exec { "symlink-lemmatizer":
        command => "ln -s /home/vagrant/solr/cores/libLemmatizer-`${hostarch}`.so /home/vagrant/solr/cores/libLemmatizer.so",
        cwd => "/home/vagrant/solr/cores",
        require => Exec["extract-solr"],
        creates => "/home/vagrant/solr/cores/libLemmatizer.so";
    }

    package { "openjdk-6-jre-headless":
        ensure => installed;
    }

    package { "screen":
        ensure => installed;
    }

    file { "/etc/init.d/solr":
        source => "$PROJ_DIR/puppet/files/solr",
        owner => "root", group => "root", mode => 0755,
        require => [
            Package['openjdk-6-jre-headless'],
            Exec['extract-solr']
        ],
        before => Service["solr"];
    }


    service { "solr":
        ensure => running,
        enable => true,
        require => File['/etc/init.d/solr'];
    }
}
