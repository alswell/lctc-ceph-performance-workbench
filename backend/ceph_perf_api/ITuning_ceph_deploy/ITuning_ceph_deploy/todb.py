import MySQLdb

class ToDB(object):
    def __init__(self):
        self.db = MySQLdb.connect("localhost","test","1234","fiotest" )

        self.cursor = self.db.cursor()

    def insert_tb_cluster(self, **kwargs):
        sql = "INSERT INTO ITuning_ceph_deploy_cluster(\
            name, public_network, cluster_network, \
            objectstore, journal_size, osdhosts, \
            clients, mons ) \
            VALUES ('{}', '{}', '{}', \
            '{}', '{}', '{}',  '{}', '{}' )".format(
                kwargs['name'],
                kwargs['public_network'],
                kwargs['cluster_network'],
                kwargs['objectstore'],
                kwargs['journal_size'],
                kwargs['osdhosts'],
                kwargs['clients'],
                kwargs['mons'],
            )
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            print sql
            self.db.rollback()

    def update_cluster(self, clusterid, **kwargs):
        for key, value in kwargs.items():
            sql = "UPDATE ITuning_ceph_deploy_cluster \
                SET {} = '{}' WHERE id = '{}'".format(key, value, clusterid)
            try:
                self.cursor.execute(sql)
                self.db.commit()
            except:
                print sql
                self.db.rollback()

