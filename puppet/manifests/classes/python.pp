# Install python and compiled modules for project
class python {
    case $operatingsystem {
        ubuntu: {
            package {
                ["python2.6-dev", "python2.6", "python-pip", "python-psycopg2", "libxml2-dev", "libxslt1-dev", "python-lxml"]:
                    ensure => installed;
            }

            exec { "pip-install-compiled":
                command => "pip install -r $PROJ_DIR/requirements.txt",
                require => Package['python-pip']
            }
        }
    }
}
