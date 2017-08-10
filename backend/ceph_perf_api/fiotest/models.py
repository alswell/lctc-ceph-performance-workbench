# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
class Result(models.Model):
    id = models.AutoField(primary_key=True)
    jobid = models.ForeignKey("Jobs",to_field='id', null=True)
    case_name = models.CharField(max_length=100)
    ceph_config = models.CharField(max_length=100, default='default')
    time = models.DateTimeField(null=True)
    blocksize = models.CharField(max_length=20, null=True)
    iodepth = models.IntegerField(null=True)
    numberjob = models.IntegerField(null=True)
    imagenum = models.IntegerField(null=True)
    clientnum = models.IntegerField(null=True)
    iops = models.IntegerField(null=True)
    readwrite = models.CharField(max_length=20, null=True)
    lat = models.FloatField(null=True)
    bw = models.FloatField(null=True)
    status = models.CharField(max_length=20, null=True)


class SarCPU(models.Model):
    id = models.AutoField(primary_key=True)
    caseid = models.ForeignKey("Result",to_field='id')
    node = models.CharField(max_length=20)
    time = models.DateTimeField(null=True)
    usr = models.FloatField(null=True)
    nice = models.FloatField(null=True)
    sys = models.FloatField(null=True)
    iowait = models.FloatField(null=True)
    steal = models.FloatField(null=True)
    irq = models.FloatField(null=True)
    soft = models.FloatField(null=True)
    guest = models.FloatField(null=True)
    gnice = models.FloatField(null=True)
    idle = models.FloatField(null=True)

class SarMem(models.Model):
    id = models.AutoField(primary_key=True)
    caseid = models.ForeignKey("Result",to_field='id')
    node = models.CharField(max_length=20)
    time = models.DateTimeField(null=True)
    kbmemfree = models.IntegerField(null=True)
    kbmemused = models.IntegerField(null=True)
    memused = models.FloatField(null=True)
    kbbuffers = models.IntegerField(null=True)
    kbcached = models.IntegerField(null=True)
    kbcommit = models.IntegerField(null=True)
    commit = models.FloatField(null=True)
    kbactive = models.IntegerField(null=True)
    kbinact = models.IntegerField(null=True)
    kbdirty = models.IntegerField(null=True)

class SarNic(models.Model):
    id = models.AutoField(primary_key=True)
    caseid = models.ForeignKey("Result",to_field='id')
    node = models.CharField(max_length=20)
    network = models.CharField(max_length=20, null=True)
    time = models.DateTimeField(null=True)
    rxpcks = models.FloatField(null=True)
    txpcks = models.FloatField(null=True)
    rxkBs = models.FloatField(null=True)
    txkBs = models.FloatField(null=True)
    rxcmps = models.FloatField(null=True)
    txcmps = models.FloatField(null=True)
    rxmcsts = models.FloatField(null=True)

class Iostat(models.Model):
    id = models.AutoField(primary_key=True)
    caseid = models.ForeignKey("Result",to_field='id')
    node = models.CharField(max_length=20)
    osdnum = models.CharField(max_length=20, null=True)
    diskname = models.CharField(max_length=50, null=True)
    time = models.DateTimeField(null=True)
    wrqms = models.FloatField(null=True)
    avgrqsz = models.FloatField(null=True)
    r_await = models.FloatField(null=True)
    await = models.FloatField(null=True)
    ws = models.FloatField(null=True)
    avgqusz = models.FloatField(null=True)
    svctm = models.FloatField(null=True)
    rMBs = models.FloatField(null=True)
    wMBs = models.FloatField(null=True)
    rrqms = models.FloatField(null=True)
    rs = models.FloatField(null=True)
    tps = models.FloatField(null=True)
    util = models.FloatField(null=True)
    w_await = models.FloatField(null=True)

