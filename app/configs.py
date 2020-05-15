class DefaultConfig(object):
    DEBUG = True
    SECURITY_KEY = "gAL&W~[:vT8S[Otdlc7OZ%09{d^,Y8dB:NwT`gLcas70~GFk3MjrJPFH)zelH-E"
    CASSANDRA_HOSTS = ['127.0.0.1']
    CASSANDRA_KEYSPACE = 'notifications'
    TIME_ZONE = "UTC"


class Dev(DefaultConfig):
    ENV = "development"
    TESTING = True


class Prod(DefaultConfig):
    ENV = "production"
    TESTING = False
