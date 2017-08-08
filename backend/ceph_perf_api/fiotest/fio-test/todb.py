import MySQLdb



class ToDB(object):
    def __init__(self):
        self.db = MySQLdb.connect("localhost","test","1234","fiotest" )

        self.cursor = self.db.cursor()

    def insert_tb_result(self, **kwargs):
        sql = "INSERT INTO fiotest_result(case_name, time, suite_time, \
            blocksize, iodepth, numberjob, imagenum, \
            clientnum, iops, readwrite, lat ) \
            VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', \
            '{}', '{}', '{}' )".format(
                kwargs['case_name'],
                kwargs['time'],
                kwargs['suite_time'],
                kwargs['blocksize'],
                kwargs['iodepth'],
                kwargs['numberjob'],
                kwargs['imagenum'],
                kwargs['clientnum'],
                kwargs['iops'],
                kwargs['readwrite'],
                kwargs['lat']
        )
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()

    def insert_tb_sarmemdata(self, casename, node, **kwargs):
        sql = "SELECT * FROM fiotest_result \
            WHERE case_name = '{}'".format(casename)
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            for row in results:
                caseid = row[0]
        except:
            self.db.rollback()
        sql = "INSERT INTO fiotest_sarmem(caseid_id, node, time, \
            kbmemfree, kbmemused, memused, kbbuffers, kbcached, \
            kbcommit, commit, kbactive, kbinact, kbdirty ) \
            VALUES ('{}', '{}', '{}', \
            '{}', '{}', '{}', '{}', '{}', \
            '{}', '{}', '{}', '{}', '{}')".format(
                caseid,
                node,
                kwargs['time'],
                kwargs['kbmemfree'],
                kwargs['kbmemused'],
                kwargs['memused'],
                kwargs['kbbuffers'],
                kwargs['kbcached'],
                kwargs['kbcommit'],
                kwargs['commit'],
                kwargs['kbactive'],
                kwargs['kbinact'],
                kwargs['kbdirty'],
        )

        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()

    def insert_tb_sarcpudata(self, casename, node, **kwargs):
        sql = "SELECT * FROM fiotest_result \
            WHERE case_name = '{}'".format(casename)
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            for row in results:
                caseid = row[0]
        except:
            self.db.rollback()
        sql = "INSERT INTO fiotest_sarcpu(caseid_id, node, \
            time, usr, nice, sys, iowait, steal, \
            irq, soft, guest, gnice, idle ) \
            VALUES ('{}', '{}', '{}', '{}', '{}', '{}', \
            '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
                caseid,
                node,
                kwargs['time'],
                kwargs['usr'],
                kwargs['nice'],
                kwargs['sys'],
                kwargs['iowait'],
                kwargs['steal'],
                kwargs['irq'],
                kwargs['soft'],
                kwargs['guest'],
                kwargs['gnice'],
                kwargs['idle'],
        )
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()

    def insert_tb_sarnicdata(self, casename, node, network, **kwargs):
        sql = "SELECT * FROM fiotest_result \
            WHERE case_name = '{}'".format(casename)
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            for row in results:
                caseid = row[0]
        except:
            self.db.rollback()
        sql = "INSERT INTO fiotest_sarnic(caseid_id, node, network, time, \
            rxpcks, txpcks, rxkBs, txkBs, rxcmps, txcmps, rxmcsts ) \
            VALUES ('{}', '{}', '{}', '{}', \
            '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
                caseid,
                node,
                network,
                kwargs['time'],
                kwargs['rxpcks'],
                kwargs['txpcks'],
                kwargs['rxkBs'],
                kwargs['txkBs'],
                kwargs['rxcmps'],
                kwargs['txcmps'],
                kwargs['rxmcsts'],
            )

        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()

    def insert_tb_iostatdata(self, casename, node, osdnum, disk_name, **kwargs):
        sql = "SELECT * FROM fiotest_result \
            WHERE case_name = '{}'".format(casename)
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            for row in results:
                caseid = row[0]
        except:
            self.db.rollback()
        sql = "INSERT INTO fiotest_iostat(caseid_id, node, osdnum, diskname, \
            time, wrqms, avgrqsz, r_await, await, ws, avgqusz, \
            svctm, rMBs, wMBs, rrqms, rs, util, w_await, tps ) \
            VALUES ('{}', '{}', '{}', '{}', \
            '{}', '{}', '{}', '{}', '{}', '{}', '{}', \
            '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
                caseid,
                node,
                osdnum,
                disk_name,
                kwargs['time'],
                kwargs['wrqms'],
                kwargs['avgrqsz'],
                kwargs['r_await'],
                kwargs['await'],
                kwargs['ws'],
                kwargs['avgqusz'],
                kwargs['svctm'],
                kwargs['rMBs'],
                kwargs['wMBs'],
                kwargs['rrqms'],
                kwargs['rs'],
                kwargs['util'],
                kwargs['w_await'],
                kwargs['tps'],
            )
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()

    def insert_tb_cephconfigdata(self, casename, node, osd, **kwargs):
        sql = "SELECT * FROM fiotest_result \
            WHERE case_name = '{}'".format(casename)
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            for row in results:
                caseid = row[0]
        except:
            self.db.rollback()
        sql = "INSERT INTO fiotest_cephconfig(caseid_id, node, osd, \
            max_open_files, filestore_expected_throughput_bytes, \
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
            osd_op_num_shards, osd_op_threads, osd_op_thread_timeout, \
            osd_op_thread_suicide_timeout, osd_recovery_thread_timeout, \
            osd_recovery_thread_suicide_timeout, osd_disk_threads, \
            osd_map_cache_size, osd_recovery_threads, osd_recovery_op_priority, \
            osd_recovery_max_active, osd_max_backfills, osd_scrub_begin_hour, \
            osd_scrub_end_hour, osd_scrub_sleep, osd_scrub_load_threshold, \
            osd_scrub_chunk_max, osd_scrub_chunk_min, \
            osd_journal_size, journal_max_write_bytes, \
            journal_max_write_entries, journal_throttle_high_multiple, \
            journal_throttle_max_multiple, \
            objecter_inflight_ops, objecter_inflight_op_bytes ) \
            VALUES ('{}', '{}', '{}', \
            '{}', '{}', '{}','{}', '{}', \
            '{}', '{}', '{}','{}', '{}', \
            '{}', '{}', '{}','{}', '{}', '{}', '{}', '{}', \
            '{}', '{}', '{}', '{}', '{}', '{}', \
            '{}', '{}', '{}', '{}', '{}', \
            '{}', '{}', '{}', '{}', '{}', \
            '{}', '{}', '{}', '{}', '{}', \
            '{}', '{}', '{}', '{}', '{}', \
            '{}', '{}', '{}', '{}', \
            '{}', '{}', '{}', '{}', '{}', \
            '{}', '{}')".format(
                caseid,
                node,
                osd,
                kwargs['max_open_files'],
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
                kwargs['osd_op_threads'],
                kwargs['osd_op_thread_timeout'],
                kwargs['osd_op_thread_suicide_timeout'],
                kwargs['osd_recovery_thread_timeout'],
                kwargs['osd_recovery_thread_suicide_timeout'],
                kwargs['osd_disk_threads'],
                kwargs['osd_map_cache_size'],
                kwargs['osd_recovery_threads'],
                kwargs['osd_recovery_op_priority'],
                kwargs['osd_recovery_max_active'],
                kwargs['osd_max_backfills'],
                kwargs['osd_scrub_begin_hour'],
                kwargs['osd_scrub_end_hour'],
                kwargs['osd_scrub_sleep'],
                kwargs['osd_scrub_load_threshold'],
                kwargs['osd_scrub_chunk_max'],
                kwargs['osd_scrub_chunk_min'],
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
            self.db.rollback()

    def insert_tb_perfdumpdata(self, casename, node, log_osd, **kwargs):
        sql = "SELECT * FROM fiotest_result \
            WHERE case_name = '{}'".format(casename)
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            for row in results:
                caseid = row[0]
        except:
            self.db.rollback()
        sql = "INSERT INTO fiotest_perfdump(caseid_id, node, osd, \
            filestore_queue_transaction_latency_avg_avgcount, \
            filestore_queue_transaction_latency_avg_sum, \
            filestore_bytes, \
            filestore_ops, \
            filestore_op_queue_bytes, \
            filestore_journal_bytes, \
            filestore_journal_latency_avgcount, \
            filestore_journal_latency_sum, \
            filestore_journal_wr, \
            filestore_journal_wr_bytes_avgcount, \
            filestore_journal_wr_bytes_sum, \
            filestore_journal_ops, \
            filestore_apply_latency_avgcount, \
            filestore_apply_latency_sum, \
            filestore_commitcycle, \
            filestore_commitcycle_latency_avgcount, \
            filestore_commitcycle_sum, \
            leveldb_leveldb_submit_sync_latency_avgcount, \
            leveldb_leveldb_submit_sync_latency_sum, \
            leveldb_leveldb_get_latency_avgcount, \
            leveldb_leveldb_get_latency_sum, \
            leveldb_leveldb_submit_latency_avgcount, \
            leveldb_leveldb_submit_latency_sum, \
            osd_op, \
            osd_op_wip, \
            osd_op_in_bytes, \
            osd_op_out_bytes, \
            osd_op_latency_avgcount, \
            osd_op_latency_sum, \
            osd_op_process_latency_avgcount, \
            osd_op_process_latency_sum, \
            osd_op_prepare_latency_avgcount, \
            osd_op_prepare_latency_sum, \
            osd_op_r_latency_avgcount, \
            osd_op_r_latency_sum, \
            osd_op_r_process_latency_avgcount, \
            osd_op_r_process_latency_sum, \
            osd_op_r, \
            osd_op_r_out_bytes, \
            osd_op_w, \
            osd_op_w_in_bytes, \
            osd_op_w_latency_avgcount, \
            osd_op_w_latency_sum, \
            osd_op_w_process_latency_avgcount, \
            osd_op_w_process_latency_sum, \
            osd_op_w_rlat_avgcount, \
            osd_op_w_rlat_sum, \
            osd_stat_bytes_used, \
            osd_stat_bytes_avail, \
            osd_buffer_bytes, \
            recoverystate_perf_primary_latency_avgcount, \
            recoverystate_perf_primary_latency_sum, \
            recoverystate_perf_peering_latency_avgcount, \
            recoverystate_perf_peering_latency_sum, \
            recoverystate_perf_backfilling_latency_avgcount, \
            recoverystate_perf_backfilling_latency_sum ) \
            VALUES ('{}', '{}', '{}', \
            '{}', '{}', '{}', '{}', '{}', \
            '{}', '{}', '{}', '{}', '{}', \
            '{}', '{}', '{}', '{}', '{}', \
            '{}', '{}', '{}', '{}', '{}', \
            '{}', '{}', '{}', '{}', '{}', \
            '{}', '{}', '{}', '{}', '{}', \
            '{}', '{}', '{}', '{}', '{}', \
            '{}', '{}', '{}', '{}', '{}', \
            '{}', '{}', '{}', '{}', '{}', \
            '{}', '{}', '{}', '{}', '{}', \
            '{}', '{}', '{}', '{}', '{}', \
            '{}')".format(
                caseid,
                node,
                log_osd,
                kwargs['filestore']['queue_transaction_latency_avg']['avgcount'],
                kwargs['filestore']['queue_transaction_latency_avg']['sum'],
                kwargs['filestore']['bytes'],
                kwargs['filestore']['ops'],
                kwargs['filestore']['op_queue_bytes'],
                kwargs['filestore']['journal_bytes'],
                kwargs['filestore']['journal_latency']['avgcount'],
                kwargs['filestore']['journal_latency']['sum'],
                kwargs['filestore']['journal_wr'],
                kwargs['filestore']['journal_wr_bytes']['avgcount'],
                kwargs['filestore']['journal_wr_bytes']['sum'],
                kwargs['filestore']['journal_ops'],
                kwargs['filestore']['apply_latency']['avgcount'],
                kwargs['filestore']['apply_latency']['sum'],
                kwargs['filestore']['commitcycle'],
                kwargs['filestore']['commitcycle_latency']['avgcount'],
                kwargs['filestore']['commitcycle_latency']['sum'],
                kwargs['leveldb']['leveldb_submit_sync_latency']['avgcount'],
                kwargs['leveldb']['leveldb_submit_sync_latency']['sum'],
                kwargs['leveldb']['leveldb_get_latency']['avgcount'],
                kwargs['leveldb']['leveldb_get_latency']['sum'],
                kwargs['leveldb']['leveldb_submit_latency']['avgcount'],
                kwargs['leveldb']['leveldb_submit_latency']['sum'],
                kwargs['osd']['op'],
                kwargs['osd']['op_wip'],
                kwargs['osd']['op_in_bytes'],
                kwargs['osd']['op_out_bytes'],
                kwargs['osd']['op_latency']['avgcount'],
                kwargs['osd']['op_latency']['sum'],
                kwargs['osd']['op_process_latency']['avgcount'],
                kwargs['osd']['op_process_latency']['sum'],
                kwargs['osd']['op_prepare_latency']['avgcount'],
                kwargs['osd']['op_prepare_latency']['sum'],
                kwargs['osd']['op_r_latency']['avgcount'],
                kwargs['osd']['op_r_latency']['sum'],
                kwargs['osd']['op_r_process_latency']['avgcount'],
                kwargs['osd']['op_r_process_latency']['sum'],
                kwargs['osd']['op_r'],
                kwargs['osd']['op_r_out_bytes'],
                kwargs['osd']['op_w'],
                kwargs['osd']['op_w_in_bytes'],
                kwargs['osd']['op_w_latency']['avgcount'],
                kwargs['osd']['op_w_latency']['sum'],
                kwargs['osd']['op_w_process_latency']['avgcount'],
                kwargs['osd']['op_w_process_latency']['sum'],
                kwargs['osd']['op_w_rlat']['avgcount'],
                kwargs['osd']['op_w_rlat']['sum'],
                kwargs['osd']['stat_bytes_used'],
                kwargs['osd']['stat_bytes_avail'],
                kwargs['osd']['buffer_bytes'],
                kwargs['recoverystate_perf']['primary_latency']['avgcount'],
                kwargs['recoverystate_perf']['primary_latency']['sum'],
                kwargs['recoverystate_perf']['peering_latency']['avgcount'],
                kwargs['recoverystate_perf']['peering_latency']['sum'],
                kwargs['recoverystate_perf']['backfilling_latency']['avgcount'],
                kwargs['recoverystate_perf']['backfilling_latency']['sum'],
            )
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()

    def insert_tb_cephstatusdata(self, casename, time, **kwargs):
        sql = "SELECT * FROM fiotest_result \
            WHERE case_name = '{}'".format(casename)
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            for row in results:
                caseid = row[0]
        except:
            self.db.rollback()
        sql = "INSERT INTO fiotest_cephstatus(caseid_id, time, \
            health_overall_status, \
            health_summary, \
            health_detail, \
            fsid, \
            monmap_mons, \
            osdmap_osdmap_num_osds, \
            osdmap_osdmap_num_up_osds, \
            osdmap_osdmap_num_in_osds, \
            pgmap_pgs_by_state, \
            pgmap_num_pgs, \
            pgmap_data_bytes, \
            pgmap_bytes_used, \
            pgmap_bytes_avail, \
            pgmap_bytes_total ) \
            VALUES ('{}', '{}', \
            '{}', '{}', '{}', '{}', '{}', \
            '{}', '{}', '{}', '{}', '{}', \
            '{}', '{}', '{}', '{}' )".format(
                caseid,
                time,
                kwargs['health']['overall_status'],
                kwargs['health']['summary'],
                kwargs['health']['detail'],
                kwargs['fsid'],
                kwargs['monmap']['mons'],
                kwargs['osdmap']['osdmap']['num_osds'],
                kwargs['osdmap']['osdmap']['num_up_osds'],
                kwargs['osdmap']['osdmap']['num_in_osds'],
                kwargs['pgmap']['pgs_by_state'],
                kwargs['pgmap']['num_pgs'],
                kwargs['pgmap']['data_bytes'],
                kwargs['pgmap']['bytes_used'],
                kwargs['pgmap']['bytes_avail'],
                kwargs['pgmap']['bytes_total'],
            )
        print sql
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()


    def create_tb_result(self):
        sql = """CREATE TABLE fiotest_result (
            id  int auto_increment primary key,
            case_name  CHAR(100) NOT NULL,
            time datetime,
            blocksize  CHAR(20),
            iodepth  int,
            numberjob  int,
            imagenum  int,
            clientnum  int,
            iops  int,
            readwrite  CHAR(20),
            lat  float ) ENGINE=MyISAM"""
        self.cursor.execute(sql)

    def create_tb_sarcpudata(self):
        sql = """CREATE TABLE fiotest_sarcpu (
            id int auto_increment primary key,
            caseid_id int not null,
            node  char(20),
            time  datetime,
            usr float,
            nice float,
            sys float,
            iowait float,
            steal float,
            irq float,
            soft float,
            guest float,
            gnice float,
            idle float,
            foreign key(caseid_id) references fiotest_result(id) ) ENGINE=MyISAM"""
        self.cursor.execute(sql)

    def create_tb_sarmemdata(self):
        sql = """CREATE TABLE fiotest_sarmem (
            id int auto_increment primary key,
            caseid_id int not null,
            node  char(20),
            time  datetime,
            kbmemfree int,
            kbmemused int,
            memused float,
            kbbuffers int,
            kbcached int,
            kbcommit int,
            commit float,
            kbactive int,
            kbinact int,
            kbdirty int,
            foreign key(caseid_id) references fiotest_result(id) ) ENGINE=MyISAM"""
        self.cursor.execute(sql)


    def create_tb_sarnicdata(self):
        sql = """CREATE TABLE fiotest_sarnic (
            id int auto_increment primary key,
            caseid_id int not null,
            node  char(20),
            network char(20),
            time datetime,
            rxpcks float,
            txpcks float,
            rxkBs float,
            txkBs float,
            rxcmps float,
            txcmps float,
            rxmcsts float,
            foreign key(caseid_id) references fiotest_result(id) ) ENGINE=MyISAM"""
        self.cursor.execute(sql)

    def create_tb_iostatdata(self):
        sql = """CREATE TABLE fiotest_iostat (
            id int auto_increment primary key,
            caseid_id int not null,
            node char(20),
            osdnum char(20),
            diskname char(20),
            time datetime,
            wrqms float,
            avgrqsz float,
            r_await float,
            await float,
            ws float,
            avgqusz float,
            svctm float,
            rMBs float,
            wMBs float,
            rrqms float,
            rs float,
            tps float,
            util float,
            w_await float,
            foreign key(caseid_id) references fiotest_result(id) ) ENGINE=MyISAM"""
        self.cursor.execute(sql)

    def create_tb_cephconfigfilestonedata(self):
        sql = """CREATE TABLE CEPHCONFIGFSDATA (
            id int auto_increment primary key,
            caseid_id int not null,
            node  char(20),
            osd  char(20),
            max_open_files char(20),
            filestore_expected_throughput_bytes char(20),
            filestore_expected_throughput_ops char(20),
            filestore_max_sync_interval char(20),
            filestore_min_sync_interval char(20),
            filestore_queue_max_bytes char(20),
            filestore_queue_max_ops char(20),
            filestore_queue_high_delay_multiple char(20),
            filestore_queue_max_delay_multiple char(20),
            filestore_ondisk_finisher_threads char(20),
            filestore_apply_finisher_threads char(20),
            filestore_commit_timeout char(20),
            filestore_fd_cache_shards char(20),
            filestore_fd_cache_size char(20),
            filestore_wbthrottle_enable char(20),
            filestore_op_threads char(20),
            filestore_op_thread_timeout char(20),
            filestore_op_thread_suicide_timeout char(20),
            foreign key(caseid_id) references fiotest_result(id) ) ENGINE=MyISAM"""
        self.cursor.execute(sql)

    def create_tb_cephconfigjournaldata(self):
        sql = """CREATE TABLE CEPHCONFIGJDATA (
            id int auto_increment primary key,
            caseid_id int not null,
            node  char(20),
            osd  char(20),
            osd_journal_size char(20),
            journal_max_write_bytes char(20),
            journal_max_write_entries char(20),
            journal_throttle_high_multiple char(20),
            journal_throttle_max_multiple char(20),
            foreign key(caseid_id) references fiotest_result(id) ) ENGINE=MyISAM"""
        self.cursor.execute(sql)

    def create_tb_cephconfigrbddata(self):
        sql = """CREATE TABLE CEPHCONFIGRBDDATA (
            id int auto_increment primary key,
            caseid_id int not null,
            node  char(20),
            osd  char(20),
            rbd_cache char(20),
            rbd_cache_size char(20),
            rbd_cache_target_dirty char(20),
            rbd_cache_max_dirty char(20),
            rbd_cache_max_dirty_age char(20),
            rbd_cache_writethrough_until_flush char(20),
            foreign key(caseid_id) references fiotest_result(id) ) ENGINE=MyISAM"""
        self.cursor.execute(sql)

    def create_tb_cephconfigosddata(self):
        sql = """CREATE TABLE CEPHCONFIGOSDATA (
            id int auto_increment primary key,
            caseid_id int not null,
            node  char(20),
            osd  char(20),
            osd_max_write_size char(20),
            osd_num_op_tracker_shard char(20),
            osd_client_message_size_cap char(20),
            osd_client_message_cap char(20),
            osd_deep_scrub_stride char(20),
            osd_op_num_threads_per_shard char(20),
            osd_op_num_shards char(20),
            osd_op_threads char(20),
            osd_op_thread_timeout char(20),
            osd_op_thread_suicide_timeout char(20),
            osd_recovery_thread_timeout char(20),
            osd_recovery_thread_suicide_timeout char(20),
            osd_disk_threads char(20),
            osd_map_cache_size char(20),
            osd_recovery_threads char(20),
            osd_recovery_op_priority char(20),
            osd_recovery_max_active char(20),
            osd_max_backfills char(20),
            osd_scrub_begin_hour char(20),
            osd_scrub_end_hour char(20),
            osd_scrub_sleep char(20),
            osd_scrub_load_threshold char(20),
            osd_scrub_chunk_max char(20),
            osd_scrub_chunk_min char(20),
            foreign key(caseid_id) references fiotest_result(id) ) ENGINE=MyISAM"""
        self.cursor.execute(sql)

    def create_tb_cephconfigclientdata(self):
        sql = """CREATE TABLE CEPHCONFIGCDATA (
            id int auto_increment primary key,
            caseid_id int not null,
            node  char(20),
            osd  char(20),
            objecter_inflight_ops char(20),
            objecter_inflight_op_bytes char(20),
            foreign key(caseid_id) references fiotest_result(id) ) ENGINE=MyISAM"""
        self.cursor.execute(sql)

    def create_tb_perfdumpdata(self):
        sql = """CREATE TABLE PERFDUMPDATA (
            id int auto_increment primary key,
            caseid_id int not null,
            node  char(20),
            filestore__queue_transaction_latency_avg char(20),
            filestore__bytes char(20),
            foreign key(caseid_id) references fiotest_result(id) ) ENGINE=MyISAM"""
        self.cursor.execute(sql)



    def close_db(self):
        self.db.close()

    def cleanup_db(self):
        self.cursor.execute("DROP TABLE IF EXISTS PERFDUMPDATA")
        self.cursor.execute("DROP TABLE IF EXISTS CEPHCONFIGFSDATA")
        self.cursor.execute("DROP TABLE IF EXISTS CEPHCONFIGJDATA")
        self.cursor.execute("DROP TABLE IF EXISTS CEPHCONFIGRBDDATA")
        self.cursor.execute("DROP TABLE IF EXISTS CEPHCONFIGOSDATA")
        self.cursor.execute("DROP TABLE IF EXISTS CEPHCONFIGCDATA")
        self.cursor.execute("DROP TABLE IF EXISTS fiotest_iostat")
        self.cursor.execute("DROP TABLE IF EXISTS fiotest_sarcpu")
        self.cursor.execute("DROP TABLE IF EXISTS fiotest_sarmem")
        self.cursor.execute("DROP TABLE IF EXISTS fiotest_sarnic")
        self.cursor.execute("DROP TABLE IF EXISTS fiotest_result")


def main():

    todb = ToDB()
    todb.cleanup_db()
    todb.create_tb_result()
    todb.create_tb_sarcpudata()
    todb.create_tb_sarmemdata()
    todb.create_tb_iostatdata()
    todb.create_tb_sarnicdata()
    todb.create_tb_cephconfigfilestonedata()
    todb.create_tb_cephconfigjournaldata()
    todb.create_tb_cephconfigrbddata()
    todb.create_tb_cephconfigosddata()
    todb.create_tb_cephconfigclientdata()
    todb.create_tb_perfdumpdata()
    todb.close_db()

if __name__ == '__main__':
    main()