class CephConfig(models.Model):
    id = models.AutoField(primary_key=True)
    caseid = models.ForeignKey("Result",to_field='id')
    node = models.CharField(max_length=20)
    osd  = models.CharField(max_length=20)
    max_open_files = models.CharField(max_length=20, null=True)
    filestore_expected_throughput_bytes = models.CharField(max_length=20, null=True)
    filestore_expected_throughput_ops = models.CharField(max_length=20, null=True)
    filestore_max_sync_interval = models.CharField(max_length=20, null=True)
    filestore_min_sync_interval = models.CharField(max_length=20, null=True)
    filestore_queue_max_bytes = models.CharField(max_length=20, null=True)
    filestore_queue_max_ops = models.CharField(max_length=20, null=True)
    filestore_queue_high_delay_multiple = models.CharField(max_length=20, null=True)
    filestore_queue_max_delay_multiple = models.CharField(max_length=20, null=True)
    filestore_ondisk_finisher_threads = models.CharField(max_length=20, null=True)
    filestore_apply_finisher_threads = models.CharField(max_length=20, null=True)
    filestore_commit_timeout = models.CharField(max_length=20, null=True)
    filestore_fd_cache_shards = models.CharField(max_length=20, null=True)
    filestore_fd_cache_size = models.CharField(max_length=20, null=True)
    filestore_wbthrottle_enable = models.CharField(max_length=20, null=True)
    filestore_op_threads = models.CharField(max_length=20, null=True)
    filestore_op_thread_timeout = models.CharField(max_length=20, null=True)
    filestore_op_thread_suicide_timeout = models.CharField(max_length=20, null=True)
    osd_journal_size = models.CharField(max_length=20, null=True)
    journal_max_write_bytes = models.CharField(max_length=20, null=True)
    journal_max_write_entries = models.CharField(max_length=20, null=True)
    journal_throttle_high_multiple = models.CharField(max_length=20, null=True)
    journal_throttle_max_multiple = models.CharField(max_length=20, null=True)
    rbd_cache = models.CharField(max_length=20, null=True)
    rbd_cache_size = models.CharField(max_length=20, null=True)
    rbd_cache_target_dirty = models.CharField(max_length=20, null=True)
    rbd_cache_max_dirty = models.CharField(max_length=20, null=True)
    rbd_cache_max_dirty_age = models.CharField(max_length=20, null=True)
    rbd_cache_writethrough_until_flush = models.CharField(max_length=20, null=True)
    osd_max_write_size = models.CharField(max_length=20, null=True)
    osd_num_op_tracker_shard = models.CharField(max_length=20, null=True)
    osd_client_message_size_cap = models.CharField(max_length=20, null=True)
    osd_client_message_cap = models.CharField(max_length=20, null=True)
    osd_deep_scrub_stride = models.CharField(max_length=20, null=True)
    osd_op_num_threads_per_shard = models.CharField(max_length=20, null=True)
    osd_op_num_shards = models.CharField(max_length=20, null=True)
    osd_op_threads = models.CharField(max_length=20, null=True)
    osd_op_thread_timeout = models.CharField(max_length=20, null=True)
    osd_op_thread_suicide_timeout = models.CharField(max_length=20, null=True)
    osd_recovery_thread_timeout = models.CharField(max_length=20, null=True)
    osd_recovery_thread_suicide_timeout = models.CharField(max_length=20, null=True)
    osd_disk_threads = models.CharField(max_length=20, null=True)
    osd_map_cache_size = models.CharField(max_length=20, null=True)
    osd_recovery_threads = models.CharField(max_length=20, null=True)
    osd_recovery_op_priority = models.CharField(max_length=20, null=True)
    osd_recovery_max_active = models.CharField(max_length=20, null=True)
    osd_max_backfills = models.CharField(max_length=20, null=True)
    osd_scrub_begin_hour = models.CharField(max_length=20, null=True)
    osd_scrub_end_hour = models.CharField(max_length=20, null=True)
    osd_scrub_sleep = models.CharField(max_length=20, null=True)
    osd_scrub_load_threshold = models.CharField(max_length=20, null=True)
    osd_scrub_chunk_max = models.CharField(max_length=20, null=True)
    osd_scrub_chunk_min = models.CharField(max_length=20, null=True)
    osd_objectstore = models.CharField(max_length=20, null=True)
    objecter_inflight_ops = models.CharField(max_length=20, null=True)
    objecter_inflight_op_bytes = models.CharField(max_length=20, null=True)

