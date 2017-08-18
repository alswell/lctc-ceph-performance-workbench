/**
 * Created by chenkang1 on 2017/6/30.
 */
import React from 'react'
import PropTypes from 'prop-types'
import { connect } from 'dva'
import DataTable from '../../components/BasicTable/DataTable'
import { Modal, Row, Col, Card, Button, Tabs } from 'antd'
import { Link } from 'dva/router'
import DropOption from '../../components/DropOption/DropOption'
import BatchModal from '../../components/modals/BatchModal'
import { fetchAndNotification } from '../../services/restfulService'
import { CollectionsPage } from '../../components/host/CreateModal'

const confirm = Modal.confirm
const TabPane = Tabs.TabPane;

class HostPage extends React.Component {
  // constructor (props) {
  //   super(props)
  // }

  componentDidMount () {

  }

  handleMenuClick = (record, e) => {
    if (e.key === '1') {
      let { dispatch } = this.props
      dispatch({
        type: 'host/showModal',
        payload: {
          key: 'modalVisible',
        },

      })
    } else if (e.key === '2') {
      confirm({
        title: 'Are you sure delete this record?',
        onOk () {
          console.log(record)
        },
      })
    }
  };

  showModal = (key) => {
    let { dispatch } = this.props
    dispatch({
      type: 'host/showModal',
      payload: {
        key,
      },
    })
  };

  refresh = () => {
    this.props.dispatch({ type: 'host/refresh' })
  };

