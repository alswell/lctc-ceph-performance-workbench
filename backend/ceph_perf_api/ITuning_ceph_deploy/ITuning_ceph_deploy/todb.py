import json
import re
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

    def insert_cephconfig(self, clusterid, node, osd, config):
        sql = "INSERT INTO ITuning_ceph_deploy_defaultcephconfig(clusterid_id, node, osd, total ) \
            VALUES ('{}', '{}', '{}', '{}')".format(
                clusterid,
                node,
                osd,
                config,
            )
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            print sql
            self.db.rollback()


    def _insert_cephconfig(self, clusterid, node, osd, **kwargs):
        sql = "INSERT INTO ITuning_ceph_deploy_defaultcephconfig(clusterid_id, node, osd, total, \
            filestore_expected_throughput_bytes, \
            filestore_expected_throughput_ops, filestore_max_sync_interval, \
            filestore_min_sync_interval, filestore_queue_max_bytes, \
            filestore_queue_max_ops, filestore_queue_high_delay_multiple, \
            filestore_queue_max_delay_multiple, filestore_ondisk_finisher_threads, \
            filestore_apply_finisher_threads, filestore_commit_timeout, \
            filestore_fd_cache_shards, filestore_fd_cache_size, \
            filestore_wbthrottle_enable, filestore_op_threads, \
            filestore_op_thread_timeout, filestore_op_thread_suicide_timeout, \
            rbd_cache, rbd_cache_size, rbd_cache_target_dirty, \
            rbd_cache_max_dirty, rbd_cache_max_dirty_age, rbd_cache_writethrough_until_flush, \
            osd_max_write_size, osd_num_op_tracker_shard, \
            osd_client_message_size_cap, osd_client_message_cap, \
            osd_deep_scrub_stride, osd_op_num_threads_per_shard, \
            osd_op_num_shards, osd_op_thread_timeout, \
            osd_op_thread_suicide_timeout, osd_recovery_thread_timeout, \
            osd_recovery_thread_suicide_timeout, osd_disk_threads, \
            osd_map_cache_size, osd_recovery_op_priority, \
            osd_recovery_max_active, osd_max_backfills, osd_scrub_begin_hour, \
            osd_scrub_end_hour, osd_scrub_sleep, osd_scrub_load_threshold, \
            osd_scrub_chunk_max, osd_scrub_chunk_min, osd_objectstore,\
            osd_journal_size, journal_max_write_bytes, \
            journal_max_write_entries, journal_throttle_high_multiple, \
            journal_throttle_max_multiple, \
            objecter_inflight_ops, objecter_inflight_op_bytes ) \
            VALUES ('{}', '{}', '{}', '{}', \
            '{}', '{}','{}', '{}', \
            '{}', '{}', '{}','{}', '{}', \
            '{}', '{}', '{}','{}', '{}', '{}', '{}', '{}', \
            '{}', '{}', '{}', '{}', '{}', '{}', \
            '{}', '{}', '{}', '{}', '{}', \
            '{}', '{}', '{}', '{}', '{}', \
            '{}', '{}', '{}', '{}', '{}', \
            '{}', '{}', '{}', '{}', \
            '{}', '{}', '{}', '{}', \
            '{}', '{}', '{}', '{}', '{}', \
            '{}', '{}')".format(
                clusterid,
                node,
                osd,
                re.sub('\\\\', '\\\\\\\\', json.dumps(kwargs)),
                #kwargs['max_open_files'],
                kwargs['filestore_expected_throughput_bytes'],
                kwargs['filestore_expected_throughput_ops'],
                kwargs['filestore_max_sync_interval'],
                kwargs['filestore_min_sync_interval'],
                kwargs['filestore_queue_max_bytes'],
                kwargs['filestore_queue_max_ops'],
                kwargs['filestore_queue_high_delay_multiple'],
                kwargs['filestore_queue_max_delay_multiple'],
                kwargs['filestore_ondisk_finisher_threads'],
                kwargs['filestore_apply_finisher_threads'],
                kwargs['filestore_commit_timeout'],
                kwargs['filestore_fd_cache_shards'],
                kwargs['filestore_fd_cache_size'],
                kwargs['filestore_wbthrottle_enable'],
                kwargs['filestore_op_threads'],
                kwargs['filestore_op_thread_timeout'],
                kwargs['filestore_op_thread_suicide_timeout'],
                kwargs['rbd_cache'],
                kwargs['rbd_cache_size'],
                kwargs['rbd_cache_target_dirty'],
                kwargs['rbd_cache_max_dirty'],
                kwargs['rbd_cache_max_dirty_age'],
                kwargs['rbd_cache_writethrough_until_flush'],
                kwargs['osd_max_write_size'],
                kwargs['osd_num_op_tracker_shard'],
                kwargs['osd_client_message_size_cap'],
                kwargs['osd_client_message_cap'],
                kwargs['osd_deep_scrub_stride'],
                kwargs['osd_op_num_threads_per_shard'],
                kwargs['osd_op_num_shards'],
                #kwargs['osd_op_threads'],
                kwargs['osd_op_thread_timeout'],
                kwargs['osd_op_thread_suicide_timeout'],
                kwargs['osd_recovery_thread_timeout'],
                kwargs['osd_recovery_thread_suicide_timeout'],
                kwargs['osd_disk_threads'],
                kwargs['osd_map_cache_size'],
                #kwargs['osd_recovery_threads'],
                kwargs['osd_recovery_op_priority'],
                kwargs['osd_recovery_max_active'],
                kwargs['osd_max_backfills'],
                kwargs['osd_scrub_begin_hour'],
                kwargs['osd_scrub_end_hour'],
                kwargs['osd_scrub_sleep'],
                kwargs['osd_scrub_load_threshold'],
                kwargs['osd_scrub_chunk_max'],
                kwargs['osd_scrub_chunk_min'],
                kwargs['osd_objectstore'],
                kwargs['osd_journal_size'],
                kwargs['journal_max_write_bytes'],
                kwargs['journal_max_write_entries'],
                kwargs['journal_throttle_high_multiple'],
                kwargs['journal_throttle_max_multiple'],
                kwargs['objecter_inflight_ops'],
                kwargs['objecter_inflight_op_bytes'],
            )
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            print sql
            self.db.rollback()

    def query_config(self, clusterid):
        columns_sql = "SHOW COLUMNS FROM ITuning_ceph_deploy_defaultcephconfig"
        sql = "SELECT * FROM ITuning_ceph_deploy_defaultcephconfig \
            WHERE clusterid_id = '{}'".format(clusterid)
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
        except:
            print "Error: unable to fecth data"

        try:
            self.cursor.execute(columns_sql)
            columns = self.cursor.fetchall()
        except:
            print "Error: unable to fecth data"


        return results, columns