class PerfDump(models.Model):
    id = models.AutoField(primary_key=True)
    caseid = models.ForeignKey("Result",to_field='id')
    node = models.CharField(max_length=20)
    osd  = models.CharField(max_length=20, null=True)
    filestore_queue_transaction_latency_avg_avgcount = models.IntegerField(null=True)
    filestore_queue_transaction_latency_avg_sum = models.FloatField(null=True)
    filestore_bytes = models.IntegerField(null=True)
    filestore_ops = models.IntegerField(null=True)
    filestore_op_queue_bytes = models.IntegerField(null=True)
    filestore_journal_bytes = models.IntegerField(null=True)
    filestore_journal_latency_avgcount = models.IntegerField(null=True)
    filestore_journal_latency_sum = models.FloatField(null=True)
    filestore_journal_wr = models.IntegerField(null=True)
    filestore_journal_wr_bytes_avgcount = models.IntegerField(null=True)
    filestore_journal_wr_bytes_sum = models.IntegerField(null=True)
    filestore_journal_ops = models.IntegerField(null=True)
    filestore_apply_latency_avgcount = models.IntegerField(null=True)
    filestore_apply_latency_sum = models.FloatField(null=True)
    filestore_commitcycle = models.IntegerField(null=True)
    filestore_commitcycle_latency_avgcount = models.IntegerField(null=True)
    filestore_commitcycle_sum = models.FloatField(null=True)
    leveldb_leveldb_submit_sync_latency_avgcount = models.IntegerField(null=True)
    leveldb_leveldb_submit_sync_latency_sum = models.FloatField(null=True)
    leveldb_leveldb_get_latency_avgcount = models.IntegerField(null=True)
    leveldb_leveldb_get_latency_sum = models.FloatField(null=True)
    leveldb_leveldb_submit_latency_avgcount = models.IntegerField(null=True)
    leveldb_leveldb_submit_latency_sum = models.FloatField(null=True)
    osd_op = models.IntegerField(null=True)
    osd_op_wip = models.IntegerField(null=True)
    osd_op_in_bytes = models.IntegerField(null=True)
    osd_op_out_bytes = models.IntegerField(null=True)
    osd_op_latency_avgcount = models.IntegerField(null=True)
    osd_op_latency_sum = models.FloatField(null=True)
    osd_op_process_latency_avgcount = models.IntegerField(null=True)
    osd_op_process_latency_sum = models.FloatField(null=True)
    osd_op_prepare_latency_avgcount = models.IntegerField(null=True)
    osd_op_prepare_latency_sum = models.FloatField(null=True)
    osd_op_r_latency_avgcount = models.IntegerField(null=True)
    osd_op_r_latency_sum = models.FloatField(null=True)
    osd_op_r_process_latency_avgcount = models.IntegerField(null=True)
    osd_op_r_process_latency_sum = models.FloatField(null=True)
    osd_op_r = models.IntegerField(null=True)
    osd_op_r_out_bytes = models.IntegerField(null=True)
    osd_op_w = models.IntegerField(null=True)
    osd_op_w_in_bytes = models.IntegerField(null=True)
    osd_op_w_latency_avgcount = models.IntegerField(null=True)
    osd_op_w_latency_sum = models.FloatField(null=True)
    osd_op_w_process_latency_avgcount = models.IntegerField(null=True)
    osd_op_w_process_latency_sum = models.FloatField(null=True)
    osd_op_w_rlat_avgcount = models.IntegerField(null=True)
    osd_op_w_rlat_sum = models.FloatField(null=True)
    osd_stat_bytes_used = models.BigIntegerField(null=True)
    osd_stat_bytes_avail = models.BigIntegerField(null=True)
    osd_buffer_bytes = models.BigIntegerField(null=True)
    recoverystate_perf_primary_latency_avgcount = models.IntegerField(null=True)
    recoverystate_perf_primary_latency_sum = models.FloatField(null=True)
    recoverystate_perf_peering_latency_avgcount = models.IntegerField(null=True)
    recoverystate_perf_peering_latency_sum = models.FloatField(null=True)
    recoverystate_perf_backfilling_latency_avgcount = models.IntegerField(null=True)
    recoverystate_perf_backfilling_latency_sum = models.FloatField(null=True)