  init = () => {
    this.modalProps = {
      visible: this.props.host.modalVisible,
      maskClosable: true,
      title: 'test',
      wrapClassName: 'vertical-center-modal',
      onOk: (data) => {
        console.log(data)
      },
      onCancel: () => {
        let { dispatch } = this.props
        dispatch({
          type: 'host/hideModal',
          payload: {
            key: 'modalVisible',
          },
        })
      },
    }

    this.cputableDataProps = {
      columns: [
        {
          title: 'Case ID',
          dataIndex: 'caseid',
          key: 'caseid',
          width: 60,
          sorter: true,
        }, {
          title: 'Start Time',
          dataIndex: 'time',
          key: 'time',
          sorter: true,
          width: 150,
        }, {
          title: 'Node',
          dataIndex: 'node',
          key: 'node',
          width: 80,
        }, {
          title: '%usr',
          dataIndex: 'usr',
          key: 'usr',
          sorter: true,
          // width: 100,
        }, {
          title: '%nice',
          dataIndex: 'nice',
          key: 'nice',
          sorter: true,
          // width: 64,
        }, {
          title: '%sys',
          dataIndex: 'sys',
          key: 'sys',
          sorter: true,
        },
        {
          title: '%iowait',
          dataIndex: 'iowait',
          key: 'iowait',
        }, {
          title: '%steal',
          dataIndex: 'steal',
          key: 'steal',
        }, {
          title: '%irq',
          dataIndex: 'irq',
          key: 'irq',
        },
        {  
          title: '%soft',
          dataIndex: 'soft',
          key: 'soft',
        }, {
          title: '%guest',
          dataIndex: 'guest',
          key: 'guest',
        }, {
          title: '%gnice',
          dataIndex: 'gnice',
          key: 'gnice',
        }, {
          title: '%idle',
          dataIndex: 'idle',
          key: 'idle',
        }, {
          title: 'Operation',
          key: 'operation',
          width: 100,
          render: (text, record) => {
            return (<DropOption onMenuClick={e => this.handleMenuClick(record, e)}
              menuOptions={[{ key: '1', name: 'Update' }, { key: '2', name: 'Delete' }]}
            />)
          },
        },
      ],
      fetchData: {
        url: this.props.host.caseid ? `sarcpu/${this.props.host.caseid}/`:`sarcpu`,
        params: null,
      },
      errorMsg: 'get sar cpu table error',
      refresh: this.props.host.refresh,
      handleSelectItems: (selectedRows) => {
        this.props.dispatch({ type: 'host/updateSelectItems', payload: selectedRows })
      },
    }

    this.memtableDataProps = {
      columns: [
        {
          title: 'Case ID',
          dataIndex: 'caseid',
          key: 'caseid',
          width: 60,
          sorter: true,
        }, {
          title: 'Start Time',
          dataIndex: 'time',
          key: 'time',
          sorter: true,
          width: 150,
        }, {
          title: 'Node',
          dataIndex: 'node',
          key: 'node',
          width: 80,
        }, {
          title: 'kbmemfree',
          dataIndex: 'kbmemfree',
          key: 'kbmemfree',
        }, {
          title: 'kbmemused',
          dataIndex: 'kbmemused',
          key: 'kbmemused',
        }, {
          title: '%memused',
          dataIndex: 'memused',
          key: 'memused',
        },
        {
          title: 'kbbuffers',
          dataIndex: 'kbbuffers',
          key: 'kbbuffers',
        }, {
          title: 'kbcached',
          dataIndex: 'kbcached',
          key: 'kbcached',
        }, {
          title: 'kbcommit',
          dataIndex: 'kbcommit',
          key: 'kbcommit',
        },
        {  
          title: '%commit',
          dataIndex: 'commit',
          key: 'commit',
        }, {
          title: 'kbactive',
          dataIndex: 'kbactive',
          key: 'kbactive',
        }, {
          title: 'kbinact',
          dataIndex: 'kbinact',
          key: 'kbinact',
        }, {
          title: 'kbdirty',
          dataIndex: 'kbdirty',
          key: 'kbdirty',
        }, {
          title: 'Operation',
          key: 'operation',
          width: 100,
          render: (text, record) => {
            return (<DropOption onMenuClick={e => this.handleMenuClick(record, e)}
              menuOptions={[{ key: '1', name: 'Update' }, { key: '2', name: 'Delete' }]}
            />)
          },
        },
      ],
      fetchData: {
        url: this.props.host.caseid ? `sarmem/${this.props.host.caseid}/`:`sarmem`,
        params: null,
      },
      errorMsg: 'get sarmem table error',
      refresh: this.props.host.refresh,
      handleSelectItems: (selectedRows) => {
        this.props.dispatch({ type: 'host/updateSelectItems', payload: selectedRows })
      },
    }

    this.nictableDataProps = {
      columns: [
        {
          title: 'Case ID',
          dataIndex: 'caseid',
          key: 'caseid',
          width: 60,
          sorter: true,
        }, {
          title: 'Start Time',
          dataIndex: 'time',
          key: 'time',
          sorter: true,
          width: 150,
        }, {
          title: 'Node',
          dataIndex: 'node',
          key: 'node',
          width: 80,
        }, {
          title: 'Network',
          dataIndex: 'network',
          key: 'network',
          width: 120,
        }, {
          title: 'rxpck/s',
          dataIndex: 'rxpcks',
          key: 'rxpcks',
        }, {
          title: 'txpck/s',
          dataIndex: 'txpcks',
          key: 'txpcks',
        }, {
          title: 'rxkB/s',
          dataIndex: 'rxkBs',
          key: 'rxkBs',
        },
        {
          title: 'txkB/s',
          dataIndex: 'txkBs',
          key: 'txkBs',
        }, {
          title: 'rxcmp/s',
          dataIndex: 'rxcmps',
          key: 'rxcmps',
        }, {
          title: 'txcmp/s',
          dataIndex: 'txcmps',
          key: 'txcmps',
        },
        {  
          title: 'rxmcst/s',
          dataIndex: 'rxmcsts',
          key: 'rxmcsts',
        }, {
          title: 'Operation',
          key: 'operation',
          width: 100,
          render: (text, record) => {
            return (<DropOption onMenuClick={e => this.handleMenuClick(record, e)}
              menuOptions={[{ key: '1', name: 'Update' }, { key: '2', name: 'Delete' }]}
            />)
          },
        },
      ],
      fetchData: {
        url: this.props.host.caseid ? `sarnic/${this.props.host.caseid}/`:`sarnic`,
        params: null,
      },
      errorMsg: 'get sarnic table error',
      refresh: this.props.host.refresh,
      handleSelectItems: (selectedRows) => {
        this.props.dispatch({ type: 'host/updateSelectItems', payload: selectedRows })
      },
    }

    this.iostattableDataProps = {
      columns: [
        {
          title: 'Case ID',
          dataIndex: 'caseid',
          key: 'caseid',
          width: 60,
          sorter: true,
        }, {
          title: 'Start Time',
          dataIndex: 'time',
          key: 'time',
          sorter: true,
          width: 150,
        }, {
          title: 'Node',
          dataIndex: 'node',
          key: 'node',
          width: 80,
        }, {
          title: 'osd',
          dataIndex: 'osdnum',
          key: 'osdnum',
        }, {
          title: 'Disk',
          dataIndex: 'diskname',
          key: 'diskname',
        }, {
          title: 'rrqm/s',
          dataIndex: 'rrqms',
          key: 'rrqm/s',
        }, {
          title: 'wrqm/s',
          dataIndex: 'wrqms',
          key: 'wrqms',
        }, {
          title: 'r/s',
          dataIndex: 'rs',
          key: 'rs',
        },
        {
          title: 'w/s',
          dataIndex: 'ws',
          key: 'ws',
        }, {
          title: 'rMB/s',
          dataIndex: 'rMBs',
          key: 'rMBs',
        }, {
          title: 'wMB/s',
          dataIndex: 'wMBs',
          key: 'wMBs',
        }, {  
          title: 'avgrq-sz',
          dataIndex: 'avgrqsz',
          key: 'avgrqsz',
        }, {
          title: 'await',
          dataIndex: 'await',
          key: 'await',
        }, {
          title: 'r_await',
          dataIndex: 'r_await',
          key: 'r_await',
        }, {
          title: 'w_await',
          dataIndex: 'w_await',
          key: 'w_await',
        }, {
          title: 'svctm',
          dataIndex: 'svctm',
          key: 'svctm',
        }, {
          title: '%util',
          dataIndex: 'util',
          key: 'util',
        }, {
          title: 'Operation',
          key: 'operation',
          width: 100,
          render: (text, record) => {
            return (<DropOption onMenuClick={e => this.handleMenuClick(record, e)}
              menuOptions={[{ key: '1', name: 'Update' }, { key: '2', name: 'Delete' }]}
            />)
          },
        },
      ],
      fetchData: {
        url: this.props.host.caseid ? `iostat/${this.props.host.caseid}/`:`iostat`,
        params: null,
      },
      errorMsg: 'get iostat table error',
      refresh: this.props.host.refresh,
      handleSelectItems: (selectedRows) => {
        this.props.dispatch({ type: 'host/updateSelectItems', payload: selectedRows })
      },
    }

    this.cephstatustableDataProps = {
      columns: [
        {
          title: 'Case ID',
          dataIndex: 'caseid',
          key: 'caseid',
          width: 60,
          sorter: true,
        }, {
          title: 'Start Time',
          dataIndex: 'time',
          key: 'time',
          sorter: true,
          width: 150,
        }, {
          title: 'Health',
          dataIndex: 'health_overall_status',
          key: 'health_overall_status',
        }, {
          title: 'Health Summary',
          dataIndex: 'health_summary',
          key: 'health_summary',
          width: 120,
        }, {
          title: 'Health Detail',
          dataIndex: 'health_detail',
          key: 'health_detail',
        }, {
          title: 'fsid',
          dataIndex: 'fsid',
          key: 'fsid',
        }, {
          title: 'monmap_mons',
          dataIndex: 'monmap_mons',
          key: 'monmap_mons',
        },
        {
          title: 'osdmap_osdmap_num_osds',
          dataIndex: 'osdmap_osdmap_num_osds',
          key: 'osdmap_osdmap_num_osds',
        }, {
          title: 'osdmap_osdmap_num_up_osds',
          dataIndex: 'osdmap_osdmap_num_up_osds',
          key: 'osdmap_osdmap_num_up_osds',
        }, {
          title: 'osdmap_osdmap_num_in_osds',
          dataIndex: 'osdmap_osdmap_num_in_osds',
          key: 'osdmap_osdmap_num_in_osds',
        },
        {  
          title: 'pgmap_pgs_by_state',
          dataIndex: 'pgmap_pgs_by_state',
          key: 'pgmap_pgs_by_state',
        }, {
          title: 'pgmap_num_pgs',
          dataIndex: 'pgmap_num_pgs',
          key: 'pgmap_num_pgs',
        }, {
          title: 'pgmap_data_bytes',
          dataIndex: 'pgmap_data_bytes',
          key: 'pgmap_data_bytes',
        }, {
          title: 'pgmap_bytes_used',
          dataIndex: 'pgmap_bytes_used',
          key: 'pgmap_bytes_used',
        }, {
          title: 'pgmap_bytes_avail',
          dataIndex: 'pgmap_bytes_avail',
          key: 'pgmap_bytes_avail',
        }, {
          title: 'pgmap_bytes_total',
          dataIndex: 'pgmap_bytes_total',
          key: 'pgmap_bytes_total',
        }, {
          title: 'Operation',
          key: 'operation',
          width: 100,
          render: (text, record) => {
            return (<DropOption onMenuClick={e => this.handleMenuClick(record, e)}
              menuOptions={[{ key: '1', name: 'Update' }, { key: '2', name: 'Delete' }]}
            />)
          },
        },
      ],
      fetchData: {
        url: this.props.host.caseid ? `cephstatus/${this.props.host.caseid}/`:`cephstatus`,
        params: null,
      },
      errorMsg: 'get sarnic table error',
      refresh: this.props.host.refresh,
      handleSelectItems: (selectedRows) => {
        this.props.dispatch({ type: 'host/updateSelectItems', payload: selectedRows })
      },
    }

    this.cephinfotableDataProps = {
      columns: [
        {
          title: 'Case ID',
          dataIndex: 'caseid',
          key: 'caseid',
          width: 60,
          sorter: true,
        }, {
          title: 'Monitor Number',
          dataIndex: 'monnum',
          key: 'monnum',
        }, {
          title: 'Node Number',
          dataIndex: 'nodenum',
          key: 'nodenum',
        }, {
          title: 'Version',
          dataIndex: 'version',
          key: 'version',
        }, {
          title: 'osd Number',
          dataIndex: 'osdnum',
          key: 'osdnum',
        }, {
          title: 'global raw used',
          dataIndex: 'globalrawused',
          key: 'globalrawused',
        }, {
          title: 'Operation',
          key: 'operation',
          width: 100,
          render: (text, record) => {
            return (<DropOption onMenuClick={e => this.handleMenuClick(record, e)}
              menuOptions={[{ key: '1', name: 'Update' }, { key: '2', name: 'Delete' }]}
            />)
          },
        },
      ],
      title: 'Ceph Info',
      fetchData: {
        url: this.props.host.caseid ? `cephinfo/${this.props.host.caseid}/`:`cephinfo`,
        params: null,
      },
      errorMsg: 'get cephinfo table error',
      refresh: this.props.host.refresh,
      handleSelectItems: (selectedRows) => {
        this.props.dispatch({ type: 'host/updateSelectItems', payload: selectedRows })
      },
    }

    this.poolinfotableDataProps = {
      columns: [
        {
          title: 'Case ID',
          dataIndex: 'caseid',
          key: 'caseid',
          width: 60,
          sorter: true,
        }, {
          title: 'Pool Name',
          dataIndex: 'name',
          key: 'name',
        }, {
          title: 'PG Number',
          dataIndex: 'pgnum',
          key: 'pgnum',
        }, {
          title: 'Size',
          dataIndex: 'size',
          key: 'size',
        }, {
          title: 'Operation',
          key: 'operation',
          width: 100,
          render: (text, record) => {
            return (<DropOption onMenuClick={e => this.handleMenuClick(record, e)}
              menuOptions={[{ key: '1', name: 'Update' }, { key: '2', name: 'Delete' }]}
            />)
          },
        },
      ],
      title: 'Pool Info',
      fetchData: {
        url: this.props.host.caseid ? `poolinfo/${this.props.host.caseid}/`:`poolinfo`,
        params: null,
      },
      errorMsg: 'get poolinfo table error',
      refresh: this.props.host.refresh,
      handleSelectItems: (selectedRows) => {
        this.props.dispatch({ type: 'host/updateSelectItems', payload: selectedRows })
      },
    }

    this.batchModalProps = {
      visible: this.props.host.batchModalVisible,
      maskClosable: true,
      title: 'Batch Action Modal',
      wrapClassName: 'vertical-center-modal',
      selectedItems: this.props.host.selectedItems,
      fetchData: {
        url: 'host',
        method: 'delete',
      },
      onOk: (data) => {
        this.batchModalProps.onCancel()
        this.props.host.selectedItems.forEach((item) => {
          fetchAndNotification({
            url: 'host',
            method: 'delete',
            params: { ids: item.id },
            notifications: {
              title: 'batch Action',
              success: `${item.name} 操作成功！`,
              error: `${item.name} 操作失败！`,
            },
          })
        })
      },
      onCancel: () => {
        let { dispatch } = this.props
        dispatch({
          type: 'host/hideModal',
          payload: {
            key: 'batchModalVisible',
          },
        })
      },
    }

    this.createModalProps = {
      visible: this.props.host.createModalVisible,
      maskClosable: true,
      title: 'Batch Action Modal',
      wrapClassName: 'vertical-center-modal',
      selectedItems: this.props.host.selectedItems,
      fetchData: {
        url: 'host',
        method: 'delete',
      },
      onOk: (data) => {
        this.batchModalProps.onCancel()
        this.props.host.selectedItems.forEach((item) => {
          fetchAndNotification({
            url: 'host',
            method: 'delete',
            params: { ids: item.id },
            notifications: {
              title: 'batch Action',
              success: `${item.name} 操作成功！`,
              error: `${item.name} 操作失败！`,
            },
          })
        })
      },
      onCancel: () => {
        let { dispatch } = this.props
        dispatch({
          type: 'host/hideModal',
          payload: {
            key: 'createModalVisible',
          },
        })
      },
    }
  };


  render () {
    this.init()

    return (
      <div className="content-inner">
        <Tabs type="card">
          <TabPane tab="cpu" key="1">
            <DataTable
              {...this.cputableDataProps}
            />
          </TabPane>
          <TabPane tab="memory" key="2">
            <DataTable
              {...this.memtableDataProps}
            />
          </TabPane>
          <TabPane tab="network" key="3">
            <DataTable
              {...this.nictableDataProps}
            />
          </TabPane>
          <TabPane tab="disk" key="4">
            <DataTable
              {...this.iostattableDataProps}
            />
          </TabPane>
          <TabPane tab="Ceph status" key="5">
            <DataTable
              {...this.cephstatustableDataProps}
            />
          </TabPane>
           <TabPane tab="Ceph info" key="6">
            <DataTable
              {...this.cephinfotableDataProps}
            />
          </TabPane>
          <TabPane tab="Ceph Pool" key="7">
            <DataTable
              {...this.poolinfotableDataProps}
            />
          </TabPane>
        </Tabs>
        {this.props.host.modalVisible && <Modal {...this.modalProps} />}
        {this.props.host.batchModalVisible && <BatchModal {...this.batchModalProps} />}
      </div>
    )
  }
}


function mapStateToProps ({ sysdata }) {
  return {
    host:sysdata,
  }
}

HostPage.propTypes = {
  cluster: PropTypes.object,
  location: PropTypes.object,
  dispatch: PropTypes.func,
  loading: PropTypes.object,
  host: PropTypes.object,
}

export default connect(mapStateToProps)(HostPage)