class HWInfo(models.Model):
    id = models.AutoField(primary_key=True)
    caseid = models.ForeignKey("Result",to_field='id')
    node = models.CharField(max_length=20)
    HyperThreading = models.CharField(max_length=20, null=True)
    VirtualTechnology = models.CharField(max_length=20, null=True)
    NUMA = models.CharField(max_length=20, null=True)
    OperatingModes = models.CharField(max_length=20, null=True)
    CPUType = models.CharField(max_length=50, null=True)
    CPUCores = models.IntegerField(null=True)
    CPUMaxSpeed = models.CharField(max_length=50, null=True)
    CPUNum = models.IntegerField(null=True)
    MemNum = models.IntegerField(null=True)
    MemType = models.CharField(max_length=50, null=True)
    MemSize = models.CharField(max_length=50, null=True)

class DiskInfo(models.Model):
    id = models.AutoField(primary_key=True)
    caseid = models.ForeignKey("Result",to_field='id')
    node = models.CharField(max_length=20)
    disk_name = models.CharField(max_length=20)
    disk_size = models.CharField(max_length=20)
    disk_model = models.CharField(max_length=20)
    disk_speed = models.CharField(max_length=20)

class OSInfo(models.Model):
    id = models.AutoField(primary_key=True)
    caseid = models.ForeignKey("Result",to_field='id')
    node = models.CharField(max_length=20)
    PIDnumber = models.IntegerField(null=True)
    read_ahead = models.CharField(max_length=20, null=True)
    IOscheduler = models.CharField(max_length=20, null=True)
    dirty_background_ratio = models.CharField(max_length=20, null=True)
    dirty_ratio = models.CharField(max_length=20, null=True)
    MTU = models.CharField(max_length=20, null=True)

class CephStatus(models.Model):
    id = models.AutoField(primary_key=True)
    caseid = models.ForeignKey("Result",to_field='id')
    time = models.DateTimeField(null=True)
    health_overall_status = models.CharField(max_length=20, null=True)
    health_summary = models.CharField(max_length=200, null=True)
    health_detail = models.CharField(max_length=200, null=True)
    fsid = models.CharField(max_length=200, null=True)
    monmap_mons = models.CharField(max_length=200, null=True)
    osdmap_osdmap_num_osds = models.IntegerField(null=True)
    osdmap_osdmap_num_up_osds = models.IntegerField(null=True)
    osdmap_osdmap_num_in_osds = models.IntegerField(null=True)
    pgmap_pgs_by_state = models.CharField(max_length=200, null=True)
    pgmap_num_pgs = models.IntegerField(null=True)
    pgmap_data_bytes = models.BigIntegerField(null=True)
    pgmap_bytes_used = models.BigIntegerField(null=True)
    pgmap_bytes_avail = models.BigIntegerField(null=True)
    pgmap_bytes_total = models.BigIntegerField(null=True)

class Jobs(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    time = models.DateTimeField(null=True)
    status = models.CharField(max_length=20, null=True)

class CephInfo(models.Model):
    id = models.AutoField(primary_key=True)
    caseid = models.ForeignKey("Result",to_field='id')
    monnum = models.IntegerField(null=True)
    nodenum = models.IntegerField(null=True)
    version = models.CharField(max_length=100, null=True)
    osdnum = models.IntegerField(null=True)
    globalrawused = models.CharField(max_length=20, null=True)

class CephPoolInfo(models.Model):
    id = models.AutoField(primary_key=True)
    caseid = models.ForeignKey("Result",to_field='id')
    name = models.CharField(max_length=20)
    pgnum = models.IntegerField(null=True)
    size = models.IntegerField(null=True) 
